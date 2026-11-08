"""
Automated AWS EC2 Deployment Script for EstateClassify AI
Provisions an EC2 instance, configures Security Group (ports 80, 8501),
and launches the Streamlit ML application using cloud-init.
"""

import os
import sys
import time
import zipfile
import boto3
from botocore.exceptions import ClientError

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REGION = "us-east-1"
INSTANCE_TYPE = "t2.micro" # Free Tier eligible
SECURITY_GROUP_NAME = "estate-classify-web-sg"
S3_BUCKET_NAME = "ironlock-networksecurity-2026"
S3_KEY = "estate-classify/app.zip"

def create_project_zip(output_zip: str = "deploy/app.zip"):
    """Creates a deployment zip bundle including code, models, and config."""
    print(f"📦 Packaging application into {output_zip}...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    ignore_dirs = {".git", ".github", "venv", "env", "__pycache__", ".pytest_cache"}
    
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file.endswith((".pyc", ".zip", ".log")):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, project_root)
                zf.write(full_path, rel_path)
    
    print(f" Zip bundle created ({os.path.getsize(output_zip) / (1024*1024):.2f} MB)")
    return output_zip

def get_or_create_security_group(ec2_client, vpc_id: str) -> str:
    """Finds or creates the security group with ports 8501 and 80 open."""
    try:
        response = ec2_client.describe_security_groups(
            Filters=[
                {"Name": "group-name", "Values": [SECURITY_GROUP_NAME]},
                {"Name": "vpc-id", "Values": [vpc_id]}
            ]
        )
        if response["SecurityGroups"]:
            sg_id = response["SecurityGroups"][0]["GroupId"]
            print(f" Reusing existing Security Group: {sg_id} ({SECURITY_GROUP_NAME})")
            return sg_id
    except ClientError as e:
        print(f"Notice during SG lookup: {e}")

    print(f"🔨 Creating Security Group '{SECURITY_GROUP_NAME}' in VPC {vpc_id}...")
    sg_resp = ec2_client.create_security_group(
        GroupName=SECURITY_GROUP_NAME,
        Description="Security group for EstateClassify ML Web Application",
        VpcId=vpc_id
    )
    sg_id = sg_resp["GroupId"]

    # Authorize ports 8501 (Streamlit), 80 (HTTP), and 22 (SSH)
    ip_permissions = [
        {
            "IpProtocol": "tcp", "FromPort": 8501, "ToPort": 8501,
            "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "Streamlit Web App"}]
        },
        {
            "IpProtocol": "tcp", "FromPort": 80, "ToPort": 80,
            "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "HTTP Web Port"}]
        },
        {
            "IpProtocol": "tcp", "FromPort": 22, "ToPort": 22,
            "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "SSH Admin"}]
        }
    ]
    ec2_client.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=ip_permissions
    )
    print(f" Security Group configured with inbound ports 8501, 80, 22.")
    return sg_id

def get_latest_ami(ec2_client) -> str:
    """Retrieves the latest official Ubuntu 22.04 Jammy LTS AMI in region."""
    response = ec2_client.describe_images(
        Filters=[
            {"Name": "name", "Values": ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]},
            {"Name": "virtualization-type", "Values": ["hvm"]},
            {"Name": "state", "Values": ["available"]}
        ],
        Owners=["099720109477"] # Canonical
    )
    images = sorted(response["Images"], key=lambda x: x["CreationDate"], reverse=True)
    if not images:
        # Fallback to standard AL2023 or known Ubuntu AMI
        return "ami-0c7217cdde317cfec"
    latest_ami = images[0]["ImageId"]
    print(f" Latest Ubuntu 22.04 AMI found: {latest_ami}")
    return latest_ami

