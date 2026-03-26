// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

import "./identity.sol";

contract Verifier {
    function verify(address identityAddress, address expectedOwner) public view returns (bool) {
        address reportedOwner = IIdentity(identityAddress).owner();
        return reportedOwner == expectedOwner;
    }
}


