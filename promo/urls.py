from django.urls import path
from promo import views
from django.urls import include, re_path


from django.urls import path
from . import views

urlpatterns = [
    path('extension-data/', views.extension_data_view, name='extension-data'),
    path('advertisers-list/', views.advertisers_list_view, name='advertisers-list'),

    # Add more URL patterns as needed
]