// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../../node_modules/@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "../../node_modules/@openzeppelin/contracts/access/Ownable.sol";

contract IoTAccessNFT is ERC721URIStorage, Ownable {
    uint256 private _tokenIds;

    struct Access {
        address delegatee;
        uint256 expiresAt; // Timestamp de expiração da permissão
    }

    // Mapeamento de NFT para permissões delegadas
    mapping(uint256 => Access) public accessControl;

    constructor(
        address initialOwner
    ) ERC721("IoTAccessNFT", "IOTNFT") Ownable(initialOwner) {}

    // Função para criar um NFT associado a um dispositivo IoT
    function mintNFT(
        address recipient,
        string memory _tokenURI
    ) public onlyOwner returns (uint256) {
        _tokenIds++;
        uint256 newItemId = _tokenIds;
        _mint(recipient, newItemId);
        _setTokenURI(newItemId, _tokenURI);
        return newItemId;
    }

    // Função para delegar acesso temporário a outro usuário
    function delegateAccess(
        uint256 tokenId,
        address delegatee,
        uint256 duration
    ) public {
        require(
            ownerOf(tokenId) == msg.sender,
            "Somente o dono pode delegar acesso"
        );
        require(delegatee != address(0), "Delegado invalido");
        accessControl[tokenId] = Access(delegatee, block.timestamp + duration);
    }

    // Função para verificar se um usuário tem acesso ao dispositivo
    function hasAccess(
        uint256 tokenId,
        address user
    ) public view returns (bool) {
        if (ownerOf(tokenId) == user) {
            return true; // O dono do NFT tem acesso
        }
        Access memory access = accessControl[tokenId];
        // Adiciona uma margem de segurança ao usar block.timestamp
        uint256 safeTimestamp = block.timestamp + 30;
        if (access.delegatee == user && safeTimestamp < access.expiresAt) {
            return true; // Usuário delegado ainda tem acesso válido
        }
        return false;
    }

    // Função para revogar acesso antes do tempo de expiração
    function revokeAccess(uint256 tokenId) public {
        require(ownerOf(tokenId) == msg.sender, "Somente o dono pode revogar");
        delete accessControl[tokenId];
    }
}
