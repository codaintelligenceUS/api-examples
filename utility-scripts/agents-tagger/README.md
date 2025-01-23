# 🏷️ Agent Bulk Tagger

This script applies a tag or list of tags to a number of agents supplied via
hostname.

## 🔧 Prerequisites

Check the main `README.md` file for prerequisites.

## 🏃 Running the script

In order to execute this script:

1. Make sure you have set up the `.env` file (or environment variables)
   according to the main `README.md` file.
2. Export the `FOOTPRINT_TENANT_ID` environment variable (or add it to your
   `.env` file) with the ID of the tenant you want to retrieve data from.
3. Supply the CSV file (see below)
4. Run the script (see below)

## 📊 Supplying the CSV file / running the script

You can supply the CSV file in two ways:

### 📝 As a file argument

For this, your CSV file has to have the following format:

| Hostname  | Tags      |
| --------- | --------- |
| DESKTOP-1 | Tag1 Tag2 |

> Note: Use spaces to separate the tags

You can supply it like so:

```bash
python agents-tagger.py myfile.csv
```

### ⛰️ As an environment variable

For usage in more restricted environments, such as an CI environment, you can
also supply the list of hostnames and tags as an environment file.

The format is similar to the CSV format - use `\n` as a newline separator and
commas as field separators. Same as in CSV, use spaces to separate tags.

For example:

```bash
export FOOTPRINT_AGENTS_TAGS='DESKTOP-1,Tag1 Tag2\nDESKTOP-2,Tag3'
```

And then run the file without arguments:

```bash
python agents-tagger.py
```

> ⚠️ No header row is needed in either the CSV or ENV variants

The script will output status on what operation it is performing.
