"""
This file creates a CSV file containing information on all agents on a certain
tenant

For more details, check the associated `README.md` file
"""

import csv
import os
import sys
from time import strftime

import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
BASE_URL = f'https://{config["FOOTPRINT_DOMAIN"]}'
FOOTPRINT_TENANT_ID = config.get(
    "FOOTPRINT_TENANT_ID", os.environ.get("FOOTPRINT_TENANT_ID")
)
WAIT_TIMEOUT_SECS = 10

print(f"🔧 Config: {config}")


def retrieve_agents():
    """Function that retrieves agents information from the API"""

    print(
        f"📌 Beginning agent retrieval process for tenant {FOOTPRINT_TENANT_ID} on {config['FOOTPRINT_DOMAIN']}"
    )

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config["FOOTPRINT_API_KEY"],
        "FootprintTenantId": FOOTPRINT_TENANT_ID,
    }

    response = requests.get(
        f"{BASE_URL}/api/console/agent/",
        headers=headers,
    )

    if response.status_code != 200:
        print(f"\t❗Error retrieving agents: {response.status_code} {response.json()}")
        sys.exit(-1)

    return response.json().get("agents", [])


def write_csv(agents: list[dict]):
    """This function retrieves the agents listing and writes the CSV file"""
    timestamp = strftime("%Y%m%d")
    filename = f"agents-listing-{FOOTPRINT_TENANT_ID}-{timestamp}.csv"

    # This array will keep parsed items as a list of dict.
    # We will convert it to a list of lists to write to CSV
    items: list[dict] = []

    for agent in agents:
        agent_command_data = "Not running any command"

        if agent.get("agentCommandData"):
            agent_command_data = (
                f"Current command: {agent.get('agentCommandData', {}).get('commandText')}."
                + f"Status: {agent.get('agentCommandData', {}).get('commandStatus')}"
            )

        items.append(
            {
                "ID": agent.get("id", ""),
                "Hostname": agent.get("hostname", ""),
                "Operating System": agent.get("operatingSystem", ""),
                "OS Type": agent.get("osType", ""),
                "Private IP": agent.get("privateIp", ""),
                "Public IP": agent.get("publicIp", ""),
                "Installation Type": agent.get("installationType", ""),
                "Installation Scope": agent.get("installationScope", ""),
                "Installed On": agent.get("installedOn", ""),
                "Last Checkin": agent.get("lastCheckin", ""),
                "Last Update": agent.get("lastUpdate", ""),
                "Agent Version": agent.get("agentVersion", ""),
                "Status": agent.get("status", ""),
                "Domain Name": agent.get("domainName", ""),
                "AD Scope": agent.get("adScope", ""),
                "Number of Scan Entries": agent.get("noOfScanEntries", ""),
                "Agent Command Data": agent_command_data,
                "Restart Required": "Yes" if agent.get("restartRequired") else "No",
                "System Update In Progress": "Yes"
                if agent.get("systemUpdateInProgress")
                else "No",
                "Is Scanning Paused": "Yes" if agent.get("isScanningPaused") else "No",
                "Is Internal Scanner Installed": "Yes"
                if agent.get("isInternalScannerInstalled")
                else "No",
                "Is Meeting IS Requirements": "Yes"
                if agent.get("isISRequirementsMet")
                else "No",
            }
        )

    rows = []

    for item_index, sub in enumerate(items, start=0):
        if item_index == 0:
            rows.append(list(sub.keys()))
        rows.append(list(sub.values()))

    print(f"📝 Writing file {filename}...")
    with open(filename, "w", newline="\n") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL
        )

        for row in rows:
            writer.writerow(row)
    print("✅ Done.")


if __name__ == "__main__":
    agents = retrieve_agents()
    print(f"🔍 Retrieved {len(agents)} agents.")

    if len(agents) == 0:
        print("∅ No agents on provided tenant. Exiting.")
        sys.exit(0)

    write_csv(agents)
