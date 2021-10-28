from exchange import Exchange
from exchanges import Exchanges
from market import Market
from collections import defaultdict


class CurrencyNode:
    def __init__(self, exchanges: Exchanges, currency_name: str) -> None:
        self.exchanges = exchanges
        self.currency_name = currency_name
        self.now_exchange = None
        self.quantity = 0
        # {target currency : [market1, market2,...]}
        self.edges_map = defaultdict(list)

    def __str__(self):
        return self.currency_name

    def refresh_edges(self):  # 거래소간 이동인지 확인하여 입출 가능한지 확인해야함
        for exchange in self.exchanges.get_exchanges_list():
            for market in exchange.get_markets_list():
                quote, base = market.get_quote(), market.get_base()
                if self.currency_name == quote:
                    self.edges_map[base].append(market)
                elif self.currency_name == base:
                    self.edges_map[quote].append(market)

    def get_currency_name(self) -> str:
        return self.currency_name

    def get_edges_map(self) -> defaultdict(list):
        return self.edges_map

    def set_quantity(self, quantity):
        self.quantity = quantity

    def calculate_quantity_by_target_currency_name(self, target_currency_name: str, my_quantity: float, my_market: Market) -> (float, Market):
        available_markets = self.edges_map[target_currency_name]
        quantitys = []
        for available_market in available_markets:
            quote, base = available_market.get_quote(), available_market.get_base()
            # 거래소간 이동인지 확인하여 입출 가능한지 확인해야함
            
            if False == self.exchanges.check_transfer_currency(self.currency_name, my_market.get_exchange_name(), available_market.get_exchange_name()):
               continue
            available_market.refresh_order_book()  # 호가창 refresh
            if self.currency_name == quote:
                quantitys.append(
                    (available_market.calculate_quantity_base_by_quote(my_quantity), available_market))
            elif self.currency_name == base:
                quantitys.append(
                    (available_market.calculate_quantity_quote_by_base(my_quantity), available_market))
        if not quantitys:
            return (0.0, None)
        return max(quantitys, key=lambda x: x[0])
