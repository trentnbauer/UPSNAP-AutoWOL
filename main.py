import requests
import time
import os
import sys

# Load Environment Variables
UPSNAP_URL = os.getenv("UPSNAP_URL")
UPSNAP_USERNAME = os.getenv("UPSNAP_USERNAME")
UPSNAP_PASSWORD = os.getenv("UPSNAP_PASSWORD")

# Default to 0 minutes (run immediately) if not set
DELAY_MINUTES = int(os.getenv("UPSNAP_DELAY", "0")) 

# Check for required variables
if not all([UPSNAP_URL, UPSNAP_USERNAME, UPSNAP_PASSWORD]):
    print("❌ Error: Missing required environment variables.", flush=True)
    sys.exit(1)

def authenticate():
    print("🔐 Authenticating...", flush=True)
    auth_url = f"{UPSNAP_URL}/api/collections/users/auth-with-password"
    auth_data = {"identity": UPSNAP_USERNAME, "password": UPSNAP_PASSWORD}
    try:
        response = requests.post(auth_url, json=auth_data)
        response.raise_for_status()
        return response.json().get("token")
    except requests.RequestException as e:
        print(f"Error during authentication: {e}", flush=True)
        return None

def get_devices(token):
    print("📃 Getting list of devices...", flush=True)
    headers = {'Authorization': f'Bearer {token}'}
    devices_url = f"{UPSNAP_URL}/api/collections/devices/records"
    try:
        response = requests.get(devices_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving devices: {e}", flush=True)
        return None

def wake_device(token, device_id):
    print(f"📨 Sending WOL packet to device {device_id}...", flush=True)
    headers = {'Authorization': f'Bearer {token}'}
    wake_url = f"{UPSNAP_URL}/api/upsnap/wake/{device_id}"
    try:
        response = requests.get(wake_url, headers=headers)
        response.raise_for_status()
        print(f"📬 WOL packet sent successfully to device {device_id}.", flush=True)
    except requests.RequestException as e:
        print(f"🧯 Error sending WOL packet to device {device_id}: {e}", flush=True)

def main():
    # 1. Initial Delay
    if DELAY_MINUTES > 0:
        print(f"⌛ Script started. Waiting for {DELAY_MINUTES} minutes...", flush=True)
        time.sleep(DELAY_MINUTES * 60)
    else:
        print("🏃‍➡️ Script started. Running immediately...", flush=True)

    # 2. Run the Logic
    token = authenticate()

    if token:
        devices = get_devices(token)
        if devices:
            for device in devices.get("items", []):
                wake_device(token, device.get("id"))
    
    # 3. Idle Forever
    # This keeps the container "Running" so Docker doesn't restart it.
    # It will only run again if the container is manually restarted or the machine reboots.
    print("🛏️ Task complete. Entering idle mode.", flush=True)
    while True:
        time.sleep(3600) # Sleep for 1 hour blocks to consume 0 CPU

if __name__ == "__main__":
    main()
