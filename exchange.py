from market import Market
import sys
import asyncio


class Exchange:
    def __init__(self, ccxt_exchange, markets: list[Market]) -> None:
        self.ccxt_exchange = ccxt_exchange
        self.markets = markets
        self.currency_deposit_address = {}

    def __str__(self):
        return '{}'.format(self.ccxt_exchange)

    def get_name(self):
        return '{}'.format(self.ccxt_exchange)

    def get_markets_list(self) -> list:
        return self.markets

    def get_all_currencies(self) -> list:
        return self.ccxt_exchange.currencies

    async def refresh_all_markets(self):
        loop = asyncio.get_event_loop()
        for market in self.markets:
            await loop.run_in_executor(None, market.refresh)
            #market.refresh()

    def _check_available_method_by_name(self, method_name: str) -> bool:
        if not self.ccxt_exchange.has[method_name]:
            print('[{}][{}] unavailable {}'.format(
                self.__class__.__name__, sys._getframe().f_code.co_name, method_name))
            return False
        if (self.ccxt_exchange.apiKey == '') or (self.ccxt_exchange.secret == ''):
            print('[{}][{}] no apiKey or secret'.format(
                self.__class__.__name__, sys._getframe().f_code.co_name))
            return False
        return True

    def create_deposit_address_by_currency_name(self, currency_name: str):
        if not self._check_available_method_by_name('createDepositAddress'):
            return None
        try:
            self.ccxt_exchange.createDepositAddress(currency_name)
        except Exception as e:
            print('[{}][{}] {}({}) {}'.format(self.__class__.__name__,
                  sys._getframe().f_code.co_name, currency_name, self.ccxt_exchange, e))
            self.currency_deposit_address[currency_name] = None
            return None

    # 입출금 열렸는지 확인하는 용도로는 부적합할듯?
    def get_deposit_address_by_currency_name(self, currency_name: str):
        if currency_name in self.currency_deposit_address:
            return self.currency_deposit_address[currency_name]
        if not self._check_available_method_by_name('fetchDepositAddress'):
            return None
        #if self.create_deposit_address_by_currency_name(currency_name):
        #    return self.currency_deposit_address[currency_name]
        try:
            self.currency_deposit_address[currency_name] = self.ccxt_exchange.fetchDepositAddress(currency_name)
            return self.currency_deposit_address[currency_name]
        except Exception as e:
            print('[{}][{}] {}({}) {}'.format(self.__class__.__name__,
                  sys._getframe().f_code.co_name, currency_name, self.ccxt_exchange, e))
            self.create_deposit_address_by_currency_name(currency_name)
            return None

    def withdraw(self, currency_name: str, amount: float, address: str, tag: str = None):
        if not self._check_available_method_by_name('withdraw'):
            return None
        try:
            return self.ccxt_exchange.withdraw(currency_name, amount, address, tag)
        except Exception as e:
            print('[{}][{}] {}'.format(self.__class__.__name__,
                  sys._getframe().f_code.co_name, e))
            return None

    def get_deposit_transactions_by_currency_name(self, currency_name: str):
        if not self._check_available_method_by_name('fetchDeposits'):
            return None
        try:
            return self.ccxt_exchange.fetchDeposits(currency_name)
        except Exception as e:
            print('[{}][{}] {}'.format(self.__class__.__name__,
                  sys._getframe().f_code.co_name, e))
            return None

    def get_withdrawal_transactions_by_currency_name(self, currency_name: str):
        if not self._check_available_method_by_name('fetchWithdrawals'):
            return None
        try:
            return self.ccxt_exchange.fetchWithdrawals(currency_name)
        except Exception as e:
            print('[{}][{}] {}'.format(self.__class__.__name__,
                  sys._getframe().f_code.co_name, e))
            return None
