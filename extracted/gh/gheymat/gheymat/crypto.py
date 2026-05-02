import requests as rq 
from bs4 import BeautifulSoup as bs 
from .currency import USD

def TON(toman=True, beauty=False):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        "symbol": "TON",
        "convert": "USD"
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "5f37df0b-f7ae-4377-835a-a63ee76f338d"
    }

    response = rq.get(url, headers=headers, params=parameters)
    data = response.json()

    price = data["data"]["TON"]["quote"]["USD"]["price"]
    
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'TON price not found.'
    
    
def BTC(toman=True, beauty=False):
    """
    if toman is False, then BTC Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-bitcoin'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'BTC price not found.'
    
def DOGE(toman=True, beauty=False):
    """
    if toman is False, then DOGE Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-dogecoin'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'DOGE price not found.'
    
def ETH(toman=True, beauty=False):
    """
    if toman is False, then Ethereum Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-ethereum'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'Ethereum price not found.'
    
def SOL(toman=True, beauty=False):
    """
    if toman is False, then Solana Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-solana'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'Solana price not found.'
    
def TRON(toman=True, beauty=False):
    """
    if toman is False, then TRON Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-tron'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'TRON price not found.'
    
def RIPP(toman=True, beauty=False):
    """
    if toman is False, then Ripple Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-ripple'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'Ripple price not found.'
    
def DASH(toman=True, beauty=False):
    """
    if toman is False, then Dash Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-dash'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'Dash price not found.'

def LITE(toman=True, beauty=False):
    """
    if toman is False, then LiteCoin Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-litecoin'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'LiteCoin price not found.'

def STELL(toman=True, beauty=False):
    """
    if toman is False, then Stellar Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-stellar'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'Stellar price not found.'