from django.urls import path 
from core.views.index import * 


urlpatterns = [
    path('', IndexView.as_view(), name='index_view'),
]
