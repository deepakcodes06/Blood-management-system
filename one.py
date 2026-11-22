"""Blood Bank Management System (PS No. 75)
Python 3 | Concepts: Dictionaries, Lists, File Handling, Search
"""

import os
import re

# donors.txt is always looked up in the same folder as this .py file
DONOR_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "donors.txt")
VALID_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# Initial stock (blood group -> units)
stock = {g: 0 for g in VALID_GROUPS}
stock.update({"A+": 10, "B+": 5, "O+": 8, "AB+": 2})

# Donor records: list of dictionaries
donors = []


def reset_donor_file():
    """Start every run from the initial data: donors.txt has Meena Joshi and Suresh Rao."""
    with open(DONOR_FILE, "w") as f:
        f.write("Meena Joshi,O+,1\n")
        f.write("Suresh Rao,O+,2\n")


def load_donors():
    """Load existing donors from donors.txt.
    Accepts 'name,group,units' on separate lines, or several records
    on one line separated by 'and' (e.g. 'Meena Joshi, O+, 1 and Suresh Rao, O+, 2').
    """
    try:
        with open(DONOR_FILE, "r") as f:
            text = f.read()
    except FileNotFoundError:
        return
    pattern = r"([A-Za-z][A-Za-z .']*?)\s*,\s*(AB|A|B|O)\s*([+-])\s*,\s*(\d+)"
    for name, grp, sign, units in re.findall(pattern, text, re.IGNORECASE):
        name = name.strip()
        if name.lower().startswith("and "):
            name = name[4:].strip()
        donors.append({"name": name, "group": grp.upper() + sign, "units": int(units)})


def save_donor(donor):
    """Append one donor record to donors.txt."""
    with open(DONOR_FILE, "a") as f:
        f.write(f"{donor['name']},{donor['group']},{donor['units']}\n")


def valid_group_message():
    return "Invalid blood group. Valid groups: " + ", ".join(VALID_GROUPS) + "."


def read_units():
    """Read a positive whole number. Returns None if invalid."""
    text = input("Units: ").strip()
    if text.isdigit() and int(text) > 0:
        return int(text)
    print("Invalid units. Enter a positive whole number.")
    return None


def add_donor():
    name = input("Name: ").strip()
    group = input("Blood group: ").strip().upper()
    if group not in VALID_GROUPS:
        print(valid_group_message())
        return
    units = read_units()
    if units is None:
        return
    donor = {"name": name, "group": group, "units": units}
    donors.append(donor)
    save_donor(donor)
    stock[group] += units
    print(f"Donor saved to donors.txt. Stock of {group} is now {stock[group]} units.")


def issue_blood():
    group = input("Blood group: ").strip().upper()
    if group not in VALID_GROUPS:
        print(valid_group_message())
        return
    units = read_units()
    if units is None:
        return
    if units > stock[group]:
        print(f"Insufficient stock: only {stock[group]} unit(s) of {group} available.")
        return
    stock[group] -= units
    print(f"{units} unit(s) of {group} issued. Stock of {group} is now {stock[group]} units.")


def view_stock():
    print("Current blood stock:")
    for group in VALID_GROUPS:
        print(f"{group}: {stock[group]} unit(s)")


def search_donors():
    group = input("Blood group: ").strip().upper()
    if group not in VALID_GROUPS:
        print(valid_group_message())
        return
    found = [d for d in donors if d["group"] == group]
    if not found:
        print(f"No donors found with blood group {group}.")
        return
    print(f"Donors with blood group {group}:")
    for i, d in enumerate(found, 1):
        print(f"{i}. {d['name']} - {d['units']} unit(s)")
    print(f"Total donors found: {len(found)}")


def main():
    reset_donor_file()
    load_donors()
    while True:
        print("\n--- Blood Bank Menu ---")
        print("1. Add donor")
        print("2. Issue blood")
        print("3. View stock")
        print("4. Search donors")
        print("5. Exit")
        choice = input("Menu: ").strip()

        if choice == "1":
            add_donor()
        elif choice == "2":
            issue_blood()
        elif choice == "3":
            view_stock()
        elif choice == "4":
            search_donors()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
