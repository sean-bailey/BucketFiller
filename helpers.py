import boto3
import botocore
from config import S3_BUCKET  # we will be using the role
from config import S3_LOCATION

s3 = boto3.client('s3')


def upload_file_to_s3(file, bucket_name):

    try:
        print(str(file.filename))
        print("bucket is %s" % bucket_name)
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                'ServerSideEncryption': 'aws:kms',
                "ContentType": file.content_type
            }
        )
        print(S3_BUCKET)
    except Exception as e:
        print("upload file Error message is %s" % str(e))
        return e
    return "{}{}{}{}{}{}{}".format('<a href="',
                                   S3_LOCATION,
                                   '/',
                                   file.filename,
                                   '">',
                                   file.filename,
                                   '</a>'
                                   )


def list_contents_of_bucket(bucket_name):
    try:
        print("listing contents of bucket %s" % bucket_name)
        returneddict = {}

        myobjects = s3.list_objects_v2(
            Bucket=bucket_name,
            Delimiter=','
        )
        if 'Contents' in myobjects.keys():
            for object in myobjects['Contents']:
                urlstring = ('%s/%s' % (S3_LOCATION, object['Key'],))
                returneddict[urlstring] = str(object['Key'])
            return returneddict
        else:
            returneddict[''] = "No objects in bucket!"
    except Exception as e:
        print(" list contents Error message is %s" % str(e))


def get_object_size(objectname, bucket_name):
    print("Getting object size of %s" % objectname)
    result = s3.list_objects_v2(Bucket=bucket_name, Delimiter=',')
    for item in result['Contents']:
        if item['Key'] == objectname:
            print(item['Size'])
            print(type(item['Size']))
            return item['Size']


def get_object_large(objectname, objectsize, bucket_name):
    offset = 0
    print("Getting large object...")
    while objectsize > 0:
        end = offset + 999999 if objectsize > 1000000 else ""
        objectsize -= 1000000
        byte_range = 'bytes={offset}-{end}'.format(offset=offset, end=end)
        offset = end + 1 if not isinstance(end, basestring) else None
        yield s3.get_object(Bucket=bucket_name, Key=objectname,
                            Range=byte_range)['Body'].read()


def delete_object(objectname, bucket_name):
    if get_object_size(objectname, bucket_name):
        response = s3.delete_object(Bucket=bucket_name, Key=objectname)
    else:
        response = "Object not found in bucket"
    return response


def get_object(objectname, objectsize, bucket_name):
    if objectsize > 1000000:
        get_object_large(objectname, objectsize, bucket_name)
    else:
        print("Getting small object...")
        return s3.get_object(Bucket=bucket_name, Key=objectname)['Body'].read()
