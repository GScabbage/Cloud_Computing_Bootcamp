import logging
import boto3
from botocore.exceptions import ClientError
import os


def create_bucket(bucket_name):
    region='eu-west-1'
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    #return True
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    return True

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        os.remove("test.txt")
    except ClientError as e:
        logging.error(e)
        return False
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    for bucket_object in bucket.objects.all():
        print(bucket_object)
    return True


def download_file(file_name,bucket):
    s3 = boto3.client('s3')
    file_name2 = 'test2.txt'
    s3.download_file(bucket, file_name, file_name2)


def delete_bucket(bucket,file_name,object_name=None):
    create_bucket(bucket)
    upload_file(file_name,bucket,object_name=None)
    download_file(file_name,bucket)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)

    bucket.objects.all().delete()
    bucket.delete()


delete_bucket('devops-gswirsky-bootcamp-python','test.txt')
#create_bucket('devops-gswirsky-bootcamp-python')
