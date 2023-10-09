import xml.etree.ElementTree as ET
import requests
from promo.models import Promocode, Advertiser
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

class XmlParser:

    def __init__(self, xml_url):
        self.xml_url = xml_url

    def parse(self):

        xml_url = self.xml_url
        print("Начинаем парсинг ", xml_url)
        try:
            response = requests.get(xml_url)
            print("Ответ ", response)
            response.raise_for_status()
            print("Статус ", response.raise_for_status())
        except requests.RequestException as req_err:
            print(f"Ошибка при выполнении запроса: {req_err}")
            return
        except requests.HTTPError as http_err:
            print(f"HTTP ошибка: {http_err}")
            return
        except Exception as err:
            print(f"Неизвестная ошибка: {err}")
            return

        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as parse_err:
            print(f"Ошибка при парсинге XML: {parse_err}")
            return

        advcampaign_sites = {}

        for advcampaign in root.findall('.//advcampaigns/advcampaign'):
            advcampaign_id = advcampaign.get('id')

            # Заполните advcampaign_sites значениями, извлекая site для каждой advcampaign.
            advcampaign_site_elem = advcampaign.find('site')
            advcampaign_site = advcampaign_site_elem.text if advcampaign_site_elem is not None else ""
            advcampaign_sites[advcampaign_id] = advcampaign_site

            #advcampaign_name = advcampaign.find('name').text
            advcampaign_name_elem = advcampaign.find('name')
            advcampaign_name = advcampaign_name_elem.text if advcampaign_name_elem is not None else "Default Value"
            advertiser_object, created = Advertiser.objects.get_or_create(advertiser_name=advcampaign_name)
            if created:
                print(f"Advertiser {advcampaign_name} created.")

            categories = [category.text for category in advcampaign.findall('.//categories/category_id')]
            types = [type_.text for type_ in root.findall('.//types/type')]
            print('Advcampaign Name:', advcampaign_name)
            print('Categories:', categories)
            print('Types:', types)

            for coupon in root.findall('.//coupons/coupon'):



                coupon_id = coupon.get('id')

                name_elem = coupon.find('name')
                name = name_elem.text if name_elem is not None else "Default Value"

                description_elem = coupon.find('description')
                description = description_elem.text if description_elem is not None else " "

                promocode_elem = coupon.find('promocode')
                promocode = promocode_elem.text if promocode_elem is not None else "Default Value"

                promolink_elem = coupon.find('promolink')
                promolink = promolink_elem.text if promolink_elem is not None else "Default Value"

                gotolink_elem = coupon.find('gotolink')
                gotolink = gotolink_elem.text if gotolink_elem is not None else "Default Value"

                date_start_elem = coupon.find('date_start')
                date_start = date_start_elem.text if date_start_elem is not None and date_start_elem.text and date_start_elem.text != "None" else "2021-01-01 00:00:00"  # None в случае отсутствующей даты

                date_end_elem = coupon.find('date_end')
                date_end = date_end_elem.text if date_end_elem is not None and date_end_elem.text and date_end_elem.text != "None" else "2031-01-01 00:00:00" # None в случае отсутствующей даты

                # В цикле coupon, используйте advcampaign_id промокода, чтобы получить соответствующий site из advcampaign_sites
                advcampaign_id_of_coupon = coupon.find('advcampaign_id').text
                promocode_url = advcampaign_sites.get(advcampaign_id_of_coupon, "")

                print('Coupon ID:', coupon_id)
                print('Name:', name)
                print('Description:', description)
                print('Promocode:', promocode)
                print('Promolink:', promocode_url)
                print('CpaPromolink:', promolink)
                print('CpaGotolink:', gotolink)
                print('Date Start:', date_start)
                print('Date End:', date_end)
                print('---')

                date_time_obj_1 = datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S')
                date_time_obj_2 = datetime.strptime(date_end, '%Y-%m-%d %H:%M:%S')

                description = "Описание: " + name + "\n  " + description

                promocode = "Промокод: "+ promocode

                defaults = {
                    "promocode_entity": promocode,
                    "promocode_url": promocode_url,
                    "promocode_cpa_url": gotolink,
                    "promocode_decription": description,
                    "promocode_valid_from": date_time_obj_1.date(),
                    "promocode_valid_to": date_time_obj_2.date(),
                    "advertiser": advertiser_object
                }

                try:
                    promocode_object, created = Promocode.objects.update_or_create(
                        promocode_external_uid=coupon_id,
                        defaults=defaults
                    )

                    if created:
                        print(f"Promocode {promocode_object.promocode_entity} created.")
                    else:
                        print(f"Promocode {promocode_object.promocode_entity} updated.")
                except Exception as e:
                    print(f"Failed to create or update Promocode: {e}")
