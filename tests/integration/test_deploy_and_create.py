from brownie import CweetFaces, network
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
import pytest
from scripts.deploy import deploy_and_create
import time


def test_deploy_and_create_integration():
    account = get_account()
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    testing, creating_transaction = deploy_and_create()
    time.sleep(60)

    # Assert
    assert testing.tokenCounter() == 1
