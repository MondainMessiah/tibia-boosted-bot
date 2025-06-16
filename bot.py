import requests

print("🔍 Fetching TibiaRoute HTML...")
response = requests.get("https://tibiaroute.com")

if response.status_code == 200:
    print("✅ Response received!")
    print(response.text[:1000])  # Print first 1000 chars
else:
    print(f"❌ Failed to load page. Status code: {response.status_code}")
