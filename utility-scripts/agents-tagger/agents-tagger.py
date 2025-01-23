"""
This file creates a CSV file containing information on all agents on a certain
tenant

For more details, check the associated `README.md` file
"""

import csv
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
FOOTPRINT_AGENTS_TAGS = config.get(
    "FOOTPRINT_AGENTS_TAGS", os.environ.get("FOOTPRINT_AGENTS_TAGS")
)
FOOTPRINT_API_KEY = config.get("FOOTPRINT_API_KEY", os.environ.get("FOOTPRINT_API_KEY"))

print(f"🔧 Config: {config}")


def get_agents(tenant_id: str) -> dict[str, int] | None:
    """This function returns the agent IDs and hostnames on a tenant"""
    print(f"📥 Retrieving agents for tenant {tenant_id}...")

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": FOOTPRINT_API_KEY,
        "FootprintTenantId": tenant_id,
    }

    response = requests.get(
        f"{BASE_URL}/api/console/agent/",
        headers=headers,
    )

    if response.status_code == 200:
        agents = response.json().get("agents")

        data = {}
        for agent in agents:
            hostname = agent.get("hostname")
            agent_id = agent.get("id")

            if not hostname:
                print(f"\t\t⏭️ Skipping agent {agent_id} because of invalid keys")

            data[hostname] = agent_id

        return data

    else:
        try:
            response_json = response.json()
            print(
                f"\t❗Error retrieving agents: {response.status_code} {response_json}"
            )
        except Exception:
            print(
                f"\t❗Error retrieving agents: {response.status_code} {response.text}"
            )


def set_tags(tenant_id: str, hostname: str, tags: list[str], agents: dict[str, int]):
    """Sets tags for agent with a certain hostname"""

    agent_id = agents.get(hostname.encode("ascii", "ignore").decode())

    if not agent_id:
        print("\t❌ Could not find agent with given hostname - skipping...")
        return

    print(f"🏷️ Setting tags  for agent {agent_id}...")
    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": FOOTPRINT_API_KEY,
        "FootprintTenantId": tenant_id,
    }

    # Get the device ID
    computers_response = requests.get(
        f"{BASE_URL}/api/console/agent/{agent_id}/computers/",
        headers=headers,
    )

    try:
        computer_id = computers_response.json().get("items", [])[0].get("device")

        # Get current tags
        elements_response = requests.get(
            f"{BASE_URL}/api/console/elements/device/{computer_id}/",
            headers=headers,
        )

        existing_tags = elements_response.json().get("tags", [])

        tags_payload = [t for t in existing_tags if t.get("tag")]

        for tag in tags:
            tags_payload.append({"tag": tag, "excludeBusinessContexts": False})

        # Push tags
        tags_response = requests.post(
            f"{BASE_URL}/api/console/elements/device/{computer_id}/updateTags/",
            headers=headers,
            json=tags_payload,
        )

        if tags_response.status_code != 200:
            print(tags_response.status_code, tags_response.text)

        print(f"\t✅ Updated tags for {agent_id}")

    except Exception:
        print(f"\t❌ Error parsing response for {agent_id} - continuing")


def read_csv(filepath: str | None) -> list[list[str]]:
    """Reads CSV data from file path, or from environment variable"""

    print("👓 Reading file...")

    if not filepath:
        print("\t Filepath not supplied, trying env var")
        # Retrieve data from environment variable
        file_data = FOOTPRINT_AGENTS_TAGS

        if not file_data:
            print("❌ No envvar data provided - exiting...")
            sys.exit()

        file_data_rows = file_data.split(sep=";")
        data = []

        for row in file_data_rows:
            data.append(row.split(","))

        return data

    data = []
    with open(filepath, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            data.append(row)

    return data


if __name__ == "__main__":
    has_file_parameter = len(sys.argv) > 1

    if has_file_parameter:
        file = read_csv(sys.argv[1])
    else:
        file = read_csv(None)

    if not file:
        print("❌ No file provided - exiting...")
        sys.exit()

    if not FOOTPRINT_TENANT_ID:
        print("❌ No tenants provided - exiting...")
        sys.exit()

    agents = get_agents(FOOTPRINT_TENANT_ID)

    if not agents:
        print("❌ Error retrieving agents, exiting...")
        sys.exit()

    count = 0
    total_count = len(file)
    for entry in file:
        count += 1
        hostname = entry[0]
        tags = entry[1].split(",")
        print(f"\t🏷️ Updating with tags ({count} out of {total_count})")

        set_tags(FOOTPRINT_TENANT_ID, hostname, tags, agents)
