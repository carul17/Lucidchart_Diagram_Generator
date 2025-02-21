from script import *
import webbrowser

def main():
    print("🛠️ Generating Data Flow Diagram (DFD) and Entity Relationship Diagram (ERD) for Smart Logistics System...")

    # ✅ **STEP 1: CREATE DATA FLOW DIAGRAM (DFD)**
    # External Entities
    customer = create_flowchart_element("Customer", x=100, y=100, flowchart_type="terminator")
    supplier = create_flowchart_element("Supplier", x=100, y=300, flowchart_type="terminator")
    logistics_system = create_flowchart_element("Logistics System", x=400, y=200, flowchart_type="process")
    warehouse_db = create_flowchart_element("Warehouse DB", x=700, y=200, flowchart_type="database")

    # Data Flow Lines
    create_line(customer, logistics_system, "Places Order", "one-to-one", start_side="right", end_side="left")
    create_line(supplier, logistics_system, "Delivers Stock", "one-to-one", start_side="right", end_side="left")
    create_line(logistics_system, warehouse_db, "Updates Stock Level", "one-to-one", start_side="right", end_side="left")
    create_line(warehouse_db, logistics_system, "Retrieves Stock Info", "one-to-one", start_side="left", end_side="right")
    create_line(logistics_system, customer, "Sends Order Confirmation", "one-to-one", start_side="left", end_side="right")

    # ✅ **STEP 2: CREATE ENTITY RELATIONSHIP DIAGRAM (ERD)**
    # Entities (Tables)
    warehouses_table = create_entity("Warehouses", [
        ("WarehouseID", True),  # Primary Key
        ("Location", False),
        ("Capacity", False)
    ], x=100, y=500)

    inventory_table = create_entity("Inventory", [
        ("InventoryID", True),  # Primary Key
        ("WarehouseID", False),
        ("ProductID", False),
        ("StockLevel", False)
    ], x=400, y=500)

    products_table = create_entity("Products", [
        ("ProductID", True),  # Primary Key
        ("ProductName", False),
        ("Cost", False)
    ], x=700, y=500)

    orders_table = create_entity("Orders", [
        ("OrderID", True),  # Primary Key
        ("CustomerID", False),
        ("OrderDate", False),
        ("WarehouseID", False)
    ], x=100, y=700)

    customers_table = create_entity("Customers", [
        ("CustomerID", True),  # Primary Key
        ("Name", False),
        ("Email", False)
    ], x=400, y=700)

    shipments_table = create_entity("Shipments", [
        ("ShipmentID", True),  # Primary Key
        ("OrderID", False),
        ("ShipmentDate", False)
    ], x=700, y=700)

    # Relationships (Crow's Foot Notation)
    create_line(warehouses_table, inventory_table, "stores", "one-to-many", start_side="top", end_side="bottom")  # One Warehouse stores Many Inventory items
    create_line(products_table, inventory_table, "categorized as", "one-to-many", start_side="left", end_side="right")  # One Product applies to Many Inventory
    create_line(customers_table, orders_table, "places", "one-to-many", start_side="top", end_side="bottom")  # One Customer places Many Orders
    create_line(orders_table, shipments_table, "has", "one-to-one", start_side="top", end_side="bottom")  # One Order has One Shipment
    create_line(orders_table, warehouses_table, "fulfilled by", "many-to-one", start_side="left", end_side="right")  # Many Orders fulfilled by One Warehouse

    # ✅ **STEP 3: IMPORT TO LUCIDCHART**
    document_id = import_to_lucidchart()

    if document_id:
        lucidchart_url = f"https://lucid.app/lucidchart/{document_id}/edit"
        print(f"🌍 Open the Lucidchart Smart Logistics System DFD + ERD: {lucidchart_url}")
        webbrowser.open(lucidchart_url)

if __name__ == "__main__":
    main()