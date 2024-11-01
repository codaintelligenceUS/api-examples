# 📈 Scheduler start trigger

This script triggers the start of certain scheduler tasks when run.

## 🔧 Prerequisites

Check the main `README.md` file for prerequisites.

## 📝 Data format

This script will require the following environment variables to be set:

* `TENANTS_TO_RUN_ON` - comma-separated list of tenants to run on
  * For example - `TENANTS_TO_RUN_ON=1,2,3`
* `TASKS_TO_START` - comma-separated list of task names to run
  * These can be retrieved from the scheduler listing on the tenant
  * For example - `TASKS_TO_START=Remediation Report Generation,Contextual Risk Scoring Report Generation`

## 🏃 Running the script

In order to execute the script:

1. Make sure you have set up the `.env` file (or environment variables)
   according to the main `README.md` file.
2. Run the script with the following command:

```bash
python scheduler-trigger.py
```
