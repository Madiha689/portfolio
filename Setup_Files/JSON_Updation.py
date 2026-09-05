"""
***********************************************************************************************
* File Name   : JSON_Updation.py
* Author      : Madhurima Rawat
* Date        : June 13. 2025
* Description : A command-line tool for updating JSON files located in the 'assets/user_data'
*               directory. Supports both dictionary and list-based JSON structures. Users can
*               select a JSON file, preview differences, modify multiple keys interactively,
*               and save changes with ease. Includes color-coded output and formatted preview
*               for a better terminal experience.
* Libraries   : os, json, pyfiglet, copy, colorama
* Version     : 1.0
***********************************************************************************************
"""

import os
import json
import pyfiglet
from copy import deepcopy
from colorama import init, Fore, Style

# Initialize colorama for automatic reset after each print (for Windows terminal compatibility)
init(autoreset=True)

# Directory path containing all JSON files to be edited
BASE_PATH = r"../assets/user_data"


# Function to print a stylized ASCII banner centered in the terminal
def print_colored_centered_banner(text):
    banner = pyfiglet.figlet_format(text)
    width = os.get_terminal_size().columns
    for line in banner.split("\n"):
        print(Fore.YELLOW + line.center(width))


# Function to show a color-coded difference between original and updated dictionaries
def show_diff(before, after):
    print(Fore.YELLOW + "\n🟡 Preview of changes:")
    for key in before.keys():
        before_val = before[key]
        after_val = after.get(key, "<removed>")
        if before_val != after_val:
            print(f"{Fore.CYAN}{key}:")
            print(f"  {Fore.RED}- {before_val}")  # Original value
            print(f"  {Fore.GREEN}+ {after_val}")  # Updated value
    for key in after.keys():
        if key not in before:
            print(f"{Fore.CYAN}{key}:")
            print(f"  {Fore.GREEN}+ {after[key]}")  # Newly added key (if any)


# -----------------------------
#        MAIN INTERFACE
# -----------------------------
print_colored_centered_banner("Portfolio Templates")

# Ensure directory exists
if not os.path.exists(BASE_PATH):
    print(Fore.RED + f"❌ Directory does not exist: {BASE_PATH}")
    exit()

# Gather all JSON files in the directory
json_files = [f for f in os.listdir(BASE_PATH) if f.endswith(".json")]
if not json_files:
    print(Fore.RED + "❌ No JSON files found.")
    exit()

# Show list of available files
print(f"\n{Fore.CYAN}📂 Available JSON files:")
for i, file in enumerate(json_files, 1):
    print(f"  {i}. {file}")

# Ask user to select a file
try:
    index = (
        int(
            input(
                f"\n{Fore.YELLOW}🔢 Enter the number of the file to update: {Style.RESET_ALL}"
            )
        )
        - 1
    )
    if not (0 <= index < len(json_files)):
        raise ValueError
except ValueError:
    print(Fore.RED + "❌ Invalid selection.")
    exit()

# Load the chosen file
filename = json_files[index]
filepath = os.path.join(BASE_PATH, filename)

with open(filepath, "r") as f:
    data = json.load(f)

print(f"\n{Fore.CYAN}📄 Current content of {filename}:{Style.RESET_ALL}")

# ======================================================
# ==========   CASE 1: JSON is a DICTIONARY   ==========
# ======================================================
if isinstance(data, dict):
    # Display current key-value pairs
    for k, v in data.items():
        print(f"{k}: {v}")

    # Interactive editing loop
    while True:
        key = input(f"\n{Fore.YELLOW}✏️ Key to update: ").strip()

        # Disallow new keys if editing user.json
        if filename == "user.json" and key not in data:
            print(Fore.RED + f"❌ Adding new keys is not allowed in user.json.")
            print(Fore.CYAN + "✏️  You can still edit existing keys.")
            continue

        # Get current value and ask for update
        current_val = data.get(key, "")
        value = input(f"{key} ({current_val}): ").strip()

        # Handle list-type values separately
        if isinstance(current_val, list):
            data[key] = [item.strip() for item in value.split(",")]
        else:
            data[key] = value

        more = input("➕ Do you want to edit another key? (y/n): ").strip().lower()
        if more != "y":
            break

