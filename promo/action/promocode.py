from django.shortcuts import render, get_object_or_404
from django.db import connection
import tldextract
from django.db.models import Q
from promo.models import Advertiser

class get_promo_by_site:

    def __init__(self, url, request):
        self.url = url
        self.request = request

    def get_promo_from_sqllite(self):
        url = self.url
        extracted_domain = tldextract.extract(url)
        main_domain = extracted_domain.domain + "." + extracted_domain.suffix
        sqlreq = f"""
        SELECT promocode_url, promocode_entity, promocode_decription FROM promo_promocode 
        WHERE status IS 'on' and promocode_url like '%{main_domain}%'"""
        url_sqlreq = f"""
        SELECT promo_advertiser.id FROM promo_promocode
        inner join promo_advertiser on promo_promocode.advertiser_id = promo_advertiser.id
        WHERE status IS 'on' and promocode_url like '%{main_domain}%'"""
        with connection.cursor() as cursor:
            cursor.execute(sqlreq)
            results = cursor.fetchall()
            cursor.execute(url_sqlreq)
            image_data = cursor.fetchone()
            if image_data:
                instance = get_object_or_404(Advertiser, id=image_data[0])
                image_url = self.request.build_absolute_uri(instance.advertiser_image.url)
            else:
                image_url = None
        #print("Result: ",results," URL: ",image_url)
        return results, image_url


