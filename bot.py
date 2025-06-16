import requests

response = requests.get("https://tibiaroute.com")
print("✅ Response received!")
print(response.text[:1000])  # Print first 1000 characters
