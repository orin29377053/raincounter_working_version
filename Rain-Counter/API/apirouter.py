from django.urls import path
from rest_framework.routers import DefaultRouter
# from ma02_acoustic_smart_design_tool.api import acct_proj, apiview
from API import views


router = DefaultRouter()
router.register('data_upload_iot', views.data_upload_iot, basename='data_upload_iot')
# router.register(r'acoustic-data', apiview.AcousticDataViewset, basename='acoustic-data')
# router.register(r'acoustic-data-management', apiview.AcousticDataManagementViewset, basename='acoustic-data-management')

# router.register(r'ema-temp', apiview.EMATempViewset, basename='ema-temp')
# router.register(r'ema-mode-temp', apiview.EMAModeTempViewset, basename='ema-mode-temp')
# router.register(r'ema-file-temp', apiview.EMAFileTempViewset, basename='ema-file-temp')
# router.register(r'ema-temp-review', apiview.EMATempReviewViewset, basename='ema-temp-review')

# router.register(r'acoustic-data-temp', apiview.AcousticDataTempViewset, basename='acoustic-data-temp')
# router.register(r'acoustic-data-temp-review', apiview.AcousticDataTempReviewViewset, basename='acoustic-data-temp-review')

# router.register(r'option-vendor', apiview.VendorViewset, basename='option-vendor')
# router.register(r'option-fan-size', apiview.FanSizeViewset, basename='option-fan-size')
# router.register(r'option-hdd-vendor', apiview.HddVendorViewset, basename='option-hdd-vendor')
# router.register(r'option-hdd-family', apiview.HddFamilyNameViewset, basename='option-hdd-family')

urlpatterns = [
    # path('acct-porj/', acct_proj.acct_proj_api),
    # path('sub-proj/', acct_proj.sub_project_api),
]

urlpatterns += router.urls
