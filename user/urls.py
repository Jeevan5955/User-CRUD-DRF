from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('user/', views.UserDetail.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)