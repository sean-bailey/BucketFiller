bucketfiller template
needs to create the s3 bucket, the role, and the ec2 instance with proper
configurations set in the UserData section
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")

This needs to be one-click deployable with Ansible.
