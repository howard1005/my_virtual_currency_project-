import unittest   # The test framework

import ccxt
from market import Market
from exchange import Exchange
from exchanges import Exchanges
from exchanges_config import ExchangeConfig


class MarketTest(unittest.TestCase):

    def setUp(self):
        self.exchanges_config = ExchangeConfig().get_config()
        self.exchanges = Exchanges()
        for name, config in self.exchanges_config.items():
            ccxt_exchange = getattr(ccxt, name)(config)
            self.exchanges.add_exchange(Exchange(ccxt_exchange, [Market(ccxt_exchange, ccxt_market)
                                                                 for ccxt_market in ccxt_exchange.load_markets().values()]))
        print(self.exchanges)

    def test_init(self):
        pass

    def test_calculate_quantity(self):
        for exchange in self.exchanges.get_exchanges_list():
            for market in exchange.get_markets_list():
                if market.get_symbol() == 'BTC/KRW':
                    market.refresh()
                    print(market.calculate_quantity_base_by_quote(1))
                    print(market.calculate_quantity_quote_by_base(0.029))


if __name__ == '__main__':
    unittest.main()
