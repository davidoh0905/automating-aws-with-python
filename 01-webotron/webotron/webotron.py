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

import boto3
import sys
import click

from bucket import BucketManager

# to make this available for all other functions, define them here
session = None # session has to be configured after cli since options will only work once cli is working
bucket_manager = None

@click.group()
@click.option('--profile', default=None,
    help="Use a given AWS profile.")
def cli(profile): # only when the group takes over
    """Webotron deploys websites to AWS."""
    # profile name configuration. let user pass in the profile
    global session, bucket_manager # to reset them here

    session_cfg={} # dictionary
    if profile:
        session_cfg['profile_name'] = profile

    session=boto3.Session(**session_cfg)  # glob? #profile_name='pythonAutomation'
    bucket_manager = BucketManager(session) ## bucket manager will later hold S3 resource

    pass


#@click.command('list-buckets')
@cli.command('list-buckets') # cli becomes the decorator. deligate control of command
# @click is a decorator. and it will control the way our function runs
def list_buckets():
    """List all S3 buckets.""" # document string. use --help
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List contents of the bucket."""
    for object in bucket_manager.all_objects(bucket):
        print(object)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    print("requesting to create bucket with name "+bucket)
    # has to be defined before going into try and except block
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync Contents of PATHNAME to BUCKET."""
    #s3_bucket = bucket_manager.s3.Bucket(bucket)
    bucket_manager.sync(pathname, bucket)

    print(" sync function worked! ")

# a single file in python is treated as a module
# BUT, if you want to run it as a script
# give __name__ == '__main__'
if __name__ == '__main__':
    #print(sys.argv)
    print("I am using click and click.group 1")
    cli() # initialize click group
    print("I am using click and click.group 2")

# python convention
# when this file run as script __name__ will eaqual __main__
