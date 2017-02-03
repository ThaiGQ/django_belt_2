from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index, name = "main"),
    url(r"^register$", views.register, name = "registration"),
    url(r"^login$", views.login, name = "login"),
    # url(r"^user/(?P<user_id>\d+)$", views.success, name = "user_profile"),
    url(r"^logout$", views.logout, name = "logout"),
]
