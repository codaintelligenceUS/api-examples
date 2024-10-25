# 📁 Footprint API examples

This repository contains API access examples in various languages for
performing operations on the Footprint platform.

You will find two folders in this repo:

- `api-flow-example/` - An example flow script
- `utility-scripts/` - Various scripts that may be useful for performing API
  operations in Footprint.

## 🔧 Prerequisites

Make sure you have a working Python installation.

Run `pip install -r requirements.txt` to make sure all dependencies are
installed.

## 🌊 API Flow Example

The script in `api-flow-example/` shows how to do a basic end-to-end scan flow
via the API. The operations performed are:

- 🌟 Creating a new co-managed client
- 🔍 Adding a domain to a new scan
- 🔁 Polling the endpoint and waiting until the scan is done
- 📊 Retrieving the Technical Report for the provided tenant

This is just a basic example to get you started with using the Footprint API.
For more information, see the Footprint OpenAPI schema, or contact the support
team at <support@codaintelligence.com>.

The scripts will write the technical report as a JSON file to the current
working directory.

## 🧰 Utility Scripts

These scripts are helpful utilities for performing various common operations.
Check the `README.md` file in each subfolder for details.

## 🔧 Configuration variables

All examples in this repository assume the following environment variables are
defined:

- `FOOTPRINT_DOMAIN` - The URL of your Footprint instance.
- `FOOTPRINT_API_KEY` - The API key of your Footprint account.

> [!NOTE]
>
> These scripts assume you use an API key to authenticate to the
> Footprint instance.
> You can obtain an API key from your profile page.

The scripts in the `api-flow-example/` folder also assume these variables are defined:

- `FOOTPRINT_CO_MANAGED_CLIENT_NAME` - The name of your co-managed client
- `FOOTPRINT_CO_MANAGED_CLIENT_EMAIL` - The email address to use for the initial
  account
- `FOOTPRINT_SCAN_TARGET` - URL or IP address to scan

You can place these variables in a `.env` file next to the script.
An example dotenv file with dummy values is included in the root of the
repository.
