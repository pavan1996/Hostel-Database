from django.conf.urls import url
from .views import index , about, contact, infoentry, updateInfo, product_list, product_list_sort_by, transaction, purpose, paymentmode, profile, profile_post_data, export_users_xls, features, report, card,card_sort_by, emailList, quick_search_id, quick_search_name


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^quick_search_id/$', quick_search_id, name='quick_search_id'),
    url(r'^quick_search_name/$', quick_search_name, name='quick_search_name'),
 	url(r'^about/$', about, name='about'),   
 	url(r'^contact/$', contact, name='contact'),
 	url(r'^infoentry/$', infoentry, name='info'),
 	url(r'^updateinfo/(?P<id>[HhTtDd]{1}[a-zA-Z]{1}[0-9]{3})/$', updateInfo, name='updateInfo'),
 	url(r'^filter/$', product_list, name='filter'),
 	url(r'^filter/(?P<sortBy>[a-zA-Z].*)/$', product_list_sort_by, name='filter_sort_by'),
 	# url(r'^filter/', export_users_xls, name='export_users_xls'),	

 	url(r'^transaction/(?P<id>[HhTtDd]{1}[a-zA-Z]{1}[0-9]{3})/$', transaction, name='transaction'),
 	url(r'^purpose/$', purpose, name='purpose'),
 	url(r'^paymentmode/$', paymentmode, name='paymentmode'),
 	url(r'^profile/(?P<id>[HhTtDd]{1}[a-zA-Z]{1}[0-9]{3})/post$', profile_post_data, name='profile_post_dat'),
 	url(r'^profile/(?P<id>[HhTtDd]{1}[a-zA-Z]{1}[0-9]{3})/$', profile, name='profile'),
 	url(r'^export/xls/$', export_users_xls, name='export_users_xls'),
 	url(r'^features/$', features, name='features'),
 	url(r'^features/report/$', report, name='report'),
 	url(r'^features/card/$', card, name='card'),
 	url(r'^features/card/(?P<sortBy>[a-zA-Z].*)/$', card_sort_by, name='card_sort_by'),
 	url(r'^features/email_list/$', emailList, name='emailList'),
]