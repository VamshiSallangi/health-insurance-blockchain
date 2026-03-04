// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract HealthInsurance {
    struct Claim {
        string claimId;
        string patientName;
        uint256 age;
        string gender;
        string hospital;
        string diagnosis;
        uint256 claimAmount;
        string dateOfService;
        uint256 timestamp;
    }

    Claim[] public claims;
    event ClaimAdded(string claimId, string patientName, uint256 claimAmount, uint256 index);

    function addClaim(
        string memory _claimId,
        string memory _patientName,
        uint256 _age,
        string memory _gender,
        string memory _hospital,
        string memory _diagnosis,
        uint256 _claimAmount,
        string memory _dateOfService
    ) public {
        Claim memory c = Claim({
            claimId: _claimId,
            patientName: _patientName,
            age: _age,
            gender: _gender,
            hospital: _hospital,
            diagnosis: _diagnosis,
            claimAmount: _claimAmount,
            dateOfService: _dateOfService,
            timestamp: block.timestamp
        });
        claims.push(c);
        emit ClaimAdded(_claimId, _patientName, _claimAmount, claims.length - 1);
    }

    function getClaim(uint256 index) public view returns (
        string memory, string memory, uint256, string memory, string memory, string memory, uint256, string memory, uint256
    ) {
        Claim storage c = claims[index];
        return (
            c.claimId,
            c.patientName,
            c.age,
            c.gender,
            c.hospital,
            c.diagnosis,
            c.claimAmount,
            c.dateOfService,
            c.timestamp
        );
    }

    function getTotalClaims() public view returns (uint256) {
        return claims.length;
    }
}
