# -*- coding: utf-8 -*-
"""Jupiter Trading Volume ATH Alert Dune API Integration


IMPORTING LIBRARIES
"""

import logging
import requests
import time
import json
import shutil
import os
from dotenv import load_dotenv

"""LOAD ENVIRONMENT VARIABLES"""
load_dotenv()

"""SETTING UP LOGGING"""
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""SETTING ENVIRONMENT"""

DUNE_API_KEY = os.getenv("DUNE_API_KEY")
QUERY_ID = 5193365
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
headers = {
    "x-dune-api-key": DUNE_API_KEY
}


def handle_response(response):
    try:
        response.raise_for_status()  # levanta erro HTTP se for 4xx ou 5xx
        return response.json()
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err} - Status Code: {response.status_code}")
        return None
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        return None

"""QUERY EXECUTION"""

execute_response = requests.post(
    f"https://api.dune.com/api/v1/query/{QUERY_ID}/execute",
    headers=headers
)
execution_id = execute_response.json()["execution_id"]
print(f"Query executed. Execution ID: {execution_id}")

"""POLL FOR STATUS"""

# Step 2: Poll for status
while True:
    status_response = requests.get(
        f"https://api.dune.com/api/v1/execution/{execution_id}/status",
        headers=headers
    )
    state = status_response.json()["state"]
    print(f"Query state: {state}")

    if state == "QUERY_STATE_COMPLETED":
        break
    elif state in ["QUERY_STATE_FAILED", "QUERY_STATE_CANCELLED", "QUERY_STATE_ERRORED"]:
        raise Exception(f"Query failed with state: {state}")

    time.sleep(2)  # wait before checking again

"""FETCH THE RESULTS"""

# Step 3: Fetch the results
results_response = requests.get(
    f"https://api.dune.com/api/v1/execution/{execution_id}/results",
    headers=headers
)
results = results_response.json()
print(results)

"""EXTRACTING VALUES FROM RESULTS"""

row = results["result"]["rows"][0]  # assuming only 1 row is returned
week = row["week"][:10]
volume = row["volume"]
rank = row["volume_rank"]

"""COMPOSING AND SENDING DISCORD MESSAGE"""

discord_message = {
    "content": (
        f"Jupiter Total Volume Weekly Update\n"
        f"**Week of {week}**\n"
        f"Total Volume: **${volume:,.2f}**\n"
        f"Rank: **#{rank} all-time**"
    )
}

discord_response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)

if discord_response.status_code == 204:
    print("Message successfully sent to Discord!")
else:
    print(f"Failed to send message. Status: {discord_response.status_code}")
    print(discord_response.text)

"""SAVING RESULTS TO JSON FILE"""

# Save results to JSON file
json_file_path = "dune_results.json"
with open(json_file_path, "w") as json_file:
    json.dump(results, json_file, indent=4)

print(f"JSON results saved to {json_file_path}")

# Export JSON file
downloads_path = os.path.join(os.environ["HOME"], "Downloads")
shutil.copy(json_file_path, downloads_path)

print(f"File copied to {downloads_path}")

"""EXPORTING JSON FILE"""

# from google.colab import files
# files.download("dune_results.json")
