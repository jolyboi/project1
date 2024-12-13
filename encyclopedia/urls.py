from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:name>', views.page, name="page"),
    path('search', views.search, name='search'),
    path('random', views.random_entry, name='random'),
    path('new', views.new, name='new'),
    path('create', views.create_page, name='create')
]
