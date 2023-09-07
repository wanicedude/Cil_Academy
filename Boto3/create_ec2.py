import boto3


def ami_state(ec2_client, AMI):
    # Checking if the AMI state is available
    response = ec2_client.describe_images(ImageIds=[AMI])
    ami_state = response["Images"][0]["State"]
    return ami_state


# Get Amazon AMIs owned by Amazon
def Get_Image(ec2_client):
    images = ec2_client.describe_images(
        Filters=[
            {
                "Name": "name",
                "Values": [
                    # "amzn2-ami-hvm*",
                    "al2023-ami-2023*",
                ],
            },
            {
                "Name": "boot-mode",
                "Values": [
                    "uefi-preferred",
                ],
            },
            {
                "Name": "owner-alias",
                "Values": [
                    "amazon",
                ],
            },
        ],
    )
    AMI = images["Images"][0]["ImageId"]
    return AMI


# Create EC2 instance
def Start_Ec2(AMI, ec2_client, ec2_resource, ami_state, user_data):
    """Use the AMI gotten from the Get Image to create an EC2 instance"""

    if ami_state == "available":
        # Create instance if AMI state is available
        instance = ec2_client.run_instances(
            ImageId=AMI,
            InstanceType="t2.micro",
            MaxCount=1,
            MinCount=1,
            KeyName = "Lala",
            UserData=user_data,
            SecurityGroupIds = ["sg-020b176d16ae1479c",],
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [{"Key": "Name", "Value": "CIL_ACADEMY"}],
                }
            ],
        )
        # This is to print the newly created Instance ID
        ec2 = ec2_resource.Instance(instance["Instances"][0]["InstanceId"])
        return ec2
    else:
        print("The AMI was not available")
        return None


# Used to only run the code inside the if statement when the program is run directly by the Python interpreter. The code inside the if statement is not executed when the file's code is imported as a module".
# This means i can make use of the two other functions when i Import this file as a module without running the specific tasks or tests meant for standalone execution.
if __name__ == "__main__":
    # Create an EC2 client object & Resource
    ec2_client = boto3.client("ec2")
    ec2_resource = boto3.resource("ec2")

    # Create User Data Variable to install Apache server
    User_data = """#!/bin/bash
        sudo su
        yum update -y
        yum install httpd -y
        echo "<h1>This is Cohort 6 Server</h1>" > /var/www/html/index.html
        echo "<h2>This is my private IP: $(hostname -f)</h2>" >> /var/www/html/index.html
        systemctl start httpd"""

    # Get AMI
    AMI = Get_Image(ec2_client)

    # Get AMI State
    Ami_State = ami_state(ec2_client, AMI)

    # Create and start the ec2 instance
    ec2 = Start_Ec2(AMI, ec2_client, ec2_resource, Ami_State, User_data)

    # Print Ec2 Instance ID
    Instance = ec2_resource.Instance(ec2.instance_id)

    # Using boto3 Waiters
    ec2.wait_until_running()

    print(f"Instance is {ec2.state['Name']}")

    # Terminate Ec2 Instance
    ec2.terminate()

    # Using boto3 Waiters
    ec2.wait_until_terminated()
    print(f"Instance is {ec2.state['Name']}")
