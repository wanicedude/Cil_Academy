# AWS CLI HANDS-ON

>**Commands & Steps**

1. Install AWS CLI on terminal. *Documentation Link: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html*

2. Configure AWS on CLI using the necessary details (Region, Access Key & Secret Access Key)

3. Get an Amazon owned AMI using the Describe Images Command Flag:        
*aws ec2 describe-images \ \
    --owners amazon \ \
    --filters "Name=name,Values=amzn2-ami-hvm-2.0.????????.?-x86_64-gp2" "Name=root-device-type,Values=ebs" "Name=virtualization-type, Values=hvm" \ \
    --query 'Images[0].[ImageId]' \ \
    --output text*


 1. Create an EC2 instance using the "Run instance" command flag:      
 *aws ec2 run-instances \ \
--image-id ami-038b3df3312ddf25d \ \
--instance-type t2.micro \ \
--count 1 \ \
--key-name Lala \ \
--security-group-ids  \ \
--user-data $'#!/bin/bash\nsudo su\nyum update -y\nyum install httpd -y\nsystemctl start httpd'*


# AWS SDK BOTO3

1. Documentation Link: *https://aws.amazon.com/developer/tools/*
2. Boto3 Quick Start Link: *https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html*

4.  Get AMI that are owned by Amazon using the describe image documentation. Link: *https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instances.html*

4. Create EC2 Instance using the run instance documentation. Link: *https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/run_instances.html*.
