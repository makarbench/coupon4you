from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import string
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
def old_extension_data_view(request):
    if request.method == 'POST':
        data = request.POST.get('urls')  # Получите данные из запроса
        print("Результат", data)
        # Обработайте полученные данные здесь
        # ...

        response_data = {'message': 'Data received successfully'}
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'})

import json
def a_extension_data_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        payload_url = body.get('url')
        print("Список ", payload_url)
        for element in payload_url:
            element = str(element)
            print("Элемент списка ", element)
            characters = string.ascii_letters + string.digits
            random_code = ''.join(random.choice(characters) for _ in range(6))
            promocode = element + " " + random_code
            print("Полученный URL и его промокод ", promocode)
            return JsonResponse({'Your promocode is': promocode})
        else:
            return JsonResponse({'error': 'Invalid request method'})

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешение CORS для всех маршрутов



import sys
from promo.action.promocode import get_promo_by_site
sys.path.append("../promo/action/promocode.py")

@csrf_exempt #отключаем csrf защиту для
# данных получаемых с расширения, т.к. сейчас передачи конфиденциальных данных не будет.
# если добавлю авторизацию, то будем использовать  Django REST Framework или JWT
@app.route('/extension-data/', methods=['POST'])
def extension_data_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        payload_url = body.get('url')
        result = get_promo_by_site(payload_url).get_promo_from_sqllite()
        #print("Итоговые url", result)
       #print("Список ", payload_url)
       #characters = string.ascii_letters + string.digits
        #random_code_1 = ''.join(random.choice(characters) for _ in range(6))
       # random_code_2 = ''.join(random.choice(characters) for _ in range(6))
       # random_code_3 = ''.join(random.choice(characters) for _ in range(6))
        #promocode = payload_url + " " + random_code
        #promocode = {'Скидка 50% на все': random_code_1, 'Кэшбэк': random_code_2, 'Возьми 2 3 с подарок': random_code_3}
        #print("Полученный URL и его промокод ", promocode)
        return JsonResponse({'message': result})
        #return JsonResponse({'message': 'Invalid request method'})
    else:
        return JsonResponse({'message': 'Invalid request method'})


if __name__ == '__main__':
    app.run(port=8000)



