import requests
import time
import os
import sys

# Load Environment Variables
UPSNAP_URL = os.getenv("UPSNAP_URL")
UPSNAP_USERNAME = os.getenv("UPSNAP_USERNAME")
UPSNAP_PASSWORD = os.getenv("UPSNAP_PASSWORD")

# Default to 10 minutes if not set
DELAY_MINUTES = int(os.getenv("UPSNAP_DELAY", "10")) 

# specific check to ensure variables exist
if not all([UPSNAP_URL, UPSNAP_USERNAME, UPSNAP_PASSWORD]):
    print("Error: Missing required environment variables.")
    print("Please set UPSNAP_URL, UPSNAP_USERNAME, and UPSNAP_PASSWORD.")
    sys.exit(1)

def authenticate():
    print("Authenticating...")
    auth_url = f"{UPSNAP_URL}/api/collections/users/auth-with-password"
    auth_data = {"identity": UPSNAP_USERNAME, "password": UPSNAP_PASSWORD}
    try:
        response = requests.post(auth_url, json=auth_data)
        response.raise_for_status()
        return response.json().get("token")
    except requests.RequestException as e:
        print(f"Error during authentication: {e}")
        return None

def get_devices(token):
    print("Getting list of devices...")
    headers = {'Authorization': f'Bearer {token}'}
    devices_url = f"{UPSNAP_URL}/api/collections/devices/records"
    try:
        response = requests.get(devices_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving devices: {e}")
        return None

def wake_device(token, device_id):
    print(f"Sending WOL packet to device {device_id}...")
    headers = {'Authorization': f'Bearer {token}'}
    wake_url = f"{UPSNAP_URL}/api/upsnap/wake/{device_id}"
    try:
        response = requests.get(wake_url, headers=headers)
        response.raise_for_status()
        print(f"WOL packet sent successfully to device {device_id}.")
    except requests.RequestException as e:
        print(f"Error sending WOL packet to device {device_id}: {e}")

def main():
    print(f"Script started. Waiting for {DELAY_MINUTES} minutes...")
    
    # Convert minutes to seconds for time.sleep()
    time.sleep(DELAY_MINUTES * 60) 

    token = authenticate()

    if token:
        devices = get_devices(token)
        if devices:
            for device in devices.get("items", []):
                wake_device(token, device.get("id")) 

if __name__ == "__main__":
    main()
