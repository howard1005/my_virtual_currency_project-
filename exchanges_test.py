import unittest   # The test framework

import ccxt
from market import Market
from exchange import Exchange
from exchanges import Exchanges
from exchanges_config import ExchangeConfig


class ExchangeTest(unittest.TestCase):

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

    def test_refresh(self):
        self.exchanges.refresh()
        for exchange in self.exchanges.get_exchanges_list():
            for market in exchange.get_markets_list():
                self.assertIsNotNone(market.get_order_book())

    def test_get_deposit_address(self):
        for exchange in self.exchanges.get_exchanges_list():
            address = exchange.get_deposit_address_by_currency_name('IOTA')
            print(address)

    def test_get_transactions(self):
        for exchange in self.exchanges.get_exchanges_list():
            transactions = exchange.get_deposit_transactions_by_currency_name(
                'IOTA')
            print(transactions)
        for exchange in self.exchanges.get_exchanges_list():
            transactions = exchange.get_withdrawal_transactions_by_currency_name(
                'IOTA')
            print(transactions)

    def test_check_transfer(self):
        exchanges_list = self.exchanges.get_exchanges_list()
        for i in range(0, len(exchanges_list)):
            for j in range(0, len(exchanges_list)):
                exchange1,exchange2= '{}'.format(exchanges_list[i]),'{}'.format(exchanges_list[j])
                print(exchange1,exchange2)
                chk = self.exchanges.check_transfer_currency(
                    'REP', exchange1, exchange2)
                print(chk)


if __name__ == '__main__':
    unittest.main()
