"""
This file reads a CSV file and runs the CPE updater for each one.

For more details, check the associated `README.md` file
"""

import csv
import sys
import requests

from dotenv import dotenv_values

config = dotenv_values(".env")
BASE_URL = f"https://{config['FOOTPRINT_DOMAIN']}"

print(f"🔧 Config: {config}")


def update_cpe(app_id: str, tenant_id: str, new_cpe: str):
    """This function updates the CPE for a certain app"""

    print(f"🏃 Setting CPE {new_cpe} for app ID {app_id} on tenant {tenant_id}")

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config["FOOTPRINT_API_KEY"],
        "FootprintTenantId": tenant_id,
    }
    print(f"{BASE_URL}/api/console/elements/application/{app_id}/userEditor/")

    response = requests.post(
        f"{BASE_URL}/api/console/elements/application/{app_id}/userEditor/",
        headers=headers,
        json={"newCpe": new_cpe},
    )

    try:
        if response.status_code == 200:
            print(f"\t✅ Successfully edited CPE for {app_id}")
        else:
            print(
                f"\t❗Error editing CPE for {app_id}: {response.status_code} {response.json()}"
            )
    except Exception as e:
        print(e)
        print(f"\t ❗ Error editing CPE for {app_id}")


def read_csv(filepath: str):
    """Reads CSV data from file path"""
    data = []
    with open(filepath, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            data.append(row)

    return data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ No CSV file provided, exiting...")
        sys.exit()

    filename = sys.argv[1]
    print(f"🔍 Reading file {filename}")
    file_data = read_csv(filename)

    print(f"📌 Beginning CPE editing process on {config['FOOTPRINT_DOMAIN']}")

    for data in file_data:
        if len(data) < 2:
            print("⚠️ Empty data row, continuing...")
            continue
        tenant_id = data[0]
        app_id = data[1]
        new_cpe = data[2]

        update_cpe(app_id, tenant_id, new_cpe)
