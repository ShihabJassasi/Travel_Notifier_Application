import requests
import json
import config
import os, datetime as dt
from dotenv import load_dotenv

from db import insert

from notifier import send_slack




load_dotenv() 

url = "https://routes.googleapis.com/directions/v2:computeRoutes"

#source_address = config.source
#destination_address = config.destination


payload = json.dumps({
  "origin": {
    "address": config.source
  },
  "destination": {
    "address": config.destination
  },
  "travelMode": "DRIVE",
  "routingPreference": "TRAFFIC_AWARE"
})
headers = {
  'Content-Type': 'application/json',
  'X-Goog-Api-Key':os.getenv("google_api_key"),
  'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters'
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)
 
data = response.json()
route = data["routes"][0]

distance_meters = route["distanceMeters"]
duration_seconds = int(route["duration"].replace("s", ""))


distance_km = distance_meters / 1000
duration_minutes = duration_seconds / 60



print(f"Distance: {distance_km:.2f} km")
print(f"Duration: {duration_minutes:.1f} minutes")
insert(duration_minutes, distance_km)
print("✅ Saved to DB")

if send_slack(f" Notification ⚠️ : You will take arround {distance_km:.2f} km and  {duration_minutes:.1f} min to reach from {config.source} to {config.destination}"):
    print("Slack notified ✅")
else:
    print("Slack failed ❌")
