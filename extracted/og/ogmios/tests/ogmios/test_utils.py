import pytest
from datetime import datetime
from pydantic.v1.error_wrappers import ValidationError

from tests.ogmios.test_fixtures import client

from ogmios.utils import GenesisParameters, get_current_era, wait_for_empty_mempool
from ogmios.datatypes import Era

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_GenesisParameters(client):
    for i in range(len(Era)):
        genesis = GenesisParameters(client, Era.by_index(i))
        assert hasattr(genesis, "genesis_delegations")
        assert hasattr(genesis, "genesis_key_hashes")
        assert hasattr(genesis, "initial_funds")
        assert hasattr(genesis, "initial_vouchers")
        assert hasattr(genesis, "start_time")
        assert hasattr(genesis, "updatable_parameters")
        if genesis.era == "byron":
            continue

        assert hasattr(genesis, "active_slots_coefficient")
        assert hasattr(genesis, "epoch_length")
        assert hasattr(genesis, "initial_delegates")
        assert hasattr(genesis, "initial_parameters")
        assert hasattr(genesis, "initial_stake_pools")
        assert hasattr(genesis, "max_kes_evolutions")
        assert hasattr(genesis, "max_lovelace_supply")
        assert hasattr(genesis, "security_parameter")
        assert hasattr(genesis, "slot_length")
        assert hasattr(genesis, "slots_per_kes_period")
        assert hasattr(genesis, "start_time")
        if genesis.era == "shelley":
            continue

        assert hasattr(genesis, "update_quorum")
        if genesis.era == "alonzo":
            continue

        assert hasattr(genesis, "constitution")
        assert hasattr(genesis, "constitutional_committee")
        if genesis.era == "conway":
            continue
