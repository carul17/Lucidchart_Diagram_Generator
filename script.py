import requests
import json

api_key = 'api-key'
headers = {
    'Authorization': f'Bearer {api_key}',
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