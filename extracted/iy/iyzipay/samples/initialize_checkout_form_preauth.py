import json
import iyzipay

options = {
    'api_key': iyzipay.api_key,
    'secret_key': iyzipay.secret_key,
    'base_url': iyzipay.base_url
}

buyer = {
    'id': 'BY789',
    'name': 'John',
    'surname': 'Doe',
    'gsmNumber': '+905350000000',
    'email': 'email@email.com',
    'identityNumber': '74300864791',
    'lastLoginDate': '2015-10-05 12:43:35',
    'registrationDate': '2013-04-21 15:12:09',
    'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
    'ip': '85.34.78.112',
    'city': 'Istanbul',
    'country': 'Turkey',
    'zipCode': '34732'
}

address = {
    'contactName': 'Jane Doe',
    'city': 'Istanbul',
    'country': 'Turkey',
    'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
    'zipCode': '34732'
}

basket_items = [
    {
        'id': 'BI101',
        'name': 'Binocular',
        'category1': 'Collectibles',
        'category2': 'Accessories',
        'itemType': 'PHYSICAL',
        'price': '0.3'
    },
    {
        'id': 'BI102',
        'name': 'Game code',
        'category1': 'Game',
        'category2': 'Online Game Items',
        'itemType': 'VIRTUAL',
        'price': '0.5'
    },
    {
        'id': 'BI103',
        'name': 'Usb',
        'category1': 'Electronics',
        'category2': 'Usb / Cable',
        'itemType': 'PHYSICAL',
        'price': '0.2'
    }
]

request = {
    'locale': 'tr',
    'conversationId': '123456789',
    'price': '1',
    'paidPrice': '1.2',
    'currency': 'TRY',
    'basketId': 'B67832',
    'paymentGroup': 'PRODUCT',
    "callbackUrl": "https://www.merchant.com/callback",
    'buyer': buyer,
    'shippingAddress': address,
    'billingAddress': address,
    'basketItems': basket_items
}

checkout_form_preauth_initialize = iyzipay.CheckoutFormInitializePreAuth()
checkout_form_preauth_initialize_result = checkout_form_preauth_initialize.create(request, options)
checkout_form_preauth_initialize_response = json.load(checkout_form_preauth_initialize_result)
print('response:', checkout_form_preauth_initialize_response)

if checkout_form_preauth_initialize_response['status'] == 'success':
    secret_key = options['secret_key']
    conversationId = checkout_form_preauth_initialize_response['conversationId']
    token = checkout_form_preauth_initialize_response['token']
    signature = checkout_form_preauth_initialize_response['signature']
    checkout_form_preauth_initialize.verify_signature([conversationId, token], secret_key, signature)