def deploy_to_ec2():
    print(f"\n🚀 Initiating AWS EC2 Deployment in {REGION}...")
    ec2 = boto3.client("ec2", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)

    # 1. Package and upload to S3
    zip_path = create_project_zip()
    presigned_url = None
    try:
        print(f"📤 Uploading {zip_path} to s3://{S3_BUCKET_NAME}/{S3_KEY}...")
        s3.upload_file(zip_path, S3_BUCKET_NAME, S3_KEY)
        print(" S3 upload successful.")
        # Generate presigned download URL valid for 2 hours
        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET_NAME, "Key": S3_KEY},
            ExpiresIn=7200
        )
        print(f" Presigned deployment package URL generated.")
    except Exception as e:
        print(f"⚠️ S3 upload note: {e}")

    # 2. Get Default VPC
    vpcs = ec2.describe_vpcs(Filters=[{"Name": "isDefault", "Values": ["true"]}])
    if not vpcs["Vpcs"]:
        raise RuntimeError("No default VPC found in region.")
    vpc_id = vpcs["Vpcs"][0]["VpcId"]
    print(f" Using Default VPC: {vpc_id}")

    # 3. Security Group
    sg_id = get_or_create_security_group(ec2, vpc_id)

    # 4. AMI
    ami_id = get_latest_ami(ec2)

    # 5. Cloud-init user-data script
    download_cmd = f'curl -s -L "{presigned_url}" -o app.zip' if presigned_url else 'echo "No presigned URL"'

    user_data_script = f"""#!/bin/bash
exec > /var/log/user-data.log 2>&1
set -e
echo "Starting cloud initialization at $(date)..."

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3-pip python3-venv git unzip curl

mkdir -p /opt/estate-classify
cd /opt/estate-classify

# Download deployment package via presigned S3 URL
echo "Downloading application package..."
{download_cmd}

if [ -f app.zip ]; then
    echo "Extracting app.zip..."
    unzip -o app.zip
fi

echo "Setting up Python virtual environment..."
python3 -m venv /opt/estate-classify/venv
/opt/estate-classify/venv/bin/pip install --upgrade pip
/opt/estate-classify/venv/bin/pip install -r requirements.txt

echo "Registering systemd service..."
cat << 'EOF' > /etc/systemd/system/estateclassify.service
[Unit]
Description=EstateClassify Streamlit ML Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/estate-classify
ExecStart=/opt/estate-classify/venv/bin/streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable estateclassify
systemctl start estateclassify
echo "Application started successfully on port 8501 at $(date)!"
"""

    # 6. Launch Instance
    print(f"⚡ Launching EC2 instance ({INSTANCE_TYPE})...")
    run_response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=INSTANCE_TYPE,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[sg_id],
        UserData=user_data_script,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": "EstateClassify-ML-Server"},
                    {"Key": "Project", "Value": "EstateClassify-AI"}
                ]
            }
        ]
    )

    instance_id = run_response["Instances"][0]["InstanceId"]
    print(f" Instance launched: {instance_id}")
    print("⏳ Waiting for instance to transition to 'running' state...")

    waiter = ec2.get_waiter("instance_running")
    waiter.wait(InstanceIds=[instance_id])

    # 7. Get Public IP
    desc_resp = ec2.describe_instances(InstanceIds=[instance_id])
    inst = desc_resp["Reservations"][0]["Instances"][0]
    public_ip = inst.get("PublicIpAddress", "Pending")
    public_dns = inst.get("PublicDnsName", "Pending")

    print("\n" + "="*60)
    print(" 🎉 AWS EC2 DEPLOYMENT SUCCESSFUL!")
    print("="*60)
    print(f" Instance ID:   {instance_id}")
    print(f" Region:        {REGION}")
    print(f" Instance Type: {INSTANCE_TYPE}")
    print(f" Public IPv4:   {public_ip}")
    print(f" Public DNS:    {public_dns}")
    print(f"\n🌐 Live Application URL: http://{public_ip}:8501")
    print("="*60)
    print("Note: Please allow 2-3 minutes for cloud-init package installation.")
    return {
        "instance_id": instance_id,
        "public_ip": public_ip,
        "public_dns": public_dns,
        "app_url": f"http://{public_ip}:8501"
    }

if __name__ == "__main__":
    deploy_to_ec2()
