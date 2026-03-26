// SPDX-License-Identifier: MIT
pragma solidity 0.8.30;

interface IIdentity {
    function owner() external view returns (address);
}