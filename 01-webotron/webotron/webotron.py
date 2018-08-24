#!/usr/bin/python    : #! interpreter
# -*- coding: utf-8 -*-       # encoding?

"""Webotron: Deploy websites with AWS.

Webotro automates the process of deploying static websites to AWS.
- configure AWS S3 list_buckets
    - Create them
    - Set them up for statis website hosting
    - Deploy local files to them
- configure DNS with AWS Route 53
- Configure a content delivery Network and SSL with AWS

## it's a good habit to leave the comments in the doc string
"""

from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError
import boto3
import sys
import click


SESSION=boto3.Session(profile_name='pythonAutomation')
S3=SESSION.resource('s3')


@click.group()
def cli():
    """Webotron deploys websites to AWS."""
    pass


#@click.command('list-buckets')
@cli.command('list-buckets') # cli becomes the decorator. deligate control of command
# @click is a decorator. and it will control the way our function runs
def list_buckets():
    """List all S3 buckets.""" # document string. use --help
    for bucket in S3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List contents of the bucket."""
    for object in S3.Bucket(bucket).objects.all():
        print(object)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    print("requesting to create bucket with name "+bucket)
    # has to be defined before going into try and except block
    s3_bucket=None

    # s3_bucket = s3.create_bucket(
    #     Bucket= bucket,
    #     CreateBucketConfiguration={'LocationConstraint' : session.region_name})

    try: s3_bucket = S3.create_bucket(
        Bucket= bucket,
        CreateBucketConfiguration={
            'LocationConstraint' : SESSION.region_name
            }
        )

    except ClientError as error:
        if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = S3.Bucket(bucket)
        else:
            raise error

    policy = """
    {
    "Version":"2012-10-17",
    "Statement":[{
        "Sid":"PublicReadGetObject",
        "Effect":"Allow",
        "Principal": "*",
        "Action":["s3:GetObject"],
        "Resource":["arn:aws:s3:::%s/*"
          ]
        }
      ]
    }
    """ % s3_bucket.name
    policy = policy.strip()

    pol = s3_bucket.Policy()
    pol.put(Policy=policy)

    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    }
    )
    return


def upload_file(s3_bucket, path, key):
    """Upload file to S3 bucket."""
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
            'ContentType' : content_type
        }
    )


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def syn(pathname, bucket):
    """Sync Contents of PATHNAME to BUCKET."""
    s3_bucket = S3.Bucket(bucket)

    #closure
    root = Path(pathname).expanduser().resolve()

    # the pathname given is relative path. expanduser expands this to absolute path.
    # and resolve... what does it do?
    # both full path / relative path / tilda all works
    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_directory(p)
            if p.is_file():
                upload_file(s3_bucket, str(p), str(p.relative_to(root)))
                                # print("Path : {}\n Key : {}".format(p, p.relative_to(root)))

    handle_directory(root)

    print(" sync function worked! ")



if __name__ == '__main__':
    #print(sys.argv)
    print("I am using click and click.group 1")
    cli()
    print("I am using click and click.group 2")

# python convention
# when this file run as script __name__ will eaqual __main__
