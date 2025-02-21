import requests
import json
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
LUCIDCHART_API_KEY = os.getenv("LUCIDCHART_API_KEY")
headers = {
    'Authorization': f'Bearer {LUCIDCHART_API_KEY}',
    'Content-Type': 'application/json'
}

url = 'https://api.lucidchart.com/v1/documents'
data = {
    "title": "My First Diagram",
    "description": "Created via API"
}

response = requests.post(url, headers=headers, json=data)

# Print the status code and full response JSON for inspection
print("Status Code:", response.status_code)
try:
    response_json = response.json()
    # print("Response JSON:")
    # print(json.dumps(response_json, indent=2))
    
    # Try to extract the diagram ID from common keys
    diagram_id = response_json.get('documentId')
    if diagram_id:
        print("Diagram created successfully! ID:", diagram_id)
    else:
        print("Diagram created, but no ID found in response.")
except Exception as e:
    print("Error parsing response JSON:", str(e))