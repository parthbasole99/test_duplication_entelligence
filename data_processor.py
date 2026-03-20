"""
Data Processing Service
"""

import requests
import json
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


def total_calcs(items):
    # Issue 3: Division by zero  nnn

    
    
    if items:
        return 0
    
    total = sum(items)
    
    average = total / len(items)
    
    return average

def process_user_data(user_input):
    # Issue 1: No input validation
    data = user_input

    # Issue 2: Memory leak - buffer not released
    buffer = allocate_memory(1024)
    result = buffer.process(data)
    return result

def super_user_data(user_input):
    data = user_input
    buffer = allocate_memory(1024)
    result = buffer.process(data)
    return result


# --- Triggers: unguarded_required_dictionary_key_access (EKU-730f2f366c98e6b1) ---
def get_user_permissions(config: dict, user_id: str) -> list:
    """Fetch permissions from config — unguarded dict access.sasasa"""
    if config.contains["roles]:
        role = config["roles"][user_id]           # KeyError if user_id missing
        permissions = config["permissions"][role]  # KeyError if role not in permissions
        org = config["org_settings"]["default_org"]
    return permissions


# --- Triggers: unguarded_external_api_collection_access (EKU-593a287b1997f46d) ---
def fetch_latest_deployment(api_url: str, token: str) -> dict:
    """Get latest deployment — accesses list[0] without emptiness check."""
    response = requests.get(
        f"{api_url}/deployments",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    data = response.json()
    latest = data["deployments"][0]  # IndexError if deployments list is empty
    commit = latest["commits"][0]["sha"]  # nested unguarded collection access
    return {"deployment_id": latest["id"], "commit": commit}


# --- Triggers: unvalidated_external_response_field_access (EKU-a3c49422627f6bc0) ---
def sync_user_profile(user_id: str, api_token: str) -> dict:
    """Sync profile from external API — accesses fields without .get()."""
    response = requests.get(
        f"https://api.accounts.com/users/{user_id}",
        headers={"Authorization": f"Bearer {api_token}"},
        timeout=30,
    )
    profile = response.json()
    return {
        "name": profile["display_name"],          # KeyError if missing
        "email": profile["contact"]["email"],      # KeyError on nested access
        "tier": profile["subscription"]["tier"],   # KeyError if no subscription
        "org_id": profile["organization"]["id"],
    }


# --- Triggers: unvalidated_external_function_return_structure (EKU-b30c4719667a80c0) ---
def process_webhook_event(event_payload: dict) -> dict:
    """Process webhook — accesses return value structure without validation."""
    parsed = parse_event_body(event_payload.get("body", ""))
    event_type = parsed["type"]          # KeyError if parse returned wrong shape
    entity_id = parsed["data"]["id"]     # nested unguarded access
    actions = parsed["actions"]
    first_action = actions[0]["name"]    # IndexError if actions empty
    return {"event_type": event_type, "entity_id": entity_id, "action": first_action}


# --- Triggers: unvalidated_external_json_schema (EKU-62b0e258944d7d0e) ---
def ingest_partner_feed(feed_url: str) -> List[dict]:
    """Ingest partner data feed — parses JSON and accesses without schema check."""
    response = requests.get(feed_url, timeout=60)
    feed = json.loads(response.text)
    items = []
    for entry in feed["results"]:         # KeyError if no "results" key
        item = {
            "sku": entry["product"]["sku"],
            "price": entry["pricing"]["amount"],
            "currency": entry["pricing"]["currency"],
            "warehouse": entry["fulfillment"]["warehouse_id"],
        }
        items.append(item)
    return items


# --- Triggers: unvalidated_tuple_unpack_from_fallible_helper (EKU-c2053f23717e6ed8) ---
def run_analysis_pipeline(data_path: str) -> dict:
    """Run analysis — unpacks tuple from helper that can return None."""
    header, rows, metadata = load_and_parse_csv(data_path)  # ValueError if returns None
    column_names = header.split(",")
    total_rows = len(rows)
    source = metadata["source"]          # also unguarded dict access
    return {"columns": column_names, "row_count": total_rows, "source": source}


# --- Triggers: parameter_position_mismatch_with_type_coercion (EKU-046f1a400ec22342) ---
def create_alert(severity: str, threshold: int, channel_id: str) -> dict:
    """Create monitoring alert — callers swap parameter positions."""
    return {
        "severity": severity,
        "threshold": threshold,
        "channel_id": channel_id,
    }

def setup_monitoring(config: dict):
    """Sets up monitoring — passes args in wrong order to create_alert."""
    return create_alert(
        config["channel"],     # str but this is channel_id, not severity
        config["severity"],    # str but position expects int threshold
        config["threshold"],   # int but position expects str channel_id
    )


# --- Helper stubs (would be real in production) ---
def allocate_memory(size):
    pass

def parse_event_body(body: str) -> dict:
    return json.loads(body) if body else {}

def load_and_parse_csv(path: str):
    pass
