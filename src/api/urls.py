from django.urls import path

from api.views import query

urlpatterns = [path("", query)]
