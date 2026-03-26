// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

contract Identity {
    address public owner;

    constructor(address _owner) {
        owner = _owner;
    }
}

