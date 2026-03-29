// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title DIDRegistry
 * @dev Manages the Decentralized Identifiers (DIDs) for users in the dApp system.
 * This acts as the foundational registry to ensure identities are active before 
 * issuing credentials or verifying proofs, reducing the risk of identity theft.
 */
contract DIDRegistry {
    // Represents a voter's decentralized identity record
    struct DIDEntry {
        address holder; // The Voter's wallet address
        bytes32 documentHash; // Hash of the underlying identity document
        bool isActive;
    }

    // Maps a voter's address to their identity entry
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

    /**
     * @dev Registers a new decentralized identity for a voter.
     * This simulates the foundational KYC verification process.
     */
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

    /**
     * @dev Allows a voter to deactivate if compromised.
     */
    function deactivateDID() external didExists(msg.sender)
    {
        didEntries[msg.sender].isActive = false;
        emit DIDDeactivated(msg.sender);
    }

    /**
     * @dev Used by the Issuer and Verifier contracts to ensure a voter's identity is currently valid.
     */
    function isDIDActive(address holderAddress) external view returns (bool) {
        DIDEntry memory entry = didEntries[holderAddress];
        return entry.isActive;
    }

    // Retrieves full DID information for front-end interface usage
    function getDID(address holderAddress) external view didExists(holderAddress) returns (address holder, bytes32 documentHash, bool active)
    {
        DIDEntry memory entry = didEntries[holderAddress];
        return (entry.holder, entry.documentHash, entry.isActive);
    }
}