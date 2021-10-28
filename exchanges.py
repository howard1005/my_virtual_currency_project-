from market import Market
from exchange import Exchange
import asyncio


class Exchanges:
    def __init__(self, exchanges: list[Exchange] = []) -> None:
        self.exchanges = exchanges
        self.exchanges_map = self._get_exchanges_map()

    def __str__(self):
        return '{}'.format(self.exchanges)

    def __len__(self):
        return len(self.exchanges)

    def __getitem__(self, key):
        if type(key) == type(''):
            return self.exchanges_map[key]
        else:
            return self.exchanges[key]

    def __iter__(self):
        return iter(self.exchanges)

    def _get_exchanges_map(self):
        exchanges_map = {}
        for exchange in self.exchanges:
            exchanges_map['{}'.format(exchange)] = exchange
        return exchanges_map

    def add_exchange(self, exchange: Exchange):
        self.exchanges.append(exchange)
        self.exchanges_map['{}'.format(exchange)] = exchange

    def get_exchanges_list(self) -> list:
        return self.exchanges

    def get_exchange_by_name(self, exchange_name: str) -> Exchange:
        return self.exchanges_map[exchange_name]

    def refresh(self):
        self.refresh_all_exchanges()

    def refresh_all_exchanges(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(
            *[exchange.refresh_all_markets() for exchange in self.exchanges]))
        #for exchange in self.exchanges:
        #exchange.refresh_all_markets()

    def transfer_currency(self, currency_name: str, exchange1_name: str, exchange2_name: str):
        pass
    
    # https://blockchair.com에서 검색? 
    # withdraw만 따로 확인 못하는듯.. => 주소 가져 올 수 있는지로 전송 가능 확인 !!주소가 이상하거나(:), 네트워크가 다른거는 판단 못함
    def check_transfer_currency(self, currency_name: str, exchange1_name: str, exchange2_name: str) -> bool:
        if exchange1_name == exchange2_name:
            return True
        if self.exchanges_map[exchange1_name].get_deposit_address_by_currency_name(currency_name) and self.exchanges_map[exchange2_name].get_deposit_address_by_currency_name(currency_name):
            return True
        return False
