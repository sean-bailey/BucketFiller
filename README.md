This project was a proof of concept creating a Flask based, FOSS web based S3 bucket interface for managing data on the bucket. It allows users to upload, download, view and delete files on the bucket.

This is designed to be deployed on an EC2 instance with the following environmental variables configured:

`S3_BUCKET`: The name of the bucket to use with this program
`S3_KEY`: (optional, not recommended): the AWS Access Key to use with this bucket (like if Bucket is external to account)
`S3_SECRET`: (optional, not recommended): the AWS Secret Access Key to use with this bucket (like if Bucket is external to account)
`APPLICATION_PORT`: (optional, default 80): the port you'd like this application to run on.

Ideally, you would not want to expose this application directly to the internet. It is highly recommended that you keep the application on a private subnet, with a role attached to the EC2 instance which gives permissions to the S3 bucket (HEAD,GET,LIST,DELETE). Use an ALB with SSL termination at the load balancer to keep the system secure.

Improvements needed:

1) Change placeholder strings for `__init__.py` to prevent obvious potential for bugs.
2) Remove unnecessary comments during PoC development
3) Improve UI with some real graphical design (React?)
4) Create Ansible scripts to deploy EC2 instance with role and ALB as recommended above, install this software, and configure it appropriately.
