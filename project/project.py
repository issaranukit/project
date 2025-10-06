import datetime
import uuid
import sys

items = {}
categories = {}
movements = []

def generate_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"

def print_line(char='-', length=90):
    print(char * length)

def get_datetime_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_item():
    item_id = input("Item ID: ").strip()
    if item_id in items:
        print("Item ID already exists.")
        return

    item_name = input("Item Name: ").strip()
    category_id = input("Category ID: ").strip()
    if category_id not in categories:
        category_name = input("Category Name (add new): ").strip()
        categories[category_id] = {"Category_Name": category_name}
        print(f"Category '{category_name}' added automatically.")
    brand = input("Brand/Model: ").strip()
    qty = int(input("Quantity: "))
    unit = input("Unit: ").strip()
    price = float(input("Unit Price: "))
    location = input("Location: ").strip()

    items[item_id] = {
        "Item_Name": item_name,
        "Category_ID": category_id,
        "Brand_Model": brand,
        "Quantity": qty,
        "Unit": unit,
        "UnitPrice": price,
        "Status": "Available",
        "Location": location
    }
    log_movement(item_id, "Add", qty, "-", location)
    print(f"Item '{item_name}' has been added.")

def update_item():
    item_id = input("Item ID to update: ").strip()
    if item_id not in items:
        print("Item not found.")
        return
    print("\n[1] Name\n[2] Quantity\n[3] Price\n[4] Location")
    choice = input("Choose field to update: ").strip()
    if choice == "1":
        items[item_id]["Item_Name"] = input("New Name: ")
    elif choice == "2":
        new_qty = int(input("New Quantity: "))
        diff = new_qty - items[item_id]["Quantity"]
        items[item_id]["Quantity"] = new_qty
        log_movement(item_id, "Update", diff, "-", items[item_id]["Location"])
    elif choice == "3":
        items[item_id]["UnitPrice"] = float(input("New Price: "))
    elif choice == "4":
        items[item_id]["Location"] = input("New Location: ")
    else:
        print("Invalid option.")
        return
    print("Item updated successfully.")

def delete_item():
    item_id = input("Item ID to delete: ").strip()
    if item_id not in items:
        print("Item not found.")
        return

    current_qty = items[item_id]["Quantity"]
    print(f"Current quantity: {current_qty}")
    qty_to_delete = int(input("Quantity to delete: "))

    if qty_to_delete <= 0:
        print("Invalid quantity.")
        return
    elif qty_to_delete > current_qty:
        print("Not enough quantity to delete.")
        return

    from_loc = items[item_id]["Location"]
    log_movement(item_id, "Delete", qty_to_delete, from_loc, "-")

    if qty_to_delete == current_qty:
        del items[item_id]
        print("Item completely deleted from inventory. Remaining quantity: 0")
    else:
        items[item_id]["Quantity"] -= qty_to_delete
        remaining = items[item_id]["Quantity"]
        print(f"{qty_to_delete} units deleted. Remaining quantity: {remaining} units.")

def transfer_item():
    item_id = input("Item ID to transfer: ").strip()
    if item_id not in items:
        print("Item not found.")
        return
    qty = int(input("Quantity to transfer: "))
    from_loc = items[item_id]["Location"]
    to_loc = input("Destination Location: ").strip()
    if qty > items[item_id]["Quantity"]:
        print("Not enough quantity.")
        return
    items[item_id]["Location"] = to_loc
    log_movement(item_id, "Transfer", qty, from_loc, to_loc)
    print(f"Item '{item_id}' transferred to {to_loc}.")

def dispose_item():
    item_id = input("Item ID to dispose: ").strip()
    if item_id not in items:
        print("Item not found.")
        return

    current_qty = items[item_id]["Quantity"]
    print(f"Current quantity: {current_qty}")
    qty_to_dispose = int(input("Quantity to dispose: "))

    if qty_to_dispose <= 0:
        print("Invalid quantity.")
        return
    elif qty_to_dispose > current_qty:
        print("Not enough quantity to dispose.")
        return

    from_loc = items[item_id]["Location"]
    log_movement(item_id, "Dispose", qty_to_dispose, from_loc, "-")

    if qty_to_dispose == current_qty:
        items[item_id]["Status"] = "Disposed"
        items[item_id]["Quantity"] = 0
        print("Item completely disposed.")
    else:
        items[item_id]["Quantity"] -= qty_to_dispose
        remaining = items[item_id]["Quantity"]
        print(f"{qty_to_dispose} units disposed. Remaining quantity: {remaining} units.")

