import boto3
import time

INSTANCE_ID = "i-06ed6cd08216f604b"
REGION = "us-east-1"

def allocate_and_associate_eip():
    ec2 = boto3.client('ec2', region_name=REGION)
    
    print(f"Allocating new Elastic IP in {REGION}...")
    alloc_resp = ec2.allocate_address(
        Domain='vpc',
        TagSpecifications=[
            {
                'ResourceType': 'elastic-ip',
                'Tags': [
                    {'Key': 'Name', 'Value': 'EstateClassify-Static-IP'},
                    {'Key': 'Project', 'Value': 'EstateClassify-AI'}
                ]
            }
        ]
    )
    
    allocation_id = alloc_resp['AllocationId']
    public_ip = alloc_resp['PublicIp']
    print(f"Successfully allocated Elastic IP: {public_ip} (Allocation ID: {allocation_id})")

    print(f"Associating {public_ip} with EC2 instance {INSTANCE_ID}...")
    assoc_resp = ec2.associate_address(
        AllocationId=allocation_id,
        InstanceId=INSTANCE_ID
    )
    
    association_id = assoc_resp['AssociationId']
    print(f"Successfully associated! (Association ID: {association_id})")
    print(f"Permanent Static Public IP is now active: http://{public_ip}:8501")
    return public_ip, allocation_id

if __name__ == '__main__':
    allocate_and_associate_eip()
