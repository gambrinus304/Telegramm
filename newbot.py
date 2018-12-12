import requests, collections
from settings import token
from time import sleep

url = "https://api.telegram.org/bot575720932:" + token 
cripto_url = "https://www.bitstamp.net/api/v2/ticker/"
limit = 5
timeout = 100
offset = 0
start_message = 'hello, world!'
def_message = 'Hi! You can get use this commands: /start, /btc, /eth. Good luck!'
pair = 'btcusd'


def get_bot_updates(limit, timeout, offset):
    link = (url + 'getUpdates')
    # можно было сделать через формат - https://api.telegram.org/bot{}/getUpdates".format(token)
    params = {'limit': limit, 'timeout': timeout, 'offset': offset}
    # Задаем параметры:
    result = requests.get(link, params=params)
    # получаем через get-запрос данные с учетом параметров
    decoded = result.json()
    # переводим данные в json-формат
    return decoded['result']


def send_message(chat_id, text):
    link = (url + 'sendMessage')
    params = {'chat_id': chat_id, 'text': text}
    send = requests.post(link, params=params)
    return send


def cripto_priсe(pair):
    link = (cripto_url + pair)
    params = {'pair': pair}
    result_price = requests.get(link, params=params)
    decoded_price = result_price.json()
    return decoded_price


while True:
    result = get_bot_updates(limit, timeout, offset)
    decoded_price = cripto_priсe(pair)

    for update_id in result:
        offset = result[0]['update_id'] + 1
        # проверка работоспособности offset
        # print(offset)

        # обрабатываем исключения при получении сообщений, которые были отредактированы
        try:
            message_id = result[0]['message']['message_id']
            text = result[0]['message']['text']
            chat_id = result[0]['message']['chat']['id']
        except:
            message_id = result[0]['edited_message']['message_id']
            text = result[0]['edited_message']['text']
            chat_id = result[0]['edited_message']['chat']['id']
        print(text)
        message_id = message_id + 1
        # Проверка chat_id
        # print(chat_id)

        if text == '/start':
            send_message(chat_id, start_message)

        elif text == '/btc':
            pair = 'btcusd'
            result_price = cripto_priсe(pair)
            try:
                btc = result_price['last']
            except:
                btc = result_price['open']
            print(btc)
            send_message(chat_id, "BTC prise is: $ " + btc)
        elif text == '/eth':
            pair = 'ethusd'
            result_price = cripto_priсe(pair)
            try:
                eth = result_price['last']
            except:
                eth = result_price['open']
            print(eth)
            send_message(chat_id, "Eth prise is: $ " + eth)
        else:
            send_message(chat_id, def_message)
