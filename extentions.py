import json
import requests
from config import keys

class ConvertionException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(base: str, sym: str, amount: str):

        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f"Валюта {base} не найдена!")

        try:
            sym_key = keys[sym.lower()]
        except KeyError:
            raise ConvertionException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/1bd9ba7e637d8e10d0d6b2fd/pair/{base_key}/{sym_key}/{amount}')
        resp = json.loads(r.content)
        new_price = resp['conversion_result'] * amount
        new_price = round(new_price, 3)
        message = f'Цена {amount} {base} в {sym} : {new_price}'
        return message