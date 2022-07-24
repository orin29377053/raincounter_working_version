from re import A
from django.urls import path
from . import views

urlpatterns = [
    path('', views.apioverview, name='api-overview'),
    path('data_upload_iot/', views.data_upload_iot, name='data_upload_iot'),
    path('data_upload/', views.data_upload, name='data_upload'),
    path('data_get_test/', views.data_get_test, name='data_get_test'),
    path('get_raincounter_eq/', views.get_raincounter_eq,
         name='get_raincounter_eq'),
    path('get_rain_data/', views.get_rain_data, name='get_rain_data'),
    path('line_bot/', views.line_bot_get, name='line_bot'),
    path('.well-known/pki-validation/E766DCF1B288D001709AAD99F579406C.txt',
         views.sslFileReturn),
    path('update_raindata/', views.update_raindata, name='update_raindata'),
    path('revise_eq_info/', views.revise_eq_info, name='revise_eq_info'),
    path('get_rain_data_download/', views.get_rain_data_download, name='get_rain_data_download'),

]
