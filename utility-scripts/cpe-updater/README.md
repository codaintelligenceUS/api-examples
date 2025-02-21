# 📝 Bulk CPE Updater

This helper script can bulk update a series of application IDs to certain
CPE values.

## 🔧 Prerequisites

Check the main `README.md` file for prerequisites

## 📝 Data format

This script will require a CSV file of this format:

| tenant_id | app_id | cpe_override    |
| --------- | ------ | --------------- |
| 1         | 123    | cpe:2.3:abc:... |

## 🏃 Running the script

In order to execute the script:

1. Make sure you have set up the `.env` file (or environment variables)
   according to the main `README.md` file
2. Run the script with the following command:

```bash
python cpe-updater.py path/to/data.csv
```
