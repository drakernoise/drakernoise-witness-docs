import requests
import json

RPC_URL = "https://rpc.drakernoise.com"
ACCOUNT = "drakernoise"

def get_account_history():
    payload = {
        "jsonrpc": "2.0",
        "method": "condenser_api.get_account_history",
        "params": [ACCOUNT, -1, 10],  # Get last 10 transactions
        "id": 1
    }
    
    try:
        response = requests.post(RPC_URL, json=payload)
        result = response.json()
        
        print(f"--- Last 10 Transactions for {ACCOUNT} ---")
        for tx in result.get('result', []):
            tx_id = tx[0]
            op = tx[1]['op']
            timestamp = tx[1]['timestamp']
            print(f"[{timestamp}] ID: {tx_id} | OP: {op[0]}")
            
    except Exception as e:
        print(f"RPC Error: {e}")

if __name__ == "__main__":
    get_account_history()
