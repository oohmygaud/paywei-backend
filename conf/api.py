from apps.users.views import UserViewSet, APIKeyViewSet
from apps.invoices.views import InvoiceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'api_keys', APIKeyViewSet, basename='api_key')
router.register(r'invoices', InvoiceViewSet, basename='invoices')

urlpatterns = router.urls