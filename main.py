import requests
import time
import argparse
import sys

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="UpSnap Wake-on-LAN Automation Script")
    
    parser.add_argument(
        "--url", 
        required=True, 
        help="The base URL of the UpSnap instance (e.g., http://localhost:8090)"
    )
    
    parser.add_argument(
        "--username", 
        required=True, 
        help="The username for authentication"
    )
    
    parser.add_argument(
        "--password", 
        required=True, 
        help="The password for authentication"
    )
    
    parser.add_argument(
        "--delay", 
        type=int, 
        required=True, 
        help="Time to wait in seconds before running (e.g., 600 for 10 minutes)"
    )

    return parser.parse_args()

# Function to authenticate and get token
def authenticate(base_url, username, password):
    print("Authenticating...")
    auth_url = f"{base_url}/api/collections/users/auth-with-password"
    auth_data = {"identity": username, "password": password}
    try:
        response = requests.post(auth_url, json=auth_data)
        response.raise_for_status()
        return response.json().get("token")
    except requests.RequestException as e:
        print(f"Error during authentication: {e}")
        return None

# Function to get all devices
def get_devices(base_url, token):
    print("Getting list of devices...")
    headers = {'Authorization': f'Bearer {token}'}
    devices_url = f"{base_url}/api/collections/devices/records"
    try:
        response = requests.get(devices_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving devices: {e}")
        return None

# Function to send WOL packet
def wake_device(base_url, token, device_id):
    print(f"Sending WOL packet to device {device_id}...")
    headers = {'Authorization': f'Bearer {token}'}
    wake_url = f"{base_url}/api/upsnap/wake/{device_id}"
    try:
        response = requests.get(wake_url, headers=headers)
        response.raise_for_status()
        print(f"WOL packet sent successfully to device {device_id}.")
    except requests.RequestException as e:
        print(f"Error sending WOL packet to device {device_id}: {e}")

# Main script
def main():
    # Parse switches
    args = parse_arguments()

    print(f"Script started. Waiting for {args.delay} seconds...")
    time.sleep(args.delay)

    # Authenticate using provided args
    token = authenticate(args.url, args.username, args.password)

    if token:
        # Get devices using provided args
        devices = get_devices(args.url, token)
        if devices:
            for device in devices.get("items", []):
                wake_device(args.url, token, device.get("id")) 

if __name__ == "__main__":
    main()
