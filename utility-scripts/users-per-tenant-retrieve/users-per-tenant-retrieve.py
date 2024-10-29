"""This file retrieves users for each available tenant.

For more details, check the associated `README.md` file
"""

import csv
import sys
from time import sleep, strftime
import requests

from dotenv import dotenv_values

config = dotenv_values(".env")
BASE_URL = f'https://{config["FOOTPRINT_DOMAIN"]}'

print(f"🔧 Config: {config}")


def get_tenants() -> list[dict]:
    """Retrieves list of available tenants"""
    print("💼 Retrieving list of available tenants...")

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config["FOOTPRINT_API_KEY"],
    }

    response = requests.get(
        f"{BASE_URL}/api/common/auth/session/accounts/?size=1000000000000000000",
        headers=headers,
    )

    if response.status_code != 200:
        print(f"\t❗Error retrieving tenants: {response.status_code} {response.json()}")
        sys.exit(-1)

    tenants = response.json().get("items", [])

    print(f"📋 Retrieved {len(tenants)} tenants.")
    return tenants


def get_users(tenant_id: int, tenant_name: str) -> list[dict]:
    """Retrieves users for a certain tenant"""
    print(f"👥 Retrieving users for tenant {tenant_id} {tenant_name}...")

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config["FOOTPRINT_API_KEY"],
        "FootprintTenantId": str(tenant_id),
    }

    response = requests.get(
        f"{BASE_URL}/api/common/users/",
        headers=headers,
    )

    if response.status_code != 200:
        print(f"\t❗Error retrieving users: {response.status_code} {response.json()}")
        sys.exit(-1)

    users = response.json()

    print(f"\t📋 Retrieved {len(users)} users.")
    return users


def write_to_csv(items: list[dict]):
    """This file writes the users list to CSV"""
    timestamp = strftime("%Y%m%d")
    filename = f"users-per-tenant-{timestamp}-{config['FOOTPRINT_DOMAIN']}.csv"

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
    all_users = []
    tenants = get_tenants()

    for tenant in tenants:
        users = get_users(tenant["id"], tenant["name"])

        for user in users:
            all_users.append(
                {
                    "firstName": user.get("firstName", ""),
                    "lastName": user.get("lastName", ""),
                    "isActive": user.get("isActive", ""),
                    "email": user.get("email", ""),
                    "tenant": tenant["name"],
                }
            )

    write_to_csv(all_users)
