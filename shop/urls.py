from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("menyu/", views.menu, name="menu"),
    path("haqqimizda/", views.about, name="about"),
    path("elaqe/", views.contact, name="contact"),
    path("mehsul/<slug:slug>/", views.product_detail, name="product_detail"),
]
