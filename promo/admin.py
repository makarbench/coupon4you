from django.contrib import admin

# Register your models here.
from .models import Advertiser, PromoCompany, Promocode

# Define the admin class
class PromoCompanyInline(admin.TabularInline):
    model = PromoCompany

class PromocodeInline(admin.TabularInline):
    model = Promocode

class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertiser_name','advertiser_contact_manager_name', 'advertiser_contact_email','advertiser_contact_phone',
                    'advertiser_country',)

    fields = ['advertiser_name', 'advertiser_contact_manager_name', ('advertiser_contact_email','advertiser_contact_phone'),
             'advertiser_image','advertiser_country']
    inlines = [PromoCompanyInline]
    pass


# Register the admin class with the associated model
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
    list_display = ('id', 'promocode_decription', 'promocode_url', 'promocode_entity', 'get_status_display',
                    'promocode_valid_from', 'promocode_valid_to')
    pass
    # fields = ['id', 'server_name',  ('ip_address', 'port','server_username'),'Project', 'description', 'due_back', 'status']
