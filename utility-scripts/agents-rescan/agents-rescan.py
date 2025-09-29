"""
This file triggers a rescan on all agents on a certain
tenant

For more details, check the associated `README.md` file
"""

import os
import sys

import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
BASE_URL = (
    f"https://{config.get('FOOTPRINT_DOMAIN', os.environ.get('FOOTPRINT_DOMAIN'))}"
)
FOOTPRINT_TENANT_ID = config.get(
    "FOOTPRINT_TENANT_ID", os.environ.get("FOOTPRINT_TENANT_ID")
)
WAIT_TIMEOUT_SECS = 10

print(f"🔧 Config: {config}")


def retrieve_agents():
    """Function that retrieves agents information from the API"""

    print(
        f"📌 Beginning agent retrieval process for tenant {FOOTPRINT_TENANT_ID} on {config.get('FOOTPRINT_DOMAIN', os.environ.get('FOOTPRINT_DOMAIN'))}"
    )

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config.get(
            "FOOTPRINT_API_KEY", os.environ.get("FOOTPRINT_API_KEY")
        ),
        "FootprintTenantId": FOOTPRINT_TENANT_ID,
    }

    response = requests.get(
        f"{BASE_URL}/api/console/agent/",
        headers=headers,
    )

    if response.status_code != 200:
        print(f"\t❗Error retrieving agents: {response.status_code} {response.json()}")
        sys.exit(-1)

    return [a.get("id", "") for a in response.json().get("agents", [])]


def rescan_agent(agent_id: int):
    """Triggers the rescan command on a certain agent"""

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config.get(
            "FOOTPRINT_API_KEY", os.environ.get("FOOTPRINT_API_KEY")
        ),
        "FootprintTenantId": FOOTPRINT_TENANT_ID,
    }

    try:
        print(f" 🔄 Rescanning agent {agent_id}...")
        response = requests.post(
            f"{BASE_URL}/api/console/agent/{agent_id}/scanDeviceNow/",
            headers=headers,
        )

        if response.status_code != 200:
            print(f"\t❗Error rescanning agent: {agent_id} {response.status_code}")
    except Exception as e:
        print(e)
        print(f"\t❌ Error rescanning agent {agent_id} - continuing")


if __name__ == "__main__":
    agents = retrieve_agents()
    print(f"🔍 Retrieved {len(agents)} agents.")

    if len(agents) == 0:
        print("∅ No agents on provided tenant. Exiting.")
        sys.exit(0)

    [rescan_agent(agent_id) for agent_id in agents]
