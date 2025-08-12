from dotenv import load_dotenv
import requests
import time
import json
import os
import csv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")

# Get a workspaces murals and save to a JSON file
url = f"https://app.mural.co/api/public/v1/workspaces/{WORKSPACE_ID}/murals?status=active&sortBy=lastCreated"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(url, headers=headers)

# Create exports directory and save mural boards metadata
os.makedirs("exports", exist_ok=True)
with open("exports/murals_list.json", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Murals list saved to exports/murals_list.json")

# Load mural list
with open("exports/murals_list.json", "r", encoding="utf-8") as file:
    murals_data = json.load(file)

# Create output directory for PDFs
os.makedirs("exports/pdfs", exist_ok=True)

# Create list to store export links
export_links = []

for mural in murals_data.get("value", []):
    mural_id = mural.get("id")
    mural_name = mural.get("name", f"mural_{mural_id}")
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in mural_name)

    # Request export id
    export_url = f"https://app.mural.co/api/public/v1/murals/{mural_id}/export"
    payload = { "downloadFormat": "pdf" }
    export_response = requests.post(export_url, headers=headers, json=payload)

    if export_response.ok:
        export_id = export_response.json()["value"]["exportId"]

        export_links.append({
            "mural_id": mural_id,
            "mural_name": mural_name,
            "export_id": export_id,
        })
    else:
        print(f"Failed to initiate export for mural '{mural_name}'")

# Export links to CSV
with open("exports/mural_exports.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["mural_id", "mural_name", "export_id", "export_file_link"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in export_links:
        writer.writerow(row)

print("Export links saved to exports/mural_exports.csv")
