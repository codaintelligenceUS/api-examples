"""
This file reads a CSV file and runs the device uninstall & flush data request for each one

For more details, check the associated `README.md` file
"""

import csv
import sys
from time import sleep
import requests

from dotenv import dotenv_values

config = dotenv_values(".env")
BASE_URL = f"https://{config['FOOTPRINT_DOMAIN']}"
WAIT_TIMEOUT_SECS = 20

print(f"🔧 Config: {config}")


def delete_device(device_id: str, tenant_id: str):
    """This function takes an device and tenant id and runs the delete request"""

    API_URL = f"{BASE_URL}/api/console/elements/device/{device_id}/"
    print(
        f"🏃 Deleting device with ID {device_id} from tenant {tenant_id} via {API_URL}"
    )

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config["FOOTPRINT_API_KEY"],
        "FootprintTenantId": tenant_id,
    }

    response = requests.delete(
        API_URL,
        headers=headers,
    )

    if response.status_code == 200:
        print(f"\t✅ Deleted successfully device id {device_id}")
    else:
        print(
            f"\t❗Error deleting device {device_id}: {response.status_code} {response.text}"
        )


def read_csv(filepath: str):
    """Reads CSV data from file path"""
    data = []
    with open(filepath, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            data.append(row)

    return data


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("⚠️ No CSV file provided, exiting...")
        sys.exit()

    filename = sys.argv[1]
    print(f"🔍 Reading file {filename}")
    file_data = read_csv(filename)

    print(f"📌 Beginning device cleanup process on {config['FOOTPRINT_DOMAIN']}")

    for data in file_data:
        if len(data) < 2:
            print("⚠️ Empty data row, continuing...")
            continue
        tenant_id = data[0]
        device_id = data[1]

        delete_device(device_id, tenant_id)
        print(f"⏰ Waiting {WAIT_TIMEOUT_SECS} seconds before continuing")
        sleep(WAIT_TIMEOUT_SECS)
