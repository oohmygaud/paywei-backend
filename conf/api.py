from apps.users.views import UserViewSet, APIKeyViewSet, WhitelistAddressViewSet
from apps.invoices.views import InvoiceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'api_keys', APIKeyViewSet, basename='api_key')
router.register(r'invoices', InvoiceViewSet, basename='invoices')
router.register(r'whitelist_addresses', WhitelistAddressViewSet, basename='whitelist_addresses')

urlpatterns = router.urls