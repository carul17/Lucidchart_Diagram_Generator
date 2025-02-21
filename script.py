import os
import json
import zipfile
import requests
from dotenv import load_dotenv
import uuid
import re

# Load API key
load_dotenv()
LUCIDCHART_API_KEY = os.getenv("LUCIDCHART_API_KEY")

# Global storage for shapes and lines
shapes = []
lines = []

### 🚀 Create a Shape Dynamically ###


# Standard color name to hex mapping
COLOR_MAP = {
    "red": "#FF0000",
    "blue": "#0000FF",
    "green": "#00FF00",
    "yellow": "#FFFF00",
    "black": "#000000",
    "white": "#FFFFFF",
    "gray": "#808080",
    "purple": "#800080",
    "cyan": "#00FFFF",
    "magenta": "#FF00FF"
}

def validate_hex_color(color):
    """Ensure the color is in a valid hex format or convert color names to hex."""
    hex_pattern = r'^#(?:[0-9a-fA-F]{3,4}){1,2}$'

    # If color is a named color, convert it to hex
    if color.lower() in COLOR_MAP:
        return COLOR_MAP[color.lower()]

    # Check if color is a valid hex code
    if re.match(hex_pattern, color):
        return color

    # Invalid color → Default to black
    print(f"⚠️ Invalid color `{color}`. Defaulting to black (#000000).")
    return "#000000"

def create_shape(name, x, y, shape_type="rectangle", width=200, height=100, color="#00FF00", extra_properties=None):
    """Create a shape with a specified type, position, size, and color."""
    
    color = validate_hex_color(color)  # ✅ Fix color before using it

    shape_id = f"shape_{uuid.uuid4().hex[:8]}"  # Unique ID

    shape = {
        "id": shape_id,
        "type": shape_type,  
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


def create_flowchart_element(name, x, y, flowchart_type="process", width=200, height=100, color="#ADD8E6", extra_properties=None):
    """
    Create a flowchart element with specified type, position, size, and color.

    Supported flowchart types:
    - "braceNote"
    - "connector"
    - "database"
    - "data"
    - "decision"
    - "delay"
    - "display"
    - "document"
    - "manualInput"
    - "manualOperation"
    - "merge"
    - "process"
    - "storedData"
    - "terminator"
    """

    valid_flowchart_types = {
        "braceNote", "connector", "database", "data", "decision", "delay", 
        "display", "document", "manualInput", "manualOperation", "merge", 
        "process", "storedData", "terminator"
    }

    if flowchart_type not in valid_flowchart_types:
        raise ValueError(f"❌ Invalid flowchart type: {flowchart_type}. Must be one of {valid_flowchart_types}.")

    element_id = f"flowchart_{uuid.uuid4().hex[:8]}"  # Generate a unique ID

    flowchart_element = {
        "id": element_id,
        "type": flowchart_type,
        "boundingBox": {"x": x, "y": y, "w": width, "h": height},
        "style": {
            "fill": {"type": "color", "color": color},
            "stroke": {"color": "#000000", "width": 1, "style": "solid"}
        },
        "text": name
    }

    # Handle special cases like Brace Note
    if flowchart_type == "braceNote":
        flowchart_element["rightFacing"] = False  # Default to left-facing
        flowchart_element["braceWidth"] = 60  # Default width

    # Add extra properties if needed
    if extra_properties:
        flowchart_element.update(extra_properties)

    shapes.append(flowchart_element)  # Store the flowchart element
    return element_id  # Return the ID for reference


def create_table(name, x, y, rows=3, cols=2, width=300, height=200, color="#FFFFFF", cell_data=None):
    """
    Create a valid square table by adding extra cells to make `rows == cols`.
    """

    # 🔥 Force square table (make rows = cols by adding empty cells)
    max_dim = max(rows, cols)  # Find the larger dimension
    rows, cols = max_dim, max_dim  # Force table to be square

    table_id = f"table_{uuid.uuid4().hex[:8]}"  # Unique ID

    table = {
        "id": table_id,
        "type": "table",
        "boundingBox": {"x": x, "y": y, "w": width, "h": height},
        "style": {
            "fill": {"type": "color", "color": color},
            "stroke": {"color": "#000000", "width": 1, "style": "solid"}
        },
        "rowCount": rows,
        "colCount": cols,
        "cells": [],
        "verticalBorder": True,
        "horizontalBorder": True
    }

    # ✅ Populate table cells
    for r in range(rows):
        for c in range(cols):
            cell_text = ""
            cell_color = "#FFFFFF"
            merge_right = 0
            merge_down = 0

            if cell_data:
                for cell in cell_data:
                    if cell["x"] == c and cell["y"] == r:
                        cell_text = cell.get("text", "")
                        cell_color = cell.get("color", "#FFFFFF")
                        merge_right = cell.get("merge_right", 0)
                        merge_down = cell.get("merge_down", 0)
                        break

            # ✅ If cell is outside original dimensions, make it "hidden"
            if c >= cols or r >= rows:
                cell_text = ""
                merge_right = 0
                merge_down = 0

            table["cells"].append({
                "xPosition": c,
                "yPosition": r,
                "mergeCellsRight": merge_right,
                "mergeCellsDown": merge_down,
                "text": cell_text,
                "style": {"fill": {"type": "color", "color": cell_color}}
            })

    shapes.append(table)  # Store table
    return table_id  # Return the table ID


def create_standard_shape(shape_type, name, x, y, width=200, height=100, text=None, image_url=None, color="#FFFFFF"):
    """
    Create a standard shape from Lucidchart's standard library.
    
    - `shape_type`: Type of shape (rectangle, text, hotspot, image, stickyNote)
    - `text`: For text-based shapes
    - `image_url`: URL for images (if using an image block)
    """
    shape_id = f"shape_{uuid.uuid4().hex[:8]}"  # Unique ID

    shape = {
        "id": shape_id,
        "type": shape_type,
        "boundingBox": {"x": x, "y": y, "w": width, "h": height}
    }

    # ✅ Handle Specific Shape Properties
    if shape_type in ["rectangle", "stickyNote"]:
        shape["style"] = {
            "fill": {"type": "color", "color": color},
            "stroke": {"color": "#000000", "width": 1, "style": "solid"}
        }
        shape["text"] = text if text else name

    elif shape_type == "text":
        shape["text"] = text if text else name  # Text Blocks don't support styles

    elif shape_type == "hotspot":
        shape["style"] = {"stroke": {"color": "#000000", "width": 1, "style": "solid"}}  # No text

    elif shape_type == "image":
        shape["stroke"] = {"color": "#000000", "width": 1, "style": "solid"}
        shape["image"] = {"type": "image", "url": image_url}  # Must pass image_url

    shapes.append(shape)  # Store the shape
    return shape_id  # Return the shape ID for reference


def create_entity(name, attributes, x, y):
    """
    Auto-generates an entity table with attributes.
    
    - `name`: Entity name (e.g., "Users")
    - `attributes`: List of tuples [(name, is_primary_key), ...]
    - `x, y`: Position on the canvas
    """

    # Auto-calculate rows (1 extra row for the header)
    rows = len(attributes) + 1
    cols = 2  # First column = Attribute Name, Second column = PK indicator

    cell_data = []

    # ✅ Add Header Row
    cell_data.append({"x": 0, "y": 0, "text": name, "color": "#4682B4"})  # Table title
    cell_data.append({"x": 1, "y": 0, "text": "PK?", "color": "#4682B4"})  # PK Column Header

    # ✅ Add Attributes
    for index, (attr_name, is_primary_key) in enumerate(attributes):
        row = index + 1  # Offset by 1 because of the header
        cell_data.append({"x": 0, "y": row, "text": attr_name})  # Attribute Name
        cell_data.append({"x": 1, "y": row, "text": "✔" if is_primary_key else ""})  # PK Indicator

    return create_table(name, x, y, rows=rows, cols=2, cell_data=cell_data)



### 🚀 Create a Line Dynamically ###
def create_line(shape1_id, shape2_id, relationship="relationship", line_type="one-to-one", 
                start_side="right", end_side="left", text_position=0.5, text_side="top"):
    line_id = f"line_{uuid.uuid4().hex[:8]}"  

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
            "position": get_endpoint_position(start_side)
        },
        "endpoint2": {
            "type": "shapeEndpoint",
            "style": end_style,
            "shapeId": shape2_id,
            "position": get_endpoint_position(end_side)
        },
        "stroke": {
            "color": "#000000",
            "width": 2,
            "style": "solid"
        },
        "text": [
            {
                "text": relationship,
                "position": text_position,  # Stagger text placement
                "side": text_side           # Adjust text side
            }
        ]
    }
    lines.append(line)
    return line_id

def get_endpoint_position(side):
    """Helper function to return relative positions for endpoints."""
    positions = {
        "right": {"x": 1, "y": 0.5},
        "left": {"x": 0, "y": 0.5},
        "top": {"x": 0.5, "y": 0},
        "bottom": {"x": 0.5, "y": 1}
    }
    return positions.get(side, {"x": 1, "y": 0.5})  # Default to right



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
    print("🛠️ Generating Data Flow Diagram (DFD) and Entity Relationship Diagram (ERD)...")

    # ✅ **STEP 1: CREATE DATA FLOW DIAGRAM (DFD)**
    # External Entities
    customer = create_flowchart_element("Customer", x=100, y=100, flowchart_type="terminator")
    system = create_flowchart_element("Ordering System", x=400, y=100, flowchart_type="process")
    database = create_flowchart_element("Orders DB", x=700, y=100, flowchart_type="database")

    # Data Flow Lines
    create_line(customer, system, "Places Order", "one-to-one", start_side="right", end_side="left")
    create_line(system, database, "Saves Order", "one-to-one", start_side="right", end_side="left")
    create_line(database, system, "Retrieves Order Info", "one-to-one", start_side="left", end_side="right")
    create_line(system, customer, "Sends Confirmation", "one-to-one", start_side="left", end_side="right")

    # ✅ **STEP 2: CREATE ENTITY RELATIONSHIP DIAGRAM (ERD)**
    # Entities (Tables)
    users_table = create_entity("Users", [
        ("UserID", True),  # Primary Key
        ("Name", False),
        ("Email", False),
        ("CreatedAt", False)
    ], x=100, y=300)

    orders_table = create_entity("Orders", [
        ("OrderID", True),  # Primary Key
        ("UserID", False),
        ("TotalAmount", False),
        ("OrderDate", False)
    ], x=400, y=300)

    products_table = create_entity("Products", [
        ("ProductID", True),  # Primary Key
        ("ProductName", False),
        ("Price", False)
    ], x=700, y=300)

    order_items_table = create_entity("OrderItems", [
        ("OrderItemID", True),  # Primary Key
        ("OrderID", False),
        ("ProductID", False),
        ("Quantity", False)
    ], x=400, y=500)

    # Relationships (Crow's Foot Notation)
    create_line(users_table, orders_table, "places", "one-to-many", start_side="right", end_side="left")  # One User places Many Orders
    create_line(orders_table, order_items_table, "contains", "one-to-many", start_side="bottom", end_side="top")  # One Order contains Many OrderItems
    create_line(products_table, order_items_table, "included in", "one-to-many", start_side="bottom", end_side="top")  # One Product is included in Many OrderItems

    # ✅ **STEP 3: IMPORT TO LUCIDCHART**
    document_id = import_to_lucidchart()

    if document_id:
        print(f"🌍 Open the Lucidchart DFD + ERD: https://lucid.app/lucidchart/{document_id}/edit")

if __name__ == "__main__":
    main()

