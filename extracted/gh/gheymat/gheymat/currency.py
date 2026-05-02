import requests as rq 
from bs4 import BeautifulSoup as bs 


def USD(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/price_dollar_rl'
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
        return 'Dollar price not found.'

def GBP(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/price_gbp'
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
        return 'Pound price not found.'  

def EUR(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/price_eur'
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
        return 'EURO price not found.' 

def TRY(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/price_try'
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
        return 'Turkish lira price not found.' 
    
def AED(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/price_aed'
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
        return 'United Arab Emirates Dirham price not found.' 
  
def CNY(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/price_cny'
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
        return 'Yuan price not found.'  
    
def INR(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/price_inr'
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
        return 'Rupee price not found.'  
    
def SEK(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/price_sek'
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
        return 'Swedish Krona price not found.'  
    
def OMR(toman=True, beauty=False):
    url = 'https://www.tgju.org/profile/price_omr'
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
        return 'Oman Rial price not found.'  