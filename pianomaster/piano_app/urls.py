"""Url definition."""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from piano_app.views import *
from django.contrib.auth.decorators import login_required

app_name = 'piano_app'

# urlpatterns = [
#     path('', login_required(TemplateView.as_view(template_name='login.html'))),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#path('identified', LogoutView.as_view(template_name='identified.html')),

urlpatterns = [
    path('', views.home, name='home'),
    # path('contact', views.contact, name='contact'),
    # path('thanksContact', views.thankscontact, name='thanksContact'),
    path('suggestion', views.suggestion, name='suggestion'),
    path('suggestions', views.suggestions, name='suggestions'),
    path('continueOrNot', views.continueornot, name='continueOrNot'),
    path('continueOrNot/<int:rating>/', views.continueornot,
         name='continueOrNot'),
    path('toBeContinued', views.tobecontinued, name='toBeContinued'),
    # path('404', views.custom_404, name='404'),
    # path('500', views.custom_500, name='500'),
]

