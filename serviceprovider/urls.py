from django.conf.urls import url
from serviceprovider import views


urlpatterns = [
    url(r'^serviceprovider/$', views.ProviderList.as_view(), name='ProviderList'),
    url(r'^serviceprovider/(?P<pk>.+)/$', views.ProviderDetail.as_view(), name='ProviderDetail'),
]