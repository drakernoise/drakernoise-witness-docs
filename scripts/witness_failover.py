from blurtpy import Blurt
from blurtpy.transactionbuilder import TransactionBuilder
from blurtbase.operations import Witness_update, Amount
from blurtgraphenebase.chains import known_chains
from blurtgraphenebase.objects import GrapheneObject, isArgsThisClass
from blurtgraphenebase.types import Uint32, Uint16, OrderedDict
import blurtbase.operations
import os
from dotenv import load_dotenv
import json
import time
import sys

# --- MONKEY PATCHING FOR BLURTPY COMPATIBILITY ---
import blurtgraphenebase.account
from blurtgraphenebase.account import PrivateKey as OriginalPrivateKey

class PatchedPrivateKey(OriginalPrivateKey):
    def __init__(self, wif=None, prefix=None):
        super(PatchedPrivateKey, self).__init__(wif if not wif else wif.strip())

blurtgraphenebase.account.PrivateKey = PatchedPrivateKey
import blurtpy.transactionbuilder
blurtpy.transactionbuilder.PrivateKey = PatchedPrivateKey

class BlurtWitnessProps(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", "BLT")
            props_structure = OrderedDict([
                ('account_creation_fee', Amount(kwargs["account_creation_fee"], prefix=prefix)),
                ('maximum_block_size', Uint32(kwargs["maximum_block_size"])),
            ])
            if "account_subsidy_budget" in kwargs:
                props_structure['account_subsidy_budget'] = Uint32(kwargs["account_subsidy_budget"])
            if "account_subsidy_decay" in kwargs:
                props_structure['account_subsidy_decay'] = Uint32(kwargs["account_subsidy_decay"])
            if "operation_flat_fee" in kwargs:
                props_structure['operation_flat_fee'] = Amount(kwargs["operation_flat_fee"], prefix=prefix)
            if "bandwidth_kbytes_fee" in kwargs:
                props_structure['bandwidth_kbytes_fee'] = Amount(kwargs["bandwidth_kbytes_fee"], prefix=prefix)
            if "proposal_fee" in kwargs:
                props_structure['proposal_fee'] = Amount(kwargs["proposal_fee"], prefix=prefix)
            super(BlurtWitnessProps, self).__init__(props_structure)

blurtgraphenebase.account.default_prefix = "BLT"
# --- END MONKEY PATCHING ---

# CONFIGURATION
WITNESS_NAME = "drakernoise" # Cambiar al nombre del testigo
WITNESS_URL = "https://drakernoise.com/blurt_witness/"
POLL_INTERVAL = 10 # Segundos entre comprobaciones
RPC_NODES = [
    "https://rpc.beblurt.com",
    "https://blurt-rpc.saboin.com",
    "https://rpc.dotwin1981.de",
    "https://rpc.drakernoise.com"
]
NULL_KEY = "BLT1111111111111111111111111111111114T1Anm"

def get_witness_info(blurt_instance, account):
    try:
        witness = blurt_instance.rpc.get_witness_by_account(account)
        return witness
    except Exception as e:
        print(f"⚠️ Error fetching witness info: {e}")
        return None

def disable_witness(blurt_instance, wif, witness_name, url):
    print(f"🔴 DESHABILITANDO TESTIGO {witness_name}...")
    try:
        op = Witness_update(
            **{
                "owner": witness_name,
                "url": url,
                "block_signing_key": NULL_KEY,
                "props": {
                    "account_creation_fee": "300.000 BLURT",
                    "maximum_block_size": 65536,
                    "account_subsidy_budget": 797,
                    "account_subsidy_decay": 347321,
                    "operation_flat_fee": "0.001 BLURT",
                    "bandwidth_kbytes_fee": "0.285 BLURT",
                    "proposal_fee": "1000.000 BLURT"
                },
                "fee": "0.000 BLURT",
                "prefix": "BLT"
            }
        )
        tx = TransactionBuilder(blockchain_instance=blurt_instance)
        tx.appendOps([op])
        tx.appendWif(wif.strip())
        tx.sign()
        response = tx.broadcast()
        print(f"✅ Transacción enviada: {response}")
        return True
    except Exception as e:
        print(f"❌ Error al deshabilitar testigo: {e}")
        return False

def main():
    print("🛡️ Blurt Witness Failover Monitor")
    print("---------------------------------")
    
    env_path = "secrets.env"
    load_dotenv(env_path)
    wif = os.getenv("BLURT_ACTIVE_KEY")
    
    if not wif:
        print("❌ Error: BLURT_ACTIVE_KEY no encontrada en secrets.env")
        return

    b = Blurt(node=RPC_NODES)
    print(f"📡 Conectado a RPC: {b.rpc.url}")
    
    witness = get_witness_info(b, WITNESS_NAME)
    if not witness:
        print(f"❌ No se pudo encontrar al testigo '{WITNESS_NAME}'")
        return
    
    initial_missed = int(witness.get("total_missed", 0))
    print(f"📊 Monitoreando {WITNESS_NAME}. Missed inicial: {initial_missed}")
    
    try:
        while True:
            witness = get_witness_info(b, WITNESS_NAME)
            if witness:
                current_missed = int(witness.get("total_missed", 0))
                if current_missed > initial_missed:
                    print(f"‼️ ¡BLOQUE PERDIDO DETECTADO! (Anterior: {initial_missed}, Actual: {current_missed})")
                    if disable_witness(b, wif, WITNESS_NAME, WITNESS_URL):
                        print("📴 Testigo deshabilitado preventivamente.")
                        break
                    else:
                        print("⚠️ Reintentando deshabilitar en la próxima iteración...")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] OK - Missed: {current_missed}", end="\r")
            
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Monitor detenido por el usuario.")

if __name__ == "__main__":
    main()
