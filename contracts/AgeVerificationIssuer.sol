// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

contract Identity {
    address public owner;

    uint256 private credentialCount;

    event credentialIssued(address credentialAddress);
    event credentialRevoked(bool revocationStatus, string responseMessage);

    constructor(address _owner) {
        owner = _owner;
    }

    function issueCredential(string calldata firstName, string calldata lastName, string calldata dob) public returns (bool) {
        // if credentialIssued() == True:
        //      emit credentialIssued()
        //      credentialCount=+1
    }

    function revokeCredential(address identityAddress) public returns (bool) {
        // if credentialRevoked() == True:
        //      emit credentialRevoked()
        //      credentialCount=-1, maybe not decrement?
    }

}
