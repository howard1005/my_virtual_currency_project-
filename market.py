from collections import defaultdict
import ccxt
import sys
import math
import time


class Market:
    def __init__(self, ccxt_exchange, ccxt_market: dict, order_book_time_limit: int = 6000) -> None:
        self.ccxt_exchange = ccxt_exchange
        self.ccxt_market = ccxt_market
        (self.min, self.max) = (
            ccxt_market['limits']['amount']['min'], ccxt_market['limits']['amount']['max'])
        self.precision = ccxt_market['precision']['amount']
        self.order_book = None
        self.order_book_update_time = 0
        self.order_book_time_limit = order_book_time_limit

    def __str__(self):
        return '({}, {})'.format(self.ccxt_exchange, self.ccxt_market['symbol'])

    def refresh(self):
        self.refresh_order_book()

    def refresh_order_book(self):  # sqlite 사용해서 시간 조정 해서 쿼리 날릴지 필요할듯(굳이?)
        if time.time() - self.order_book_update_time < self.order_book_time_limit:
            return
        print('[{}][{}] {} {}  (time {}sec, limit {}sec)'.format(self.__class__.__name__, sys._getframe().f_code.co_name,
              self.ccxt_exchange, self.ccxt_market['symbol'], self.order_book_update_time, self.order_book_time_limit))
        try:
            self.order_book = self.ccxt_exchange.fetch_order_book(
                self.ccxt_market['symbol'])
        except Exception as e:
            print("Error {}".format(e))
        self.order_book_update_time = time.time()

    def get_exchange_name(self) -> str:
        return '{}'.format(self.ccxt_exchange)

    def get_symbol(self) -> str:
        return self.ccxt_market['symbol']

    def get_quote(self) -> str:
        return self.ccxt_market['quote']

    def get_base(self) -> str:
        return self.ccxt_market['base']

    def get_order_book(self) -> dict:
        return self.order_book

    def get_current_price(self):
        try:
            return self.ccxt_exchange.fetch_ticker(self.ccxt_market['symbol'])['close']
        except Exception as e:
            print("Error {}".format(e))
            return -1

    def get_ohlcvs(self, timeframe='1m'): #Open-high-low-close-volume
        try:
            return self.ccxt_exchange.fetch_ohlcv(self.ccxt_market['symbol'], timeframe=timeframe)
        except Exception as e:
            print("Error [{}] get_ohlcvs : {}".format(self.get_exchange_name(), e))
            return []

    # calculate buy
    # fee 추가 필요
    def calculate_quantity_base_by_quote(self, quote_quantity: float) -> float:
        ret = 0
        remain = quote_quantity
        for p, q in self.get_order_book()['asks']:
            remain -= p*q
            if remain >= 0:
                ret += q
            else:
                n = 10**self.precision
                ret += math.floor((p*q+remain)/p*(n))/n
                break
        if ret < self.min:
            return 0
        return ret

    # calculate sell
    # fee 추가 필요
    def calculate_quantity_quote_by_base(self, base_quantity: float) -> float:
        ret = 0
        remain = base_quantity
        for p, q in self.get_order_book()['bids']:
            remain -= q
            if remain >= 0:
                ret += p*q
            else:
                ret += (q+remain)*p
                break
        if ret < self.min:
            return 0
        return ret
