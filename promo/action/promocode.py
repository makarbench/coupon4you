from django.shortcuts import render
from django.db import connection
import tldextract



class get_promo_by_site:

    def __init__(self,url):
        self.url = url


    def get_promo_from_sqllite(self):
        # Выполнение SQL-запроса
        url = self.url
        extracted_domain = tldextract.extract(url)
        main_domain = extracted_domain.domain + "." + extracted_domain.suffix
        print(main_domain)  # Output: mail.ru
        sqlreq ='''
        SELECT promocode_url, promocode_entity, promocode_decription FROM promo_promocode 
        WHERE status IS "on" and promocode_url like "%'''+main_domain+'''%"'''
        with connection.cursor() as cursor:
            cursor.execute(sqlreq)
            results = cursor.fetchall()
            print("Запрос SQL выдал ", results)

        # Пример обработки результатов запроса

        return results