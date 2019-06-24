from apps.users.views import UserViewSet, APIKeyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'api_keys', APIKeyViewSet, basename='api_key')

urlpatterns = router.urls