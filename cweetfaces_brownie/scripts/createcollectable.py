from brownie import CweetFaces, network
from web3.main import Web3
from ..scripts.helpers import get_account, fund_with_link


def deploy_create_collectable():
    account = get_account()
    prev_transaction = CweetFaces[-1]
    fund_with_link(prev_transaction.address, amount=Web3.toWei(0.1, "ether"))
    next_transaction = prev_transaction.CreateCollectables({"from": account})
    next_transaction.wait(1)
    print("Successfull")


def main():
    deploy_create_collectable()
