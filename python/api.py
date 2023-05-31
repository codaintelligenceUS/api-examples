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
    Brief explanations of the keys are provided.
    Check the OpenAPI definition for more information.
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


if __name__ == "__main__":
    registration_id = create_registration()["id"]
