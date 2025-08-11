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
    "authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(url, headers=headers)

# Create directory and save murals list
os.makedirs("exports", exist_ok=True)
with open("exports/murals_list.json", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Murals list saved to exports/murals_list.json")

# Load mural list
with open("exports/murals_list.json", "r", encoding="utf-8") as file:
    murals_data = json.load(file)

# Create output directory for PDFs
os.makedirs("exports/pdfs", exist_ok=True)

# Get pdf link
def get_pdf_link_by_api(mural_id, export_id, api_key, max_retries=10, delay=5):
    url = f"https://app.mural.co/api/public/v1/murals/{mural_id}/exports/{export_id}"
    headers = {
        "authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }

    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            if "value" in data and "url" in data["value"]:
                return data["value"]["url"]
        time.sleep(delay)
    return None

# Create list to store export links
export_links = []

for mural in murals_data.get("value", []):
    mural_id = mural.get("id")
    mural_name = mural.get("name", f"mural_{mural_id}")
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in mural_name)

    # Request export
    export_url = f"https://app.mural.co/api/public/v1/murals/{mural_id}/export"
    payload = { "downloadFormat": "pdf" }
    export_response = requests.post(export_url, headers=headers, json=payload)

    if export_response.ok:
        export_id = export_response.json()["value"]["exportId"]
        pdf_url = get_pdf_link_by_api(mural_id, export_id, ACCESS_TOKEN)

        export_links.append({
            "mural_id": mural_id,
            "mural_name": mural_name,
            "export_id": export_id,
            "export_file_link": pdf_url
        })

        if pdf_url:
            file_path = os.path.join("exports/pdfs", f"{safe_name}.pdf")
            download_response = requests.get(pdf_url)
            if download_response.ok:
                with open(file_path, "wb") as f:
                    f.write(download_response.content)
                print(f"Exported mural '{mural_name}' to {file_path}")
            else:
                print(f"Failed to download file from URL: {download_response.status_code}")
        else:
            print(f"Export URL not ready for mural '{mural_name}'")
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
