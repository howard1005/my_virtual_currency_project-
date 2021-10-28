from market import Market
from exchange import Exchange
from exchanges import Exchanges
from currency_node import CurrencyNode
from currency_graph import CurrencyGraph
from exchanges_config import ExchangeConfig

import unittest   # The test framework
import ccxt
import sys


class CurrencyGraphTest(unittest.TestCase):

    def setUp(self):
        # exchange setup
        self.exchanges_config = ExchangeConfig().get_config()
        self.exchanges = Exchanges()
        for name, config in self.exchanges_config.items():
            ccxt_exchange = getattr(ccxt, name)(config)
            self.exchanges.add_exchange(Exchange(ccxt_exchange, [Market(ccxt_exchange, ccxt_market)
                                                                 for ccxt_market in ccxt_exchange.load_markets().values()]))
        print(self.exchanges)
        # graph setup
        currency_names = []
        for exchange in self.exchanges.get_exchanges_list():
            currency_names += [currency_name for currency_name in exchange.get_all_currencies()]
        unique_currency_names = list(set(currency_names))
        #print(unique_currency_names)
        self.currency_graph = CurrencyGraph(self.exchanges, [CurrencyNode(
            self.exchanges, currency_name) for currency_name in unique_currency_names])
        print(self.currency_graph)

    def test_init(self):
        pass

    def test_refresh_edges(self):
        self.currency_graph.init_nodes()
        for currency_node in self.currency_graph.get_node_list():
            print('currency_name :', currency_node.get_currency_name())
            edges_map = currency_node.get_edges_map()
            print(edges_map)
            self.assertIsNotNone(edges_map)

    def test_search_best_path(self):
        self.test_refresh_edges()
        best_path = self.currency_graph.search_best_path('Upbit', 'KRW', 1000000.0, max_path_len=10)
        print(best_path)
        element_list = best_path[1]
        if element_list:
            print('[{}][{}] best_path : {}'.format(self.__class__.__name__, sys._getframe(
            ).f_code.co_name, [(element[0].currency_name, element[1], '{}'.format(element[2])) for element in element_list]))


if __name__ == '__main__':
    unittest.main()
