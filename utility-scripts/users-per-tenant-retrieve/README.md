# 👥 Retrieve users for each tenant

This script will generate a CSV file of all the users in the platform for all the
tenants on which the API Key user has access to.

## 🔧 Prerequisites

Check the main `README.md` file for prerequisites.

## 🏃 Running this script

In order to execute this script:

1. Make sure you have set up the `.env` file (or environment variables)
   according to the main `README.md` file.
2. Run the script with the following command:

```bash
python users-per-tenant-retrieve.py
```

The script will output an `users-per-tenant-{YYYYMMDD}-{FOOTPRINT_HOSTNAME}.csv` file containing the
requested data.
