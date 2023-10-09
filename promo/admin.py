from django.contrib import admin
from django import forms

# Register your models here.
from .models import Advertiser, PromoCompany, Promocode, HotDealsAffiliateLink

# Define the admin class
class PromoCompanyInline(admin.TabularInline):
    model = PromoCompany

class PromocodeInline(admin.TabularInline):
    model = Promocode


class AffiliateLinkInline(admin.TabularInline):
    model = HotDealsAffiliateLink


class AdvertiserAdminForm(forms.ModelForm):
    class Meta:
        model = Advertiser
        fields = '__all__'

import sys
from promo.action.xml_parser import XmlParser
sys.path.append("../promo/action/xml_parser.py")
from django.contrib import messages

def parse_xml_files(modeladmin, request, queryset):
    for advertiser in queryset:
        if advertiser.xml_file_url:
            parser = XmlParser(advertiser.xml_file_url)
            try:
                print("Будем парсить ", advertiser.xml_file_url)
                parser.parse()
                messages.success(request, f"Успешный парсинг для {advertiser.advertiser_name}")
            except Exception as e:
                messages.error(request, f"Ошибка парсинга для {advertiser.advertiser_name}: {str(e)}")
        else:
            messages.error(request, f"У {advertiser.advertiser_name} нет xml_file_url")

# Регистрация действия администратора
parse_xml_files.short_description = "Распарсить XML файлы для выбранных рекламодателей"

class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertiser_name', 'advertiser_contact_manager_name',
                    'advertiser_contact_email', 'advertiser_contact_phone',
                    'advertiser_country', 'xml_file_url', 'advertiser_cpa_url')  # Добавьте xml_file_url, если хотите его отображать
    actions = [parse_xml_files]  # Добавьте действие
    inlines = [PromoCompanyInline, AffiliateLinkInline, PromocodeInline]
    form = AdvertiserAdminForm

    fieldsets = (
        (None, {
            'fields': ('advertiser_name', 'advertiser_cpa_url', 'advertiser_contact_manager_name',
                       ('advertiser_contact_email', 'advertiser_contact_phone'),
                       'advertiser_country')
        }),
        ('Images', {
            'fields': ('advertiser_image', 'advertiser_image_url', 'advertiser_image_aws', 'xml_file'),
            # Добавлено 'xml_file' для загрузки XML-файлов
        }),
    )

admin.site.register(Advertiser, AdvertiserAdmin)




@admin.register(PromoCompany)
class PromoCompanyAdmin(admin.ModelAdmin):
    list_filter = ('status', 'promo_company_valid_from', "promo_company_valid_to")
    list_display = ('id', 'promo_company_name', 'advertiser', 'get_status_display',
                    'promo_company_valid_from', 'promo_company_valid_to', 'summary')
    inlines = [PromocodeInline]

    fieldsets = (
        (None, {
            'fields': ('id', 'promo_company_name', 'summary', 'advertiser')
        }),
        ('Availability', {
            'fields': ('status', 'promo_company_valid_from', 'promo_company_valid_to')
        }),
    )

    pass



@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    #form = PromocodeForm
    list_display = ('id', 'advertiser', 'promocode_external_uid', 'promocode_decription', 'promocode_cpa_url', 'promocode_url',  'promocode_entity', 'get_status_display',
                    'promocode_valid_from', 'promocode_valid_to')
    pass
    # fields = ['id', 'server_name',  ('ip_address', 'port','server_username'),'Project', 'description', 'due_back', 'status']

@admin.register(HotDealsAffiliateLink)
class HotDealsAffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertiser', 'affiliatelink_cpa_url', 'affiliatelink_advertiser_url', 'affiliatelink_decription',
                    'get_status_display',
                    'affiliatelink_valid_from', 'affiliatelink_valid_to')
    pass