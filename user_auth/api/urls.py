from django.urls import path
from user_auth.api.views import register_view 
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns=[
    path('register/',register_view,name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



#----------------------TokenAuthentication---------------------------#
    #from rest_framework.authtoken.views import ObtainAuthToken
    # path('login/',ObtainAuthToken.as_view(),name='login'),
    # path('logout/',logout_view,name='logout'),
