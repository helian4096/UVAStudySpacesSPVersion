"""
 REFERENCES
 Title: did_django_google_maps_api
 Author: Bobby Stearman
 Date: 04/16/2021
 Code version: N/A
 URL: https://www.youtube.com/watch?v=wCn8WND-JpU
 Software License: GPL-3.0 license
"""
"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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

import study_spaces
from mysite import views as mysite_views
from study_spaces import views

urlpatterns = [
    path('', mysite_views.home),
    path('admin/', admin.site.urls),
    path('study/', include("study_spaces.urls")),
    path('study/accounts/', include("allauth.urls")),
]
