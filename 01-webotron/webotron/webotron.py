import boto3
import sys
import click

session = boto3.Session(profile_name = 'pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass

#@click.command('list-buckets')
@cli.command('list-buckets') # cli becomes the decorator. deligate control of command
# @click is a decorator. and it will control the way our function runs
def list_buckets():
    "List all s3 buckets" # document string. use --help
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    for object in s3.Bucket(bucket).objects.all():
        print(object)


if __name__ == '__main__':
    #print(sys.argv)
    print("I am using click and click.group 1")
    cli()
    print("I am using click and click.group 2")

## python convention
## when this file run as script __name__ will eaqual __main__
