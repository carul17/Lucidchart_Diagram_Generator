import os
import json
import zipfile
import requests
from dotenv import load_dotenv
import uuid

# Load API key
load_dotenv()
LUCIDCHART_API_KEY = os.getenv("LUCIDCHART_API_KEY")

# Global storage for shapes and lines
shapes = []
lines = []

### 🚀 Create a Shape Dynamically ###
def create_shape(name, x, y, shape_type="rectangle", width=200, height=100, color="#00FF00", extra_properties=None):
    """Create a shape with a specified type, position, size, and color."""
    
    # Ensure the shape type is valid
    valid_shapes = {
        "rectangle", "circle", "cloud", "cross", "diamond", "doubleArrow", 
        "flexiblePolygon", "hexagon", "isoscelesTriangle", "octagon", 
        "pentagon", "polyStar", "rightTriangle", "singleArrow"
    }

    if shape_type not in valid_shapes:
        raise ValueError(f"❌ Invalid shape type: {shape_type}. Must be one of {valid_shapes}.")

    shape_id = f"shape_{uuid.uuid4().hex[:8]}"  # Unique ID

    shape = {
        "id": shape_id,
        "type": shape_type,  # ✅ Shape type is dynamic
        "boundingBox": {"x": x, "y": y, "w": width, "h": height},
        "style": {
            "fill": {"type": "color", "color": color},
            "stroke": {"color": "#000000", "width": 1, "style": "solid"}
        },
        "text": name
    }

    # Add extra properties (e.g., star points, arrow direction, etc.)
    if extra_properties:
        shape.update(extra_properties)

    shapes.append(shape)  # Store the shape
    return shape_id  # Return shape ID for reference



def create_container(name, x, y, container_type="rectangleContainer", width=400, height=200, color="#D3D3D3", magnetize=True, extra_properties=None):
    """
    Create a container with specified type, position, size, and color.

    Supported container types:
    - "braceContainer"
    - "bracketContainer"
    - "circleContainer"
    - "diamondContainer"
    - "pillContainer"
    - "rectangleContainer"
    - "roundedRectangleContainer"
    - "swimLanes"
    """

    # Ensure valid container type
    valid_containers = {
        "braceContainer", "bracketContainer", "circleContainer", "diamondContainer",
        "pillContainer", "rectangleContainer", "roundedRectangleContainer", "swimLanes"
    }

    if container_type not in valid_containers:
        raise ValueError(f"❌ Invalid container type: {container_type}. Must be one of {valid_containers}.")

    container_id = f"container_{uuid.uuid4().hex[:8]}"  # Generate unique ID

    container = {
        "id": container_id,
        "type": container_type,
        "boundingBox": {"x": x, "y": y, "w": width, "h": height},
        "style": {
            "fill": {"type": "color", "color": color},
            "stroke": {"color": "#000000", "width": 1, "style": "solid"}
        },
        "text": name,
        "magnetize": magnetize
    }

    # Handle Swim Lanes (special properties)
    if container_type == "swimLanes":
        container["vertical"] = False  # Default to horizontal swim lanes
        container["titleBar"] = {
            "height": 50,
            "verticalText": False
        }
        container["lanes"] = [
            {
                "title": "Lane 1",
                "width": width // 2,
                "headerFill": "#635DFF",
                "laneFill": "#F2F3F5"
            },
            {
                "title": "Lane 2",
                "width": width // 2,
                "headerFill": "#FF6347",
                "laneFill": "#F2F3F5"
            }
        ]

    # Add extra properties if provided (e.g., swim lanes customization)
    if extra_properties:
        container.update(extra_properties)

    shapes.append(container)  # Store the container as part of shapes
    return container_id  # Return the container ID for reference



### 🚀 Create a Line Dynamically ###
def create_line(shape1_id, shape2_id, relationship="relationship", line_type="one-to-one"):
    line_id = f"line_{uuid.uuid4().hex[:8]}"  # ✅ Truncate UUID to 8 characters

    # Define line endings based on type
    endpoint_styles = {
        "one-to-one": ("one", "one"),
        "one-to-many": ("one", "many"),
        "many-to-one": ("many", "one"),
        "many-to-many": ("many", "many")
    }
    
    start_style, end_style = endpoint_styles.get(line_type, ("none", "none"))

    line = {
        "id": line_id,
        "lineType": "straight",
        "endpoint1": {
            "type": "shapeEndpoint",
            "style": start_style,
            "shapeId": shape1_id,
            "position": {"x": 1, "y": 0.5}
        },
        "endpoint2": {
            "type": "shapeEndpoint",
            "style": end_style,
            "shapeId": shape2_id,
            "position": {"x": 0, "y": 0.5}
        },
        "stroke": {
            "color": "#000000",
            "width": 2,
            "style": "solid"
        },
        "text": [
            {
                "text": relationship,
                "position": 0.5,
                "side": "middle"
            }
        ]
    }
    lines.append(line)
    return line_id


### 🚀 Generate Lucidchart JSON ###
def generate_lucidchart_json():
    return {
        "version": 1,
        "pages": [
            {
                "id": "page1",
                "title": "Dynamic Diagram",
                "shapes": shapes,  # Use stored shapes
                "lines": lines  # Use stored lines
            }
        ]
    }

### 🚀 Save JSON and Create `.lucid` File ###
def save_lucidchart_file():
    lucidchart_json = generate_lucidchart_json()
    
    with open("document.json", "w") as json_file:
        json.dump(lucidchart_json, json_file)

    with zipfile.ZipFile("document.lucid", "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write("document.json")

    return "document.lucid"

### 🚀 Import the File to Lucidchart ###
def import_to_lucidchart():
    lucid_file = save_lucidchart_file()

    url = "https://api.lucid.co/documents"
    headers = {
        "Authorization": f"Bearer {LUCIDCHART_API_KEY}",
        "Lucid-Api-Version": "1"
    }
    files = {
        "file": ("document.lucid", open(lucid_file, "rb"), "x-application/vnd.lucid.standardImport"),
        "product": (None, "lucidchart"),
        "title": (None, "Dynamic Diagram")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 201:
        document_id = response.json()["documentId"]
        print(f"✅ Document imported successfully! Document ID: {document_id}")
        return document_id
    else:
        print(f"❌ Error importing document: {response.text}")
        return None


def main():
    print("🛠️ Creating dynamic containers and relationships...")

    # ✅ Create Various Containers
    container1 = create_container("Main Group", x=50, y=50, container_type="rectangleContainer", color="#B0E0E6")
    container2 = create_container("Feature Set", x=500, y=50, container_type="roundedRectangleContainer", color="#FFD700")
    container3 = create_container("Validation", x=50, y=300, container_type="diamondContainer", color="#FF6347")
    container4 = create_container("Approval Process", x=500, y=300, container_type="pillContainer", color="#90EE90")

    # ✅ Create Swim Lane Container (Special)
    swimlane = create_container("Workflow", x=100, y=500, container_type="swimLanes", width=600, height=300,
                                extra_properties={"vertical": True})

    # ✅ Create Relationships Between Containers
    create_line(container1, container2, relationship="includes", line_type="one-to-many")
    create_line(container2, container3, relationship="requires", line_type="one-to-one")
    create_line(container3, container4, relationship="validates", line_type="many-to-one")
    create_line(container4, swimlane, relationship="flows into", line_type="many-to-many")

    # ✅ Import to Lucidchart
    document_id = import_to_lucidchart()
    
    if document_id:
        print(f"🌍 Open the Lucidchart document: https://lucid.app/lucidchart/{document_id}/edit")

if __name__ == "__main__":
    main()
