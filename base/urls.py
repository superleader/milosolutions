from django.conf.urls import patterns, url
from views import AccountUpdateView, AccountListView, AccountCreateView, \
    AccountDeleteView, AccountDetailView, CSVResponseMixin


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)$', AccountDetailView.as_view(),
                                                name='account-detail'),                   
    url(r'^(?P<pk>\d+)/edit$', AccountUpdateView.as_view(),
                                                name='account-edit'),
    url(r'^(?P<pk>\d+)/delete$', AccountDeleteView.as_view(),
                                                name='account-delete'),
    url(r'^$', AccountListView.as_view(), name='account-list'),
    url(r'^add$', AccountCreateView.as_view(), name='account-add'),
    url(r'^download-csv$', CSVResponseMixin.as_view(), name='download-csv'),
)