def view_items():
    print_line("=")
    print(f"{'ID':<10} {'Category':<15} {'Name':<20} {'Qty':<5} {'Location':<20} {'Status':<10}")
    print_line("-")
    for item_id, data in items.items():
        cat_name = categories[data["Category_ID"]]["Category_Name"]
        print(f"{item_id:<10} {cat_name:<15} {data['Item_Name']:<20} {data['Quantity']:<5} {data['Location']:<20} {data['Status']:<10}")
    print_line("=")

def log_movement(item_id, action, qty, from_loc, to_loc):
    move_id = generate_id("MV")
    cat_id = items[item_id]["Category_ID"] if item_id in items else "-"
    movement = {
        "Move_ID": move_id,
        "Category_ID": cat_id,
        "Item_ID": item_id,
        "Action_Type": action,
        "Quantity": qty,
        "From_Location": from_loc,
        "To_Location": to_loc,
        "Action_By": "Admin",
        "Action_Date": get_datetime_now()
    }
    movements.append(movement)

def report():
    print("\nWarehouse & Asset Management - Activity Log")
    print(f"Generated At : {get_datetime_now()}")
    print_line()
    
    print(f"{'Move_ID':<12} {'Category':<15} {'Item':<20} {'Action':<10} {'Qty':<5} {'From':<15} {'To':<15} {'By':<10} {'Date'}")
    print_line("-")

    for mv in movements:
        cat_name = categories[mv["Category_ID"]]["Category_Name"] if mv["Category_ID"] in categories else "-"
        item_name = items[mv["Item_ID"]]["Item_Name"] if mv["Item_ID"] in items else "-"
        print(f"{mv['Move_ID']:<12} {cat_name:<15} {item_name:<20} {mv['Action_Type']:<10} {mv['Quantity']:<5} {mv['From_Location']:<15} {mv['To_Location']:<15} {mv['Action_By']:<10} {mv['Action_Date']}")

    print("\nWarehouse & Asset Management - Daily Summary (By Category)")
    print(f"Report Date : {get_datetime_now()}")
    print_line()

    summary = {}
    remaining_qty_by_cat = {}

    for mv in movements:
        cat_name = categories[mv["Category_ID"]]["Category_Name"] if mv["Category_ID"] in categories else "-"
        if cat_name not in summary:
            summary[cat_name] = {"Add": 0, "Update": 0, "Delete": 0, "Transfer": 0, "Dispose": 0}
            remaining_qty_by_cat[cat_name] = 0
        if mv["Action_Type"] in summary[cat_name]:
            summary[cat_name][mv["Action_Type"]] += mv["Quantity"]

    for item_id, data in items.items():
        cat_name = categories[data["Category_ID"]]["Category_Name"] if data["Category_ID"] in categories else "-"
        remaining_qty_by_cat[cat_name] = remaining_qty_by_cat.get(cat_name, 0) + data["Quantity"]

    total = 0
    for cat, data in summary.items():
        print(f"\n[ {cat} ]")
        for action, qty in data.items():
            print(f"  {action:<8}: {qty} units")
        balance = remaining_qty_by_cat.get(cat, 0)
        total += balance
        print(f"  Remaining Quantity: {balance} units")
    print_line()
    print(f"Overall Remaining Total: {total} units\n")

def main():
    while True:
        print("\nWarehouse Management System")
        print("[1] Add Item")
        print("[2] Update Item")
        print("[3] Delete Item")
        print("[4] Transfer Item")
        print("[5] Dispose Item")
        print("[6] View All Items")
        print("[7] View Report + Summary")
        print("[0] Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            add_item()
        elif choice == "2":
            update_item()
        elif choice == "3":
            delete_item()
        elif choice == "4":
            transfer_item()
        elif choice == "5":
            dispose_item()
        elif choice == "6":
            view_items()
        elif choice == "7":
            report()
        elif choice == "0":
            print("Exiting program...")
            sys.exit(0)
        else:
            print("Please choose a valid number.")

if __name__ == "__main__":
    main()

