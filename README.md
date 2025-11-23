# UPSNAP-AutoWOL
I think this is a niche tool but I thought I would share it. ChatGPT wrote the script a couple of years ago for me and I've been running it as a CRON  job on the machine hosting UpSnap.
This script will wait x minutes, then send WOL packets to everything in UpSnap.

## Requirements
* [UpSnap](https://github.com/seriousm4x/UpSnap)

## How I use this
I have a Dell Wyse 5070 plugged directly into mains power running UpSnap, among some other things. The rest of my infrastructure is behind a UPS.
The workflow is
1. Power goes out, the machine hosting UpSnap and this script are powered off
2. Power comes back and the machine hosting UpSnap and this script and automatically powered on
3. The script waits x minutes, per the environmental variable, then sends WOL packets to everything in UpSnap

### Why is it set up like this?
Generally speaking, when I have 1 power outage there will be a power outage or 2 afterwards. Eg my power will return for a minute, then get switched off again.
I do not want my servers booting back up during this time. Waiting x minutes also allows the UPS battery to get some charge before the servers start drawing from it.
