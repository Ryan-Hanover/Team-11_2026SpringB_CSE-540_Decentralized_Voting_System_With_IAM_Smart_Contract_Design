"""Shared helpers for terminal-based IAM age-verification demo CLIs."""

from __future__ import annotations
from dataclasses import dataclass
from web3 import Web3
# TODO: import additional necessary packages

IPFS_API = "http://127.0.0.1:5001/api/v0"

DID_REGISTRY_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "documentHash", "type": "bytes32"}],
        "name": "registerDID",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "holderAddress", "type": "address"}],
        "name": "isDIDActive",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]

@dataclass
class ChainContext:
    web3: Web3
    account: str

# TODO: add common data structures


def prompt_non_empty(label: str, secret: bool = False) -> str:
    while True:
        value = getpass(label) if secret else input(label)
        value = value.strip()
        if value:
            return value
        print("Input cannot be empty.")


def prompt_optional(label: str, default: str) -> str:
    value = input(f"{label} [{default}]: ").strip()
    return value or default


def connect_chain_with_account() -> ChainContext:
    rpc_url = prompt_optional("RPC URL", "http://127.0.0.1:8545")
    private_key = prompt_non_empty("Private key (0x...): ", secret=True)

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise RuntimeError(f"Could not connect to RPC at {rpc_url}")

    account = web3.eth.account.from_key(private_key)
    return ChainContext(web3=web3, account=account)


def prompt_contract_address(web3: Web3, label: str) -> str:
    address = prompt_non_empty(f"{label} address: ")
    return web3.to_checksum_address(address)

def prompt_did_document_hash() -> tuple[bytes, str]:
    pass
    # TODO: implement standardized prompt flow for DID document hash

def send_contract_transaction(web3: Web3, account: object, fn_call) -> object:
    tx = fn_call.build_transaction(
        {
            "from": account.address,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gas": 300000,
            "gasPrice": web3.eth.gas_price,
            "chainId": web3.eth.chain_id,
        }
    )
    signed = web3.eth.account.sign_transaction(tx, account.key)
    tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
    return web3.eth.wait_for_transaction_receipt(tx_hash)

# TODO: add common functions for