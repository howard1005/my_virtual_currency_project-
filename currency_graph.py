from exchange import Exchange
from exchanges import Exchanges
from market import Market
from currency_node import CurrencyNode
from collections import deque
import sys


class CurrencyGraph:
    def __init__(self, exchanges: Exchanges, currency_nodes: list[CurrencyNode]) -> None:
        self.exchanges = exchanges
        self.currency_nodes = currency_nodes
        self.currency_node_map = {}

    def init_nodes(self):
        for currency_node in self.currency_nodes:
            self.currency_node_map[currency_node.currency_name] = currency_node
        self.refresh_all_nodes()

    def refresh_all_nodes(self):
        for currency_node in self.currency_nodes:
            currency_node.refresh_edges()

    def get_node_list(self) -> list:
        return self.currency_nodes

    def _print_element_list(self, element_list: list):
        print('[{}][{}] element_list : {}'.format(self.__class__.__name__, sys._getframe(1).f_code.co_name, [
              (element[0].currency_name, element[1], '{}'.format(element[2])) for element in element_list]))

    def search_paths(self, exchange_name: str, currency_name: str, quantity: float, max_path_len: int = 5) -> list:
        [currency_node.set_quantity(0)
         for currency_node in self.currency_nodes]
        cur_node = self.currency_node_map[currency_name]
        cur_node.set_quantity(quantity)
        cur_market = self.exchanges.get_exchange_by_name(exchange_name).get_markets_list()[0]
        # [node, quantity, market]
        dq = deque([[(cur_node, cur_node.quantity, cur_market)]])
        paths = []
        while dq:
            element_list = dq.popleft()
            if len(element_list) >= max_path_len:
                continue
            self._print_element_list(element_list)

            cur_element = element_list[-1]
            (cur_node, cur_quantity, cur_market) = cur_element
            if cur_node.quantity > cur_quantity:
                continue
            cur_edges_map = cur_node.get_edges_map()
            for target_currency_name in cur_edges_map:
                (target_quantity, target_market) = cur_node.calculate_quantity_by_target_currency_name(
                    target_currency_name, cur_quantity, cur_market)
                if target_market == None:
                    continue
                target_currency = self.currency_node_map[target_currency_name]
                if target_currency.quantity >= target_quantity:
                    print("target {} {}>={}".format(target_currency,
                          target_currency.quantity, target_quantity))
                    continue
                target_currency.quantity = target_quantity
                next_element_list = element_list + \
                    [(target_currency, target_quantity, target_market)]
                dq.append(next_element_list)
                if target_currency.currency_name == currency_name:
                    print("add path {} {}".format(
                        target_currency, target_quantity))
                    paths.append([target_quantity, next_element_list])
        return paths

    def search_best_path(self, exchange_name: str, currency_name: str, quantity: float, max_path_len: int = 5) -> list:
        paths = self.search_paths(exchange_name, currency_name, quantity, max_path_len)
        sorted_paths = sorted(paths, key=lambda x: x[0])
        print("path print!!~~~~~~~!!")
        for path in sorted_paths:
            self._print_element_list(path[1])
        if sorted_paths:
            return sorted_paths[-1]
        return tuple(0.0,None)

    def make_command_by_path(self, path: list) -> dict:
        pass
