import os
import alpaca_trade_api as tradeapi

os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"

api = tradeapi.REST('PK2WI3PX7GS65EDBLJ8Z', 'og/TE/EFvraussTuxhRZGorKo6AIBkqsZJgzIObt')
account = api.get_account()
print(account.status)