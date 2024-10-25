# 🗑️Bulk agents delete script

This helper script can sequentially delete a number of agents via the Footprint
API.

## 🔧 Prerequisites

Check the main `README.md` file for prerequisites.

## 📝 Data format

This script will require a CSV file of this format:

| `tenant_id` | `agent_id` |
| ----------- | ---------- |
| 1           | 2          |

## 🏃 Running the script

In order to execute the script:

1. Make sure you have set up the `.env` file (or environment variables)
   according to the main `README.md` file.
2. Run the script with the following command:

```bash
python bulk-agents-delete.py path/to/data.csv
```
