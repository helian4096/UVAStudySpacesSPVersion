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
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