# ==================================================
# ==========   CASE 2: JSON is a LIST   ============
# ==================================================
elif isinstance(data, list):
    # Show current items
    for i, item in enumerate(data, 1):
        print(f"{i}. {json.dumps(item)}")

    # Ask user action
    print(f"\n{Fore.YELLOW}What would you like to do?")
    print("  1. Edit an existing item")
    print("  2. Append a new item")
    choice = input("Enter 1 or 2: ").strip()

    # ---- Edit existing item ----
    if choice == "1":
        try:
            idx = int(input("Enter the item number to edit: ")) - 1
            if not (0 <= idx < len(data)):
                raise IndexError
        except (ValueError, IndexError):
            print(Fore.RED + "❌ Invalid index.")
            exit()

        # Make a backup of original for diff comparison
        original = deepcopy(data[idx])
        print(f"\nCurrent item:\n{json.dumps(original, indent=4)}")

        while True:
            key = input(f"{Fore.YELLOW}🔧 Key to update (blank to skip): ").strip()
            if not key:
                print(Fore.YELLOW + "⚠️ No key entered.")
                break
            if key not in data[idx]:
                print(Fore.RED + f"❌ Key '{key}' not found.")
                continue

            current_val = data[idx][key]
            new_val = input(f"{key} ({current_val}): ").strip()

            if new_val:
                if isinstance(current_val, list):
                    data[idx][key] = [v.strip() for v in new_val.split(",")]
                else:
                    data[idx][key] = new_val

            more = input("➕ Do you want to edit another key? (y/n): ").strip().lower()
            if more != "y":
                break

        # Show changes and confirm
        show_diff(original, data[idx])
        confirm = input(f"\n{Fore.YELLOW}💾 Save changes? (y/n): ").strip().lower()
        if confirm != "y":
            print(Fore.RED + "❌ Changes discarded.")
            exit()

    # ---- Append new item ----
    elif choice == "2":
        # For user.json, block new additions
        if filename == "user.json":
            print(Fore.RED + "\n❌ Adding new items is not allowed in user.json.")
            print(Fore.CYAN + "✏️  You can still edit existing items.")
            exit()

        # Create a new item with same structure as first item
        template_keys = (
            list(data[0].keys()) if data and isinstance(data[0], dict) else []
        )
        new_item = {}

        if template_keys:
            print(f"\n{Fore.YELLOW}➕ Add new item: Fill in the following fields")
            for key in template_keys:
                val = input(f"{key.capitalize()}: ").strip()
                if val:
                    new_item[key] = (
                        [v.strip() for v in val.split(",")] if "," in val else val
                    )
        else:
            print(
                Fore.RED
                + "❌ Cannot infer template keys. Make sure the first item is a dictionary."
            )
            exit()

        data.append(new_item)
        print(Fore.GREEN + "\n✅ Item appended successfully.")
    else:
        print(Fore.RED + "❌ Invalid choice.")
        exit()

# ==================================================
# ==========   CASE 3: Unsupported Format   =========
# ==================================================
else:
    print(Fore.RED + "❌ Unsupported JSON structure.")
    exit()

# ==========================
# 🔐 Save the Final Result
# ==========================
updated_filepath = os.path.join(BASE_PATH, filename)

with open(updated_filepath, "w") as f:
    json.dump(data, f, indent=4)

print(f"\n{Fore.GREEN}✅ Updated file saved as: {filename}")
print(f"\n{Fore.CYAN}📝 Final updated content:{Style.RESET_ALL}")
print(json.dumps(data, indent=4))
