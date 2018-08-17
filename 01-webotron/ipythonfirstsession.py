# coding: utf-8
import boto3
session =boto3.Session(profile_name='pythonautomtion')
session =boto3.Session(profile_name='pythonAutomtion')
session =boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print bucket
for bucket in s3.buckets.all():
    print bucket
for bucket in s3.buckets.all():
    print(bucket)
    
new_bucket = s3.create_bucket(Bucket='automatingawsdavidoh-boto')
get_ipython().run_line_magic('history', '')
new_bucket = s3.create_bucket(Bucket='automatingawsdavidoh-boto3', CreatebucketConfiguration={'LocationConstraint':'us-east-2'})
new_bucket = s3.create_bucket(Bucket='automatingawsdavidoh-boto3', CreatebucketConfiguration={'LocationConstraint':'us-east-2'})
new_bucket = s3.create_bucket(Bucket='automatingawsdavidoh-boto3', CreateBucketConfiguration={'LocationConstraint':'us-east-2'})
new_bucket
for bucket in s3.buckets.all():
    print(bucket)
    
get_ipython().run_line_magic('history', '')
ec2_client = session.client('ec2')
ec2
ec2_client
