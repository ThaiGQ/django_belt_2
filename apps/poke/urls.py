from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index, name = "main"),
    url(r"^poke/(?P<pokee_id>\d+)$", views.poke, name = "poke"),
    # url(r"^login$", views.login, name = "login"),
    # url(r"^user/(?P<user_id>\d+)$", views.success, name = "user_profile"),
    # url(r"^logout$", views.logout, name = "logout"),
]
