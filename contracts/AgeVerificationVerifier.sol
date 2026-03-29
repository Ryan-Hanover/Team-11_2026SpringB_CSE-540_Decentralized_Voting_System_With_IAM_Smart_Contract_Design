// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

// Interface to interact with the trusted Issuer contract
interface IIssuer {
     function verify(bytes32 credentialHash, string calldata cid, bytes calldata signature) external view returns (bool);
}

// Interface for the Decentralized Identity (DID) Registry
interface IDIDRegistry {function isDIDActive(address holderAddress) external view returns (bool);}

/**
 * @title AgeVerificationVerifier
 * @dev This contract represents the "Verifier" (Election Official) in our 3-entity design.
 * Their interface is only used to scan and verify voter credentials on the blockchain.
 */
contract Verifier {
    address public owner;
    IIssuer private issuer;
    IDIDRegistry private didRegistry;

    constructor(address issuerAddress, address didAddress) {
        owner = msg.sender;
        issuer = IIssuer(issuerAddress);
        didRegistry = IDIDRegistry(didAddress);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    /**
     * @dev Scans the presented proof and verifies it on the blockchain.
     * The verifier checks if the voter's credential is valid AND above 18.
     * By calling the Issuer contract, the verifier only learns true or false 
     * and nothing else thereby successfully mitigating excessive personal data disclosure.
     */
    function verify(bytes32 credentialHash, string calldata cid, bytes calldata signature) external view onlyOwner returns (bool) {
        return issuer.verify(credentialHash, cid, signature);
    }
}