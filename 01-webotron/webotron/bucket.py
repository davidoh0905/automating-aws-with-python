# -*- coding: utf-8 -*-
from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError


"""Classes for S3 Buckets."""

# package is a directory with modules

class BucketManager:
    """Manage an S3 Bucket."""
    def __init__(self, session):
        """Create a BucketManager object."""
        self.session = session
        self.s3 = self.session.resource('s3')
        # from inside the BucketManager
        # self.s3 is our s3 resource
        # with bucket_manager object, you can access .s3

    def all_buckets(self):
        """Get an iterator for all buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get an iterator for all objects in the bucket"""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create a Bucket or find bucket if it exists"""

        s3_bucket=None

        # s3_bucket = s3.create_bucket(
        #     Bucket= bucket,
        #     CreateBucketConfiguration={'LocationConstraint' : session.region_name})

        try:
            s3_bucket = self.s3.create_bucket(
                Bucket= bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint' : self.session.region_name # what the hell is self.session
                    }
                )

        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise error

        return s3_bucket

    def set_policy(self, bucket):
        """Set bucket policy readable by everyone"""
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
        """ % bucket.name
        policy = policy.strip()

        pol = bucket.Policy()
        pol.put(Policy=policy)

    def configure_website(self, bucket):
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        }
        )

    @staticmethod
    # do not need 'self'. how is this fucking working?
    def upload_file(bucket_name, path, key):
        """Upload file to S3 bucket."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        return bucket_name.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType' : content_type
            }
        )

    def sync(self, pathname, bucket_name):
        bucket = self.s3.Bucket(bucket_name) #assuming that the bucket exist
        root = Path(pathname).expanduser().resolve()

        # the pathname given is relative path. expanduser expands this to absolute path.
        # and resolve... what does it do?
        # both full path / relative path / tilda all works
        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.upload_file(bucket, str(p), str(p.relative_to(root)))
                                    # print("Path : {}\n Key : {}".format(p, p.relative_to(root)))

        handle_directory(root)

# every class in python as constructor called __init__
# when constructor is called will get instance of our class
# object as first argument and traditionally it is called "self"
# to use it we will use an instance of a class
