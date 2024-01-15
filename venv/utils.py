import requests
import json
from config import keys

"""Собственный класс исключений"""
class Apiexception(Exception):
    pass

"""Класс конвертации валют"""
class Converter:
    """Статичный метод для конвертации валют с обработкой исключений"""
    @staticmethod
    def convert(quote: str, base: str, amount):
        if quote == base:
            raise Apiexception(f"Не удалось перевести одинаковые валюты {base}.")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise Apiexception(f"Не удалось обработать валюту {quote}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise Apiexception(f"Не удалось обработать валюту {base}.")
        try:
            amount = float(amount)
        except ValueError:
            raise Apiexception(f"Не удалось обработать колличество {amount}.")
        quote_ticker, base_ticker = keys[quote], keys[base]
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]
        total_base_amount = total_base * int(amount)

        return  total_base_amount
