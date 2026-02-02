# Witness Failover Monitor (Automated Protection)

This script provides an automated failover mechanism for Blurt witnesses. It monitors your account via public RPC nodes and, if a missed block is detected, it immediately broadcasts a `witness_update` transaction to disable your node.

## Why use this?

When a witness node goes offline or hangs, it starts missing blocks. This can lead to a significant drop in witness ranking. By automatically disabling the witness (setting the signing key to a null key), you stop being scheduled for blocks, preventing further "misses" until you can manually fix the issue and re-enable it.

## Prerequisites

- **Python 3.6+**
- **blurtpy**: `pip install blurtpy`
- **python-dotenv**: `pip install python-dotenv`

## Installation

1. Download the script [witness_failover.py](../scripts/witness_failover.py).
2. Create a `.env` (or `secrets.env`) file with your **Private Active Key**:
   ```
   BLURT_ACTIVE_KEY=5YourPrivateActiveKey...
   ```
3. Edit the top of the script to set your witness name:
   ```python
   WITNESS_NAME = "your_account_name"
   WITNESS_URL = "https://your.website.url"
   ```

## Usage

Run the script in the background using `nohup` or a systemd service:

```bash
nohup python3 witness_failover.py > failover.log 2>&1 &
```

## How it Works

The script performs the following steps:
1. Connects to established public RPC nodes.
2. Fetches the initial `total_missed` count for your witness account.
3. Every 10 seconds, it fetches the current count.
4. If `current_missed > initial_missed`, it triggers the `disable_witness` function.
5. The function broadcasts a `witness_update` using the **Null Key**: `BLT1111111111111111111111111111111114T1Anm`.

> [!WARNING]
> This script requires your **Active Private Key** to broadcast the update. Ensure you run it in a secure environment.
