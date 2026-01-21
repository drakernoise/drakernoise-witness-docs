import requests
import json

RPC_URL = "https://rpc.drakernoise.com"

def get_dynamic_global_properties():
    payload = {
        "jsonrpc": "2.0",
        "method": "condenser_api.get_dynamic_global_properties",
        "params": [],
        "id": 1
    }
    
    try:
        response = requests.post(RPC_URL, json=payload)
        result = response.json()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"RPC Error: {e}")

if __name__ == "__main__":
    get_dynamic_global_properties()
