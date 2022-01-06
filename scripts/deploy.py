from brownie import CweetFaces, config, network
from .helpers import get_account, get_contract, fund_with_link


def deploy_and_create():
    account = get_account()
    deploy_contract = CweetFaces.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(deploy_contract.address)  # funding address
    creating_transaction = deploy_contract.CreateCollectables({"from": account})
    creating_transaction.wait(1)
    print("Contract Deployed & Created Suuccessfully")
    print(f"Contract Address:{deploy_contract.address}")
    return deploy_contract, creating_transaction


def main():
    deploy_and_create()
