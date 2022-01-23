from brownie import CweetFaces, network
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
import pytest
from scripts.deploy import deploy_and_create


def test_deploy_and_create():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    testing, creating_transaction = deploy_and_create()
    requestId = creating_transaction.events["requestCollect"]["requestId"]
    random_number = 345
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 345, testing.address, {"from": account}
    )
    # Assert
    assert testing.tokenCounter() == 1
    assert testing.tokenIdToFace(0) == random_number % 4
