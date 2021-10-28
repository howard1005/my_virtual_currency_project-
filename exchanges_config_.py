
class ExchangeConfig:
    def __init__(self) -> None:
        self.exchanges_config = {
            'binance': {'rateLimit': 300,
                        'apiKey': 'J6HcDz2L7OSjavrAbCfQWoYdNS007FoUQaTieGZnGfHdldTL4O3fk5mluuqUSAVZ',
                        'secret': 'vcHpRGWRCta4oyI5iR7OMpHWp5dScFfXpyJlO2fy9QEJSmdBrlAKl8r0iXaC2ZIg',
                        'timeout': 30000,
                        'enableRateLimit': True,
                        },
            'upbit': {'rateLimit': 700,
                      'apiKey': 'Wg21NYjm3TZ4DlCEXsx6fGtLZt7enevfeVgNpbGA',
                      'secret': 'LG1mwCB9N1JLEtDPocfaFzbwBMFdcJqy930yr3Du',
                      'timeout': 30000,
                      'enableRateLimit': True,
                      },
            'coinone': {'rateLimit': 700,
                      'apiKey': 'c61d4747-097a-461a-84a3-921faa46fdde',
                      'secret': '7012e474-402a-477d-a4cd-a3f3a6f5f0c2',
                      'timeout': 30000,
                      'enableRateLimit': True,
                      },
            'bithumb': {'rateLimit': 700,
                      'apiKey': 'f66ce81b1623f6e036f23dde09bc9157',
                      'secret': '77311848e417c6b6048ee32b75becb24',
                      'timeout': 30000,
                      'enableRateLimit': True,
                      },
            # 'poloniex': {'rateLimit': 500,
            #              'apiKey': '20NTRKZG-S0BV5ICR-VYA1S0GJ-YR2DEK4D',
            #              'secret': '6fd110a18dcf7b663f257d96bb5e10a090c56fa683f72a53bc70a2ed56d4dcda1f94394240902612e8fff386207e08dc85557fe423b4da46b24f04ebea75b7f8',
            #              'timeout': 30000,
            #              'enableRateLimit': True,
            #              },
            # 'gateio': {'rateLimit': 500,
            #            'apiKey': '5E396E3E-EAD7-4CE5-8598-C7C4347D2EA1',
            #            'secret': '71d19d28c2934cc3db434d46fc857e695a8870b5b87ec35c8aa901043f7e5fcf',
            #            'timeout': 30000,
            #            'enableRateLimit': True,
            #            },
        }

    def get_config(self):
        return self.exchanges_config
