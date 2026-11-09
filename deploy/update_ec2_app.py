import os
import sys
import subprocess
import tempfile
import boto3

INSTANCE_ID = "i-06ed6cd08216f604b"
REGION = "us-east-1"
OS_USER = "ubuntu"

def update_ec2():
    print(f"Connecting to EC2 {INSTANCE_ID} in {REGION}...")
    ec2 = boto3.client('ec2', region_name=REGION)
    ec2ic = boto3.client('ec2-instance-connect', region_name=REGION)

    # Get Public IP
    desc = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
    inst = desc['Reservations'][0]['Instances'][0]
    public_ip = inst.get('PublicIpAddress')
    az = inst['Placement']['AvailabilityZone']
    print(f"Target Public IP: {public_ip} (AZ: {az})")

    # Generate ephemeral SSH key pair
    temp_dir = tempfile.mkdtemp()
    key_path = os.path.join(temp_dir, "temp_id_rsa")
    pub_path = key_path + ".pub"

    keygen_cmd = f'ssh-keygen -t rsa -b 2048 -f "{key_path}" -N "" -q'
    subprocess.run(keygen_cmd, shell=True, check=True)

    with open(pub_path, "r") as f:
        pub_key = f.read().strip()

    print("Sending SSH public key via EC2 Instance Connect...")
    ec2ic.send_ssh_public_key(
        InstanceId=INSTANCE_ID,
        InstanceOSUser=OS_USER,
        SSHPublicKey=pub_key,
        AvailabilityZone=az
    )
    print("Key accepted for 60 seconds!")

    # Read local frontend/app.py and src/predict.py
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_app_path = os.path.join(project_root, "frontend", "app.py")
    local_predict_path = os.path.join(project_root, "src", "predict.py")
    
    with open(local_app_path, "r", encoding="utf-8") as f:
        app_content = f.read()
    with open(local_predict_path, "r", encoding="utf-8") as f:
        predict_content = f.read()

    ssh_opts = f'-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i "{key_path}"'

    print("Uploading updated app.py to EC2...")
    proc = subprocess.Popen(
        f'ssh {ssh_opts} {OS_USER}@{public_ip} "cat > /tmp/app_new.py"',
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate(input=app_content.encode("utf-8"))
    if proc.returncode != 0:
        print("SSH upload app.py failed:", stderr.decode())
        return False

    print("Uploading updated predict.py to EC2...")
    proc2 = subprocess.Popen(
        f'ssh {ssh_opts} {OS_USER}@{public_ip} "cat > /tmp/predict_new.py"',
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout2, stderr2 = proc2.communicate(input=predict_content.encode("utf-8"))
    if proc2.returncode != 0:
        print("SSH upload predict.py failed:", stderr2.decode())
        return False

    print("Installing updated files and restarting service...")
    cmd = (
        f'ssh {ssh_opts} {OS_USER}@{public_ip} '
        '"sudo mv /tmp/app_new.py /opt/estate-classify/frontend/app.py && '
        'sudo mv /tmp/predict_new.py /opt/estate-classify/src/predict.py && '
        'sudo chown -R root:root /opt/estate-classify/frontend /opt/estate-classify/src && '
        'sudo iptables -t nat -C PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8501 2>/dev/null || '
        'sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8501 && '
        'sudo systemctl restart estateclassify && '
        'sleep 2 && '
        'sudo systemctl status estateclassify --no-pager"'
    )
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("Service Status:")
    print(res.stdout)
    if res.stderr:
        print("Stderr:", res.stderr)

    # Cleanup temp keys
    try:
        os.remove(key_path)
        os.remove(pub_path)
        os.rmdir(temp_dir)
    except Exception:
        pass

    return res.returncode == 0

if __name__ == "__main__":
    success = update_ec2()
    print("Update status:", "SUCCESS" if success else "FAILED")
