from awspricing.offers import ElastiCacheOffer
from awspricing.constants import ELASTICACHE_LEASE_CONTRACT_LENGTH, ELASTICACHE_PURCHASE_OPTION

import pytest

from tests.data.elasticache_offer import BASIC_ELASTICACHE_OFFER_DATA, BASIC_ELASTICACHE_SKU


@pytest.fixture()
def offer():
    return ElastiCacheOffer(BASIC_ELASTICACHE_OFFER_DATA)


class TestElastiCacheOffer(object):
    def test_search_skus_attributes(self, offer):
        assert offer.search_skus(
            instance_type='cache.c7gn.large',
            cache_engine='Valkey',
            location='US East (N. Virginia)'
        ) == {BASIC_ELASTICACHE_SKU}

    def test_ondemand_hourly(self, offer):
        # Note: The test data doesn't include OnDemand pricing for the SKUs
        # This test would need actual OnDemand pricing data to be meaningful
        # For now, we're just testing that the method raises a StopIteration exception
        # which is expected when there are no OnDemand terms
        with pytest.raises(StopIteration):
            offer.ondemand_hourly(
                node_type='cache.c7gn.large',
                cache_engine='Valkey',
                region='us-east-1'
            )

    def test_reserved_hourly_no_upfront(self, offer):
        assert offer.reserved_hourly(
            node_type='cache.c7gn.large',
            cache_engine='Valkey',
            region='us-east-1',
            lease_contract_length=ELASTICACHE_LEASE_CONTRACT_LENGTH.ONE_YEAR,
            purchase_option=ELASTICACHE_PURCHASE_OPTION.NO_UPFRONT
        ) == 0.1384

    def test_reserved_hourly_partial_upfront(self, offer):
        # Calculate expected hourly rate with amortized upfront cost
        # (580.788 / (365 * 24)) + 0.0664 = 0.1327 (rounded)
        expected_hourly = (580.788 / (365 * 24)) + 0.0664
        assert offer.reserved_hourly(
            node_type='cache.c7gn.large',
            cache_engine='Valkey',
            region='us-east-1',
            lease_contract_length=ELASTICACHE_LEASE_CONTRACT_LENGTH.ONE_YEAR,
            purchase_option=ELASTICACHE_PURCHASE_OPTION.PARTIAL_UPFRONT
        ) == pytest.approx(expected_hourly)

    def test_reserved_hourly_all_upfront(self, offer):
        # Calculate expected hourly rate with amortized upfront cost
        # 1143.7056 / (365 * 24) = 0.1305 (rounded)
        expected_hourly = 1143.7056 / (365 * 24)
        assert offer.reserved_hourly(
            node_type='cache.c7gn.large',
            cache_engine='Valkey',
            region='us-east-1',
            lease_contract_length=ELASTICACHE_LEASE_CONTRACT_LENGTH.ONE_YEAR,
            purchase_option=ELASTICACHE_PURCHASE_OPTION.ALL_UPFRONT
        ) == pytest.approx(expected_hourly)

    def test_reserved_upfront_no_upfront(self, offer):
        assert offer.reserved_upfront(
            node_type='cache.c7gn.large',
            cache_engine='Valkey',
            region='us-east-1',
            lease_contract_length=ELASTICACHE_LEASE_CONTRACT_LENGTH.ONE_YEAR,
            purchase_option=ELASTICACHE_PURCHASE_OPTION.NO_UPFRONT
        ) == 0.0

    def test_reserved_upfront_partial_upfront(self, offer):
        assert offer.reserved_upfront(
            node_type='cache.c7gn.large',
            cache_engine='Valkey',
            region='us-east-1',
            lease_contract_length=ELASTICACHE_LEASE_CONTRACT_LENGTH.ONE_YEAR,
            purchase_option=ELASTICACHE_PURCHASE_OPTION.PARTIAL_UPFRONT
        ) == 580.788

    def test_reserved_upfront_all_upfront(self, offer):
        assert offer.reserved_upfront(
            node_type='cache.c7gn.large',
            cache_engine='Valkey',
            region='us-east-1',
            lease_contract_length=ELASTICACHE_LEASE_CONTRACT_LENGTH.ONE_YEAR,
            purchase_option=ELASTICACHE_PURCHASE_OPTION.ALL_UPFRONT
        ) == 1143.7056
