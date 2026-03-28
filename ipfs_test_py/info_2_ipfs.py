#!/usr/bin/env python3
import argparse
import json
import requests
from eth_abi import encode
from web3 import Web3

IPFS_API = "http://127.0.0.1:5001/api/v0"

def parse_args():
    parser = argparse.ArgumentParser(
        prog="Identity credential helper"
    )
    parser.add_argument('--firstName', '-f', required=True)
    parser.add_argument('--lastName',  '-l', required=True)
    parser.add_argument('--dob',       '-d', required=True)
    return parser.parse_args()

def upload_to_ipfs(firstName, lastName, dob):
    document = json.dumps({
        "firstName": firstName,
        "lastName":  lastName,
        "dob":       dob
    })
    response = requests.post(
        f"{IPFS_API}/add",
        files={"file": document.encode()}
    )
    return response.json()["Hash"]

def compute_credential_hash(firstName, lastName, dob):
    encoded = encode(['string', 'string', 'string'], [firstName, lastName, dob])
    return Web3.keccak(encoded)

def main():
    args = parse_args()

    cid = upload_to_ipfs(args.firstName, args.lastName, args.dob)
    credential_hash = compute_credential_hash(args.firstName, args.lastName, args.dob)

    print("\n--- Paste these into Remix ---")
    print(f"credentialHash:  0x{credential_hash.hex()}")
    print(f"ipfsCID:         {cid}")
    print(f"\n--- Sign this in Remix ---")
    print(f"Paste into Remix Sign field: 0x{credential_hash.hex()}")

if __name__ == "__main__":
    main()