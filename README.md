# 📁 Footprint API examples

This repository contains API access examples in various languages for performing operations on the Footprint platform.

The repository includes folders for examples in each supported language (currently only Python is provided, but more will be listed soon).

Each example performs the following operations:

- 🌟 Create a new co-managed client
- 🔍 Adds a domain to a new scan
- 🔁 Polls the endpoint and waits until the scan is done
- 📊 Retrieves the Technical Report for the provided tenant

This is just a basic example to get you started with using the Footprint API. For more information, see the Footprint OpenAPI schema, or contact the support team at support@codaintelligence.com.

## 🔧 Configuration variables

All examples in this repository assume the following environment variables are defined:

- `FOOTPRINT_DOMAIN` - The URL of your Footprint instance.
- `FOOTPRINT_API_KEY` - The API key of your Footprint account
- `FOOTPRINT_CO_MANAGED_CLIENT_NAME` - The name of your co-managed client
- `FOOTPRINT_CO_MANAGED_CLIENT_EMAIL` - The email address to use for the initial account
- `FOOTPRINT_SCAN_TARGET` - URL or IP address to scan

You can place these variables in a `.env` file next to the script. An example dotenv file with dummy values is included in the root of the repository.
The scripts will write the technical report as a JSON file to the current working directory.
