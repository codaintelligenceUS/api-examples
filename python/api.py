import json
import requests

# Load dotenv variables
from dotenv import dotenv_values

config = dotenv_values(".env")
BASE_URL = f'https://{config["FOOTPRINT_DOMAIN"]}'

headers = {
    "Content-Type": "application/json",
    "FootprintApiKey": config["FOOTPRINT_API_KEY"],
}

print(f"🔧 Config: {config}")


def create_registration():
    """
    This function performs the create co-managed registration call.
    """
    print("🌟 Creating new registration...")
    response = requests.put(
        f"{BASE_URL}/api/admin/registrations/",
        headers=headers,
        data=json.dumps(
            {
                "label": config[
                    "FOOTPRINT_CO_MANAGED_CLIENT_NAME"
                ],  # Registration name
                "description": "Footprint API Example",
                "photo": "",
                "associatedMspUserIds": [0],
                "managerId": 0,
                "manageType": "co_managed",
                "associatedMspGroupIds": [0],
                "signupData": {
                    "firstName": "API Example",
                    "lastName": "User",
                    "email": config["FOOTPRINT_CO_MANAGED_CLIENT_EMAIL"],
                    "companyName": "",
                    "companyWebsite": "",
                    "marketingOptIn": True,
                },
                "isPayingCustomer": True,
                "isAllMspAccessible": True,
                "maxBillableAssets": 0,
                "billingPlanType": "monthly",
            }
        ),
    )
    print(f"✅ Created new registration: {response.json()}")
    return response.json()


def get_cloud_scanner_id(tenant_id):
    """Retrieves the ID of the default cloud scanner"""

tenant_id_headers = {**headers, "FootprintTenantId": str(tenant_id)}
    print("📡 Retrieving cloud scanner...")
    scanners_response = requests.get(
        f"{BASE_URL}/api/console/scanSurface/scanners/", headers=tenant_id_headers
    )
    cloud_scanner_entry = [
        scanner
        for scanner in scanners_response.json()
        if scanner["isDefaultCloudScanner"]
    ][0]

    return cloud_scanner_entry["id"]


def start_scan(tenant_id):
    """
    This function performs the start scan call.
    """

    tenant_id_headers = {**headers, "FootprintTenantId": str(tenant_id)}
    scanner_id = get_cloud_scanner_id(tenant_id)
    print("🏃 Starting scan...")
    response = requests.post(
        f"{BASE_URL}/api/console/scanSurface/",
        headers=tenant_id_headers,
        data=json.dumps(
            {
                "scanTargets": [config["FOOTPRINT_SCAN_TARGET"]],
                "scanners": [scanner_id],
                "credentialsId": 0,
            }
        ),
    )
    print(f"✅ Started scan: {response.status_code} {response.json()}")


def wait_for_scan_finish(tenant_id):
    """
    Polls the server until thesc
    an is done"""






if __name__ == "__main__":
    tenant_id = 536  # create_registration()["meta"]["tenantId"]
    start_scan(tenant_id)
