from django.conf.urls import url
from book import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_id>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^book/(?P<book_id>[\w\-]+)/$', views.show_book, name='show_book'),
    url(r'^register/$', views.register, name='register'), # 新增的模式
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^add_comment/$', views.add_comment, name='add_comment'),
    url(r'^favorite/$', views.favorite, name='favorite'),
    url(r'^global_search', views.global_search, name='global_search'),
    url(r'^category_search', views.category_search, name='category_search'),
    url(r'^comment/$', views.comment, name='comment'),
]