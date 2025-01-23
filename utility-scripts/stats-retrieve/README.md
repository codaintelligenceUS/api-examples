# 📊 Assets count script

This script gathers the total number of applications and IPs scanned on a series of environments.

## 🔧 Prerequisites

Check the main `README.md` file for prerequisites.

> [!NOTE]
>
> This script uses `FOOTPRINT_USERNAME` and `FOOTPRINT_PASSWORD` instead of API key.
>
> Make sure your user has access to all provided instances.

## 📝 Data format

This script will require the following environment variables to be set:

- `ENVIRONMENTS_TO_RUN_ON` - comma-separated list of Footprint environments to run on

## 📝 Output format

This script will output a CSV file with the following header:

| Environment | Apps Count | IP Addresses Count |
| ----------- | ---------- | ------------------ |
| server1.com | 45         | 123                |
| ...         | ...        | ...                |
| Total       | 1234       | 4567               |

## 🏃 Running the script

In order to execute the script:

1. Make sure you have set up the `.env` file (or environment variables)
   according to the main `README.md` file.
2. Run the script with the following command:

```bash
python stats-retrieve.py
```
