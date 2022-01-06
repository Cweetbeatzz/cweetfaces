//SPDX-License-Identifier:MIT

pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract CweetFaces is ERC721, VRFConsumerBase {
    //#########################################################

    uint256 public tokenCounter;
    bytes32 public KeyHash;
    uint256 public Fee;
    enum FACES {
        red,
        blue,
        black,
        white
    }
    mapping(uint256 => FACES) public tokenIdToFace;
    mapping(bytes32 => address) public requestIdToSender;
    event requestCollect(bytes32 indexed requestId, address requester);
    event faceAssigned(uint256 indexed tokenId, FACES faces);

    //#########################################################

    constructor(
        address _vrfCoordinator,
        address _link,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        ERC721("PUPPYPUPPET", "PYPT")
        VRFConsumerBase(_vrfCoordinator, _link)
    {
        tokenCounter = 0;
        KeyHash = _keyhash;
        Fee = _fee;
    }

    //#########################################################
    function CreateCollectables() public returns (bytes32) {
        bytes32 requestId = requestRandomness(KeyHash, Fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestCollect(requestId, msg.sender);
    }

    //#########################################################

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        FACES faces = FACES(randomness % 4);
        uint256 newTokenid = tokenCounter;
        tokenIdToFace[newTokenid] = faces;
        emit faceAssigned(newTokenid, faces);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenid);
        tokenCounter += 1;
    }

    //#########################################################

    function setTokenURI(uint256 tokenId, string memory tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "Caller is not Approved or Owner"
        );
        _setTokenURI(tokenId, tokenURI);
    }
}
