"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include

from lists import views
from django.conf.urls import url, include


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path(r"^", views.home_page)
    url(r"^$", views.home_page, name="home"),
    url(r"^lists/", include("lists.urls")),

    # url(r"^lists/(\d+)/$", views.view_list, name="view_list"),
    # url(r"^lists/(\d+)/add_item$", views.add_item, name="view_list"),
    # url(r"^lists/new$", views.new_list, name="new_list")
]
