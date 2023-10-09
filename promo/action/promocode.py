from django.shortcuts import render, get_object_or_404
from django.db import connection
import tldextract
from django.db.models import Q
from promo.models import Advertiser, HotDealsAffiliateLink


class get_promo_by_site:

    def __init__(self, url, request):
        self.url = url
        self.request = request

    def get_promo_from_sqllite(self):
        url = self.url
        extracted_domain = tldextract.extract(url)
        main_domain = extracted_domain.domain + "." + extracted_domain.suffix

        sqlreq = """
            SELECT promocode_cpa_url, promocode_entity, promocode_decription
            FROM promo_promocode 
            WHERE status = 'on'   
            AND promocode_url LIKE %s
            AND CURRENT_DATE BETWEEN promocode_valid_from AND promocode_valid_to
        """

        url_sqlreq = """
                    SELECT promo_advertiser.id
                    FROM promo_promocode
                    INNER JOIN promo_advertiser ON promo_promocode.advertiser_id = promo_advertiser.id
                    WHERE status = 'on' 
                    AND promocode_url LIKE %s
                    AND CURRENT_DATE BETWEEN promocode_valid_from AND promocode_valid_to
                """

        advertiser_image = """
                            SELECT promo_advertiser.advertiser_image_url
                            FROM promo_promocode
                            INNER JOIN promo_advertiser ON promo_promocode.advertiser_id = promo_advertiser.id
                            WHERE promocode_url LIKE %s

                        """

        with connection.cursor() as cursor:
            cursor.execute(sqlreq, [f'%{main_domain}%'])
            results = cursor.fetchall()
            cursor.execute(url_sqlreq, [f'%{main_domain}%'])
            image_data = cursor.fetchone()
            cursor.execute(advertiser_image , [f'%{main_domain}%'])
            advertiser_image = cursor.fetchall()
            print("Наша ссылка", advertiser_image)

            if image_data:
                instance = get_object_or_404(Advertiser, id=image_data[0])
                image_url = instance.advertiser_image.url if instance.advertiser_image else None
            else:
                image_url = None

        print("Result: ", results, " URL: ", advertiser_image)
        return results, advertiser_image


class get_affiliatelink_by_site:

    def __init__(self, url, request):
        self.url = url
        self.request = request

    def get_affiliatelink_from_sqllite(self):
        url = self.url
        extracted_domain = tldextract.extract(url)
        main_domain = extracted_domain.domain + "." + extracted_domain.suffix

        sqlreq = """
            SELECT id, affiliatelink_cpa_url, affiliatelink_decription, affiliatelink_image
            FROM promo_hotdealsaffiliatelink 
            WHERE status = 'on' AND affiliatelink_advertiser_url LIKE %s
            AND CURRENT_DATE BETWEEN affiliatelink_valid_from AND affiliatelink_valid_to
        """

        with connection.cursor() as cursor:
            cursor.execute(sqlreq, [f'%{main_domain}%'])
            hotdeal_result = cursor.fetchall()

            #cursor.execute(url_sqlreq, [f'%{main_domain}%'])
            #image_data = cursor.fetchone()

            #if image_data:
              #  instance = get_object_or_404(Advertiser, id=image_data[0])
              #  image_url = instance.advertiser_image.url if instance.advertiser_image else None
          #  else:
              #  image_url = None

        print("Result: ", hotdeal_result)
        return hotdeal_result

class get_advertisers_list:
    def __init__(self, request):
        self.request = request
    def get_advertisers_list_from_sql(self):
        request = self.request
        print("start advertiser_list")
        sqlreq = """
        SELECT advertiser_name, advertiser_image_url, advertiser_cpa_url FROM public.promo_advertiser
        """
        with connection.cursor() as cursor:
            cursor.execute(sqlreq)
            advertiser_list= cursor.fetchall()
            print("Список рекламодаелей", advertiser_list)
        return advertiser_list



