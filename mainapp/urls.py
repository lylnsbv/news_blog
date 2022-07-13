from django.urls import path
from .views import BaseView, AboutView, ContactView

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact')
]
