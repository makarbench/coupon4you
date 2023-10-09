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

from promo.action.promocode import get_affiliatelink_by_site
sys.path.append("../promo/action/promocode.py")

from promo.action.promocode import get_advertisers_list
sys.path.append("../promo/action/promocode.py")

@csrf_exempt #отключаем csrf защиту для
# данных получаемых с расширения, т.к. сейчас передачи конфиденциальных данных не будет.
# если добавлю авторизацию, то будем использовать  Django REST Framework или JWT
@app.route('/extension-data/', methods=['POST'])
def extension_data_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        payload_url = body.get('url')
        promo_site = get_promo_by_site(payload_url, request)
        result, advertiser_image = promo_site.get_promo_from_sqllite()
        affiliatelink_site = get_affiliatelink_by_site(payload_url, request)
        hotdeal_result = affiliatelink_site.get_affiliatelink_from_sqllite()
        advertiser_image = advertiser_image[0]
        print("Доступные промокоды", result)
        print("Логотип рекламодателя: ", advertiser_image)
        print("Горячая сделка ", hotdeal_result)
        return JsonResponse({'message': result,
                             'image_url': advertiser_image,
                             'message_aflink': hotdeal_result})
        #return JsonResponse({'message': 'Invalid request method'})
    else:
        return JsonResponse({'message': 'Invalid request method',
                             'image_url': 'Invalid request method',
                             'message_aflink': 'Invalid request method'
                             })


from django.http import JsonResponse

@csrf_exempt
def advertisers_list_view(request):
    if request.method == 'GET':
        print("Hello advertisers-list")

        # Создайте экземпляр класса с передачей объекта request
        advertiser_list_instance = get_advertisers_list(request)

        # Вызовите метод get_advertisers_list_from_sql для этого экземпляра
        advertiser_list = advertiser_list_instance.get_advertisers_list_from_sql()
        print ("Список всех рекламодателей: ", advertiser_list)

        # Возвращаем список в формате JSON
        return JsonResponse({"advertisers_list": advertiser_list})



if __name__ == '__main__':
    app.run(port=8000)



