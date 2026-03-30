#!/usr/bin/env python3
"""Build an identity credential for Remix: upload JSON to IPFS and derive a Keccak hash.

Expects a local IPFS node with its HTTP API enabled (default ``127.0.0.1:5001``).
The credential hash is the Keccak-256 digest of ABI-encoded ``(string, string, string)``
for ``(firstName, lastName, dob)``, matching typical Solidity ``keccak256(abi.encode(...))``
usage for the same three strings.
"""
import argparse
import json
import requests
from eth_abi import encode
from web3 import Web3

# Base URL for the Kubo (go-ipfs) HTTP API ``/api/v0`` endpoints.
IPFS_API = "http://127.0.0.1:5001/api/v0"


def parse_args():
    """Parse CLI arguments for identity fields.

    Returns:
        argparse.Namespace: Parsed arguments with ``firstName``, ``lastName``, and ``dob``.
    """
    parser = argparse.ArgumentParser(
        prog="Identity credential helper"
    )
    parser.add_argument('--firstName', '-f', required=True)
    parser.add_argument('--lastName',  '-l', required=True)
    parser.add_argument('--dob',       '-d', required=True)
    return parser.parse_args()


def upload_to_ipfs(firstName, lastName, dob):
    """Upload a JSON document with identity fields to IPFS via the HTTP API.

    Args:
        firstName: Given name.
        lastName: Family name.
        dob: Date of birth string.

    Returns:
        str: The IPFS content identifier (CID / multihash hex from the ``add`` response ``Hash`` field).
    """
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
    """Compute Keccak-256 over ABI-encoded (string, string, string).

    Args:
        firstName: Given name (must match the strings used on-chain).
        lastName: Family name.
        dob: Date of birth string.

    Returns:
        bytes: 32-byte Keccak digest (use ``.hex()`` for ``0x``-prefixed hex in Remix).
    """
    encoded = encode(['string', 'string', 'string'], [firstName, lastName, dob])
    return Web3.keccak(encoded)


def main():
    """Parse args, upload to IPFS, print credential hash and CID for Remix."""
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