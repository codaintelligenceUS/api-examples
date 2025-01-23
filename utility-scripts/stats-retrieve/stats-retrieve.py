"""
This file collects stats about the assets detected on various environments.

For more details, check the associated `README.md` file
"""

import csv
import json
import os
import sys
from time import strftime
from typing import Literal, Union
import requests

from dotenv import dotenv_values

config = {**dotenv_values(".env"), **os.environ}
FOOTPRINT_USERNAME = config.get("FOOTPRINT_USERNAME", "")
FOOTPRINT_PASSWORD = config.get("FOOTPRINT_PASSWORD", "")
ENVIRONMENTS_TO_RUN_ON = config.get("ENVIRONMENTS_TO_RUN_ON", "").split(",")

print(f"🔧 Config: {config}")

default_headers = {
    "Content-Type": "application/json",
}


def get_auth_token(environment: str):
    """Retrieves the JWT token for authenticating"""
    print(f"\t🔑 Retrieving JWT token for {environment}")

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"https://{environment}/api/auth/token/",
        headers=headers,
        json={"username": FOOTPRINT_USERNAME, "password": FOOTPRINT_PASSWORD},
    )

    if response.status_code == 200:
        response = response.json()
        access_key = response.get("access", "N/A")
        print(f"\t🔑 Got JWT key {access_key}")

        # Also add the key as the auth token
        default_headers.update({"Authorization": f"Bearer { access_key }"})

        return access_key

    else:
        print(f"\t❗Error getting JWT key: {response.status_code} {response.json()}")
        sys.exit(-1)


def get_tenants(environment: str) -> list[dict]:
    """Retrieves list of available tenants"""
    print("💼 Retrieving list of available tenants...")

    headers = {**default_headers}

    response = requests.get(
        f"https://{environment}/api/common/auth/session/accounts/?size=1000000000000000000",
        headers=headers,
    )

    if response.status_code != 200:
        print(f"\t❗Error retrieving tenants: {response.status_code} {response.json()}")
        sys.exit(-1)

    tenants = response.json().get("items", [])

    # Exclude internal tenants
    tenants = [
        t for t in tenants if t.get("label") not in ["CODA Internal", "MSP Internal"]
    ]

    print(f"📋 Retrieved {len(tenants)} tenants.")
    return tenants


def get_statuses(
    tenant_id: str, tenant_name: str, environment: str
) -> dict[Union[Literal["apps"], Literal["devices"], Literal["ips"]], int]:
    """Retrieves associated stats for tenant"""
    print(
        f"📊 Retrieving assets stats for tenant {tenant_id} {tenant_name} on {environment}"
    )

    headers = {
        **default_headers,
        "FootprintTenantId": f"{ tenant_id }",
    }

    status_response = requests.get(
        f"https://{environment}/api/console/status/",
        headers=headers,
    )

    ips_response = requests.get(
        f"https://{environment}/api/console/scanSurface/",
        headers=headers,
    )

    ips = 0

    if ips_response.status_code == 200:
        ips = ips_response.json().get("totalCount", 0)

    if status_response.status_code == 200:
        counts = status_response.json().get("count")

        if not counts:
            print(status_response.json())
            print("\t 🤪 No counts in response for tenant, continuing")
            return {"apps": 0, "devices": 0, "ips": ips}

        return {
            "apps": counts.get("applications", 0),
            "devices": counts.get("servers", 0),
            "ips": ips,
        }
    else:
        print(
            f"\t❗Error retrieving schedulers for {tenant_id}: {status_response.status_code} {status_response.json()}"
        )
        return {"apps": 0, "devices": 0}


def write_to_csv(items: list[dict], filename):
    """This file writes the stats list to CSV"""
    timestamp = strftime("%Y%m%d")
    # filename = f"global-stats-{timestamp}.csv"

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


import argparse

parser = argparse.ArgumentParser(description="Collect stats from Footprint API")
parser.add_argument("domains", nargs="+", help="List of domains to process")
args = parser.parse_args()

if __name__ == "__main__":
    if FOOTPRINT_USERNAME == "":
        print("⚠️ No user specified")
        sys.exit(0)

    print(f"📊 Getting stats for {', '.join(args.domains)}")

    total_env_apps = 0
    total_env_devices = 0
    total_env_ips = 0

    for domain in args.domains:
        print(f"🌐 Processing domain: {domain}")

        stats = []

        get_auth_token(domain)
        tenants = get_tenants(domain)

        current_tenant_count = 1

        total_apps = 0
        total_devices = 0
        total_ips = 0

        for tenant in tenants:
            print(f"\tProcessing tenant {current_tenant_count} of {len(tenants)}")
            current_tenant_count += 1

            tenant_stats = get_statuses(tenant["id"], tenant["label"], domain)

            total_apps += tenant_stats.get("apps", 0)
            total_devices += tenant_stats.get("devices", 0)
            total_ips += tenant_stats.get("ips", 0)

        stats.append(
            {
                "Environment": domain,
                "Apps Count": total_apps,
                "Devices Count": total_devices,
                "IP Addresses Count": total_ips,
            }
        )

        write_to_csv(stats, f"{domain}_stats_{strftime('%Y%m%d')}.csv")
