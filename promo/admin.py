from django.contrib import admin

# Register your models here.
from .models import Advertiser, PromoCompany, Promocode
from django.contrib.auth.models import User
from django.forms import ModelMultipleChoiceField
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple



# admin.site.register(Advertiser)
#admin.site.register(PromoCompany)
#admin.site.register(Promocode)

# Define the admin class
class PromoCompanyInline(admin.TabularInline):
    model = PromoCompany

class PromocodeInline(admin.TabularInline):
    model = Promocode

class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ('id', 'Advertiser_Name','Advertiser_Contact_Manager_Name', 'Advertiser_Contact_Email','Advertiser_Contact_Phone',
                    'Advertiser_Country',)

    fields = ['Advertiser_Name', 'Advertiser_Contact_Manager_Name', ('Advertiser_Contact_Email','Advertiser_Contact_Phone'),
             'Advertiser_Country']
    inlines = [PromoCompanyInline]
    pass


# Register the admin class with the associated model
admin.site.register(Advertiser, AdvertiserAdmin)





@admin.register(PromoCompany)
class PromoCompanyAdmin(admin.ModelAdmin):
    list_filter = ('status', 'PromoCompany_valid_from', "PromoCompany_valid_to")
    list_display = ('id', 'PromoCompanyName', 'Advertiser', 'get_status_display',
                    'PromoCompany_valid_from', 'PromoCompany_valid_to', 'summary')
    inlines = [PromocodeInline]

    fieldsets = (
        (None, {
            'fields': ('id', 'PromoCompanyName', 'summary', 'Advertiser')
        }),
        ('Availability', {
            'fields': ('status', 'PromoCompany_valid_from', 'PromoCompany_valid_to')
        }),
    )

    pass



@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    #form = PromocodeForm
    list_display = ('id', 'promocode_decription', 'promocode_url', 'promocode_entity', 'get_status_display',
                    'Promocode_valid_from', 'Promocode_valid_to')
    pass
    # fields = ['id', 'server_name',  ('ip_address', 'port','server_username'),'Project', 'description', 'due_back', 'status']
