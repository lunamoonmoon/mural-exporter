from dotenv import load_dotenv
import os
import time
import requests
import json
import csv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")

def get_pdf_link_by_api(mural_id, export_id, api_key, max_retries=10, delay=10):
    url = f"https://app.mural.co/api/public/v1/murals/{mural_id}/exports/{export_id}"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            if "value" in data and "url" in data["value"]:
                return data["value"]["url"]
            else:
                print(f"Attempt {attempt + 1}: Export not ready yet.")
                print("Response:", json.dumps(data, indent=2))
        else:
            print(f"Attempt {attempt + 1}: Failed with status {response.status_code}")
        time.sleep(delay)
    return None

# Read export info from CSV
with open("exports/mural_exports.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mural_id = row["mural_id"]
        export_id = row["export_id"]
        mural_name = row["mural_name"]

        pdf_url = get_pdf_link_by_api(mural_id, export_id, ACCESS_TOKEN)
        if pdf_url:
            file_path = os.path.join("exports/pdfs", f"{mural_name}.pdf")
            download_response = requests.get(pdf_url)
            if download_response.ok:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(download_response.content)
                print(f"Exported mural '{mural_name}' to {file_path}")
            else:
                print(f"Failed to download file from URL: {download_response.status_code}")
        else:
            print(f"Export URL not ready for mural '{mural_name}'")
