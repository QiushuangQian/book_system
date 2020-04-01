from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^show_cart/$', views.show_cart, name='show_cart'),
    url(r'^count_cart/$', views.count_cart, name='count_cart'),
    url(r'^add_cart/$', views.add_cart, name='add_cart'),
    url(r'^delete_cart/$', views.delete_cart, name='delete_cart'),
    url(r'^settle_cart/$', views.settle_cart, name='settle_cart'),
    url(r'show_order/$', views.show_order, name='show_order'),
    url(r'modify_order/$', views.modify_order, name='modify_order'),
]