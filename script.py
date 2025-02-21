import os
import json
import zipfile
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
LUCIDCHART_API_KEY = os.getenv("LUCIDCHART_API_KEY")

# Create a shape inside Lucidchart
def create_lucidchart_import():
    lucidchart_json = {
        "version": 1,
        "pages": [
            {
                "id": "page1",
                "title": "Shape Example",
                "shapes": [
                    {
                        "id": "shape1",
                        "type": "rectangle",  # ✅ Correct type
                        "boundingBox": {  # ✅ Required bounding box
                            "x": 100,
                            "y": 100,
                            "w": 200,
                            "h": 100
                        },
                        "style": {
                            "fill": {"type": "color", "color": "#00FF00"},
                            "stroke": {"color": "#000000", "width": 1, "style": "solid"}
                        },
                        "text": "My Shape"
                    }
                ]
            }
        ]
    }

    # Save JSON to document.json
    with open("document.json", "w") as json_file:
        json.dump(lucidchart_json, json_file)

    # Zip the file to create a .lucid ZIP file
    with zipfile.ZipFile("document.lucid", "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write("document.json")

    return "document.lucid"

# ✅ Step 2: Import the file to Lucidchart
def import_to_lucidchart(updated=False):
    # Step 1: Generate new .lucid file
    lucid_file = add_new_shape()  # Generates new shapes and saves as document.lucid

    url = "https://api.lucid.co/documents"
    headers = {
        "Authorization": f"Bearer {LUCIDCHART_API_KEY}",
        "Lucid-Api-Version": "1"
    }
    files = {
        "file": ("document.lucid", open(lucid_file, "rb"), "x-application/vnd.lucid.standardImport"),
        "product": (None, "lucidchart"),
        "title": (None, "Updated ERD Diagram" if updated else "Shape Example")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 201:
        document_id = response.json()["documentId"]
        print(f"✅ {'Updated' if updated else 'New'} document imported successfully! Document ID: {document_id}")
        return document_id
    else:
        print(f"❌ Error importing document: {response.text}")
        return None


def open_lucidchart_document(document_id):
    lucidchart_url = f"https://lucid.app/lucidchart/{document_id}/edit"
    print(f"🌍 Open your document here: {lucidchart_url}")


def add_new_shape():
    lucidchart_json = {
        "version": 1,
        "pages": [
            {
                "id": "page1",
                "title": "Updated Diagram",
                "shapes": [
                    # Existing Shape
                    {
                        "id": "shape1",
                        "type": "rectangle",
                        "boundingBox": {"x": 100, "y": 100, "w": 200, "h": 100},
                        "style": {
                            "fill": {"type": "color", "color": "#00FF00"},
                            "stroke": {"color": "#000000", "width": 1, "style": "solid"}
                        },
                        "text": "My Shape"
                    },
                    # ✅ New Shape Added
                    {
                        "id": "shape2",
                        "type": "rectangle",
                        "boundingBox": {"x": 400, "y": 100, "w": 200, "h": 100},
                        "style": {
                            "fill": {"type": "color", "color": "#FF0000"},
                            "stroke": {"color": "#000000", "width": 1, "style": "solid"}
                        },
                        "text": "New Shape"
                    }
                ]
            }
        ]
    }

    # Save JSON to document.json
    with open("document.json", "w") as json_file:
        json.dump(lucidchart_json, json_file)

    # Zip to .lucid format
    with zipfile.ZipFile("document.lucid", "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write("document.json")

    return "document.lucid"


# Run the function
if __name__ == "__main__":
    print("🔄 Re-importing updated document...")
    new_document_id = import_to_lucidchart(updated=True)

    if new_document_id:
        print(f"🌍 Open the updated document: https://lucid.app/lucidchart/{new_document_id}/edit")

