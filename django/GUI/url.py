"""GUI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from crawling import views

urlpatterns = [
    #API 키 확인 화면
    path('', views.index, name='index'),
    #키 확인 일치하면 넘어가는 화면
    path('check/', views.checkAPI, name='check'),
    #키 확인 없이 볼 수 있는화면
    path('index/', views.example, name='example'),
    #검색 후 넘어가는 화면
    path('search/', views.search, name='search'),
    #새로고침 화면
    path('', views.refresh, name='refresh'),
    #주문 취소 후 화면
    path('cancel/', views.cancelorder, name='cancel'),
    #구매 후 넘어가는 화면
    path('purchase/', views.purchase, name='purchase'),
]
