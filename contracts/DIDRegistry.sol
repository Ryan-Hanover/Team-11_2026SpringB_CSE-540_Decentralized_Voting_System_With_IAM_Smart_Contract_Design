// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DIDRegistry {
    struct DIDEntry {
        address holder;
        bytes32 documentHash;
        bool isActive;
    }

    mapping(address => DIDEntry) private didEntries;

    event DIDRegistered(address indexed holder, bytes32 indexed documentHash);
    event DIDDeactivated(address indexed holder);

    modifier onlyHolder(address holderAddress) {
        require(didEntries[holderAddress].holder == msg.sender, "Not authorized");
        _;
    }

    modifier didExists(address holderAddress) {
        require(didEntries[holderAddress].holder != address(0), "DID does not exist");
        _;
    }

    function registerDID(bytes32 documentHash) external {
        require(didEntries[msg.sender].holder == address(0), "DID already exists");
        require(documentHash != bytes32(0), "Invalid document hash");

        didEntries[msg.sender] = DIDEntry({
            holder: msg.sender,
            documentHash: documentHash,
            isActive: true
        });

        emit DIDRegistered(msg.sender, documentHash);
    }

    
    function deactivateDID() external didExists(msg.sender)
    {
        didEntries[msg.sender].isActive = false;
        emit DIDDeactivated(msg.sender);
    }

    function isDIDActive(address holderAddress) external view returns (bool) {
        DIDEntry memory entry = didEntries[holderAddress];
        return entry.isActive;
    }

    function getDID(address holderAddress) external view didExists(holderAddress) returns (address holder, bytes32 documentHash, bool active)
    {
        DIDEntry memory entry = didEntries[holderAddress];
        return (entry.holder, entry.documentHash, entry.isActive);
    }
}