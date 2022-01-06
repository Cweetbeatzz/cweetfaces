from brownie import network, CweetFaces
from scripts.helpers import OPENSEA_URL, get_face, get_account


def main():
    print(f"Working on {network.show_active()}")
    prev_transcation = CweetFaces[-1]
    number_of_collectibles = prev_transcation.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        face = get_face(prev_transcation.tokenIdToFace(token_id))
        if not prev_transcation.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, prev_transcation, dog_metadata_dic[face])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Great! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
