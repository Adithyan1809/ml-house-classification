"""
AWS EC2 Instance Management Helper for EstateClassify AI
Allows simple command-line starting, stopping, and status checks.
"""

import sys
import boto3

INSTANCE_ID = "i-06ed6cd08216f604b"
REGION = "us-east-1"
STATIC_IP = "3.211.54.86"

def get_ec2_client():
    return boto3.client('ec2', region_name=REGION)

def status():
    ec2 = get_ec2_client()
    desc = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
    inst = desc['Reservations'][0]['Instances'][0]
    state = inst['State']['Name']
    print(f"EC2 Instance {INSTANCE_ID}:")
    print(f"  - Current State: {state.upper()}")
    print(f"  - Permanent Static IP: {STATIC_IP}")
    if state == "running":
        print(f"  - Live URL: http://{STATIC_IP}:8501 (or http://{STATIC_IP})")
    return state

def start():
    ec2 = get_ec2_client()
    print(f"Starting instance {INSTANCE_ID}...")
    ec2.start_instances(InstanceIds=[INSTANCE_ID])
    print("Start signal sent! Waiting for running status...")
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[INSTANCE_ID])
    print(f"Instance is now RUNNING!")
    print(f"Your static URL is active: http://{STATIC_IP}:8501")

def stop():
    ec2 = get_ec2_client()
    print(f"Stopping instance {INSTANCE_ID}...")
    ec2.stop_instances(InstanceIds=[INSTANCE_ID])
    print("Stop signal sent! Instance is shutting down gracefully.")

if __name__ == "__main__":
    action = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    if action == "start":
        start()
    elif action == "stop":
        stop()
    else:
        status()
