"""
This file reads a CSV file and runs the agent uninstall & flush data request for each one

For more details, check the associated `README.md` file
"""

import csv
import sys
from time import sleep
import requests

from dotenv import dotenv_values

config = dotenv_values(".env")
BASE_URL = f'https://{config["FOOTPRINT_DOMAIN"]}'
WAIT_TIMEOUT_SECS = 10

print(f"🔧 Config: {config}")


def delete_agent(agent_id: str, tenant_id: str):
    """This function takes an agent and tenant id and runs the delete request"""

    print(f"🏃 Deleting agent with ID {agent_id} from tenant {tenant_id}")

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config["FOOTPRINT_API_KEY"],
        "FootprintTenantId": tenant_id,
    }

    response = requests.post(
        f"{BASE_URL}/api/console/agent/{agent_id}/uninstall/?flushResults=true",
        headers=headers,
    )

    if response.status_code == 200:
        print(f"\t✅ Deleted successfully agent id {agent_id}")
    else:
        print(
            f"\t❗Error deleting agent {agent_id}: {response.status_code} {response.json()}"
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

    print(f"📌 Beginning agent cleanup process on {config['FOOTPRINT_DOMAIN']}")

    for data in file_data:
        if len(data) < 2:
            print("⚠️ Empty data row, continuing...")
            continue
        tenant_id = data[0]
        agent_id = data[1]

        delete_agent(agent_id, tenant_id)
        print(f"⏰ Waiting {WAIT_TIMEOUT_SECS} seconds before continuing")
        sleep(WAIT_TIMEOUT_SECS)
