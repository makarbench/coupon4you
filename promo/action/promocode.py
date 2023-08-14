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
        sqlreq = f"""
            SELECT promocode_cpa_url, promocode_entity, promocode_decription FROM promo_promocode 
            WHERE status IS 'on'   
            AND promocode_url like '%{main_domain}%'
            AND CURRENT_DATE BETWEEN promocode_valid_from AND promocode_valid_to"""
        url_sqlreq = f"""
            SELECT promo_advertiser.id FROM promo_promocode
            inner join promo_advertiser on promo_promocode.advertiser_id = promo_advertiser.id
            WHERE status IS 'on' 
            AND promocode_url like '%{main_domain}%'
            AND CURRENT_DATE BETWEEN promocode_valid_from AND promocode_valid_to"""
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
        print("Result: ",results," URL: ",image_url)
        return results, image_url


class get_affiliatelink_by_site:

    def __init__(self, url, request):
        self.url = url
        self.request = request

    def get_affiliatelink_from_sqllite(self):
        url = self.url
        extracted_domain = tldextract.extract(url)
        main_domain = extracted_domain.domain + "." + extracted_domain.suffix
        sqlreq = f"""
        SELECT id, affiliatelink_cpa_url, affiliatelink_decription, 
        affiliatelink_image FROM promo_hotdealsaffiliatelink 
        WHERE status IS "on" and affiliatelink_advertiser_url like '%{main_domain}%'
        AND CURRENT_DATE BETWEEN affiliatelink_valid_from AND affiliatelink_valid_to"""

        with connection.cursor() as cursor:
            cursor.execute(sqlreq)
            results_affiliate_links = cursor.fetchall()

        result_image_map = {}
        for result in results_affiliate_links:
            instance = get_object_or_404(HotDealsAffiliateLink, id=result[0])
            if instance and instance.affiliatelink_image:
                image_url_affiliate_link = self.request.build_absolute_uri(instance.affiliatelink_image.url)
            else:
                image_url_affiliate_link = None

            # Convert the tuple to a string before using it as a key
            result_string = str(result)
            result_image_map[result_string] = image_url_affiliate_link

        return result_image_map

