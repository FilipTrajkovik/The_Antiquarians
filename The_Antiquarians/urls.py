"""
URL configuration for The_Antiquarians project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from The_Antiquarians_app.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_manual/', user_manual, name="user_manual"),
    path('', home, name="home"),
    path('home/', home, name="home"),
    path('login_page/', login_page, name="login_page"),
    path('logout_user/', logout_user, name="logout_user"),
    path('register_page/', register_page, name="register_page"),
    path('products/', products, name="products"),
    path('product_details/<int:id>', product_details, name="product_details"),
    path('add_product/', add_product, name="add_product"),
    path('product/edit/<int:id>', add_product, name="product_edit"),
    path('product/delete/<int:id>', delete_product, name="product_delete"),
    path('shopping_cart/', shopping_cart, name="shopping_cart"),
    path('add_to_shopping_cart/', add_to_shopping_cart, name='add_to_shopping_cart'),
    path('shopping_cart/delete/<int:id>', delete_shopping_cart_item, name='delete_shopping_cart_item'),
    path('shopping_cart/delete_order/<int:id>', delete_order, name='delete_order'),
    path('create_order/<int:id>', create_order, name="create_order"),
    path('order_done/', order_done, name="order_done")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
