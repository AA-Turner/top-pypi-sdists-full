import requests as rq 
from bs4 import BeautifulSoup as bs 


def GOLD18(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/geram18'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                return f'{int(gh) // 10:,}'
            else:
                return f'{int(gh):,}'
        else:
            return int(gh)

    else:
        return 'GOLD price not found.'
    
def GOLD24(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/geram24'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                return f'{int(gh) // 10:,}'
            else:
                return f'{int(gh):,}'
        else:
            return int(gh)

    else:
        return 'GOLD price not found.'

def USED_GOLD(toman=True,beauty=False):
    url = 'https://www.tgju.org/profile/gold_mini_size'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                return f'{int(gh) // 10:,}'
            else:
                return f'{int(gh):,}'
        else:
            return int(gh)

    else:
        return 'GOLD price not found.'

def SEKE_BAHAR(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/sekeb'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                return f'{int(gh) // 10:,}'
            else:
                return f'{int(gh):,}'
        else:
            return int(gh)

    else:
        return 'Seke price not found.'
    
def SEKE_EMAM(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/sekee'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                return f'{int(gh) // 10:,}'
            else:
                return f'{int(gh):,}'
        else:
            return int(gh)

    else:
        return 'Seke price not found.'
    
def SILVER(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/silver_999'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                return f'{int(gh) // 10:,}'
            else:
                return f'{int(gh):,}'
        else:
            return int(gh)

    else:
        return 'Seke price not found.'