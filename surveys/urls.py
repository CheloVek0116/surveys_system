from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from surveys.views import AdminViewSet, ClientViewSet

router = routers.SimpleRouter()
router.register('admin_surveys', AdminViewSet, basename='admin-survey')
router.register('client_surveys', ClientViewSet, basename='client-survey')
urlpatterns = router.urls

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
