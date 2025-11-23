### VIBE CODED BY CHATGPT AND GEMINI

# UPSNAP-AutoWOL
I think this is a niche tool but I thought I would share it. ChatGPT wrote the script a couple of years ago for me and I've been running it as a CRON  job on the machine hosting UpSnap.
This script will wait x minutes, then send WOL packets to everything in UpSnap.

## Requirements
* [UpSnap](https://github.com/seriousm4x/UpSnap)

### Configuration Variables

| Variable | Required | Description | Example |
| :--- | :---: | :--- | :--- |
| `UPSNAP_URL` | **Yes** | The base URL of your UpSnap instance. Do not include a trailing slash. Defaults to `http://localhost:8090` | `http://localhost:8090` |
| `UPSNAP_USERNAME` | **Yes** | The username used to log into UpSnap. | `admin` |
| `UPSNAP_PASSWORD` | **Yes** | The password associated with the username. | `secure_password_123` |
| `UPSNAP_DELAY` | No | The time to wait **(in minutes)** after the container starts before sending the Wake-on-LAN packets. Defaults to `0` if not set. | `5` |

### Heath Check
The healthcheck on the docker compose attempts to connect to the UpSnap server from the scripts container. If the container is marked as unhealthy, it is likely that you need to provide the server address or you have provided bad data

## How I use this
I have a Dell Wyse 5070 plugged directly into mains power running UpSnap, among some other things. The rest of my infrastructure is behind a UPS.
The workflow is
1. Power goes out, the machine hosting UpSnap and this script are powered off
2. Power comes back and the machine hosting UpSnap and this script and automatically powered on
3. The script waits x minutes, per the environmental variable, then sends WOL packets to everything in UpSnap

### Why is it set up like this?
Generally speaking, when I have 1 power outage there will be a power outage or 2 afterwards. Eg my power will return for a minute, then get switched off again.
I do not want my servers booting back up during this time. I have my servers set to do nothing when the power is returned, while the UpSnap server will autoboot when it gets power.

Waiting x minutes also allows the UPS battery to get some charge before the servers start drawing from it.

## Script Workflow
1. Checks if it can reach the UpSnap URL
2. Attempts to authenticate
3. Sends WOL packets to all devices
4. Script goes to sleep
The script is required to sleep to ensure it automatically runs on boot
