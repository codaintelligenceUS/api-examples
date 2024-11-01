"""
This file triggers the specified scheduler tasks

For more details, check the associated `README.md` file
"""

import os
import sys
import requests

from dotenv import dotenv_values

config = {**dotenv_values(".env"), **os.environ}
BASE_URL = f'https://{config.get( "FOOTPRINT_DOMAIN", "")}'
FOOTPRINT_API_KEY = config.get("FOOTPRINT_API_KEY", "")
TENANTS_TO_RUN_ON = config.get("TENANTS_TO_RUN_ON", "").split(",")
TASKS_TO_START = config.get("TASKS_TO_START", "").split(",")

print(f"🔧 Config: {config}")


def get_cloud_scanner_id(tenant_id: str):
    """Retrieves the cloud scanner ID for the specified tenant"""
    print(f"📡 Retrieving cloud scanner ID for tenant {tenant_id}")

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config["FOOTPRINT_API_KEY"],
        "FootprintTenantId": tenant_id,
    }

    response = requests.get(
        f"{BASE_URL}/api/console/scanSurface/scanners/",
        headers=headers,
    )

    if response.status_code == 200:
        scanners = response.json()
        for scanner in scanners:
            if scanner.get("isDefaultCloudScanner"):
                print(f"\t✅ Got cloud scanner ID for {tenant_id}")
                return scanner.get("id")

        print("\t❗Default cloud scanner not found in response")
        sys.exit(-1)
    else:
        print(
            f"\t❗Error retrieving schedulers for {tenant_id}: {response.status_code} {response.json()}"
        )
        sys.exit(-1)


def get_scheduler_tasks(tenant_id: str, scanner_id: str):
    """Retrieves associated scheduler tasks for a certain tenant"""
    print(f"⌛ Retrieving scheduler tasks for tenant {tenant_id}")

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config["FOOTPRINT_API_KEY"],
        "FootprintTenantId": tenant_id,
    }

    response = requests.get(
        f"{BASE_URL}/api/console/scheduler/?scannerId={scanner_id}",
        headers=headers,
    )

    if response.status_code == 200:
        print(f"\t✅ Got schedulers for {tenant_id}")
        return response.json()
    else:
        print(
            f"\t❗Error retrieving schedulers for {tenant_id}: {response.status_code} {response.json()}"
        )
        return []


def start_task(tenant_id: str, task_name: str, task_id: int, scanner_id: str):
    """Starts a task on the specified tenant"""
    print(f"\t🏃 Starting task {task_name} for {tenant_id}...")

    headers = {
        "Content-Type": "application/json",
        "FootprintApiKey": config["FOOTPRINT_API_KEY"],
        "FootprintTenantId": tenant_id,
    }

    response = requests.post(
        f"{BASE_URL}/api/console/scheduler/{task_id}/start/?scannerId={scanner_id}",
        headers=headers,
    )

    if response.status_code == 200:
        print(f"\t✅ Task {task_name} started for {tenant_id}")
    else:
        print(
            f"\t❗Error starting task {task_name} for {tenant_id}: {response.status_code} {response.json()}"
        )


if __name__ == "__main__":
    if len(TENANTS_TO_RUN_ON) == 0:
        print("⚠️ No tenants specified to run on")
        sys.exit(0)

    if len(TASKS_TO_START) == 0:
        print("⚠️ No tasks specified to run on")
        sys.exit(0)

    if FOOTPRINT_API_KEY == "":
        print("⚠️ No API key specified")
        sys.exit(0)

    for tenant in TENANTS_TO_RUN_ON:
        if tenant == "":
            continue
        cloud_scanner_id = get_cloud_scanner_id(tenant)
        scheduler_tasks = get_scheduler_tasks(tenant, cloud_scanner_id)

        for task in TASKS_TO_START:
            task_id = [
                entry.get("id")
                for entry in scheduler_tasks
                if entry.get("name", "") == task
            ][0]

            start_task(tenant, task, task_id, cloud_scanner_id)
