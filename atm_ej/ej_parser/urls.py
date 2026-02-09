from django.urls import path
from . import views

urlpatterns = [
    # Upload page (GET)
    path('', views.upload_page, name='upload_page'),

    # File upload + parse EJ (POST)
    path('upload/', views.upload_ej, name='upload_ej'),
]
