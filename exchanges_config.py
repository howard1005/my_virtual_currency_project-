
class ExchangeConfig:
    def __init__(self) -> None:
        self.exchanges_config = {
            'binance': {'rateLimit': 300,
                        'apiKey': '',
                        'secret': '',
                        'timeout': 30000,
                        'enableRateLimit': True,
                        },
            'upbit': {'rateLimit': 700,
                      'apiKey': '',
                      'secret': '',
                      'timeout': 30000,
                      'enableRateLimit': True,
                      },
            'coinone': {'rateLimit': 700,
                      'apiKey': '',
                      'secret': '',
                      'timeout': 30000,
                      'enableRateLimit': True,
                      },
            'bithumb': {'rateLimit': 700,
                      'apiKey': '',
                      'secret': '',
                      'timeout': 30000,
                      'enableRateLimit': True,
                      },
            'poloniex': {'rateLimit': 500,
                         'apiKey': '',
                         'secret': '',
                         'timeout': 30000,
                         'enableRateLimit': True,
                         },
            'gateio': {'rateLimit': 500,
                       'apiKey': '',
                       'secret': '',
                       'timeout': 30000,
                       'enableRateLimit': True,
                       },
        }

    def get_config(self):
        return self.exchanges_config
