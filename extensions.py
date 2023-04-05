import requests
import json
from config import exchanges
class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}!")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}!")

        r = requests.get(f"https://api.apilayer.com/exchangerates_data/latest?base={base_key}&symbols={sym_key}",
                     headers={
                     "apikey": "qGGgRPoD95vYk1x8jmlLJOpvKpVWSKZ8"
                     })
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * float(amount)
        n_p = round(new_price, 2)
        return n_p
