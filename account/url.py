from rest_framework.routers import DefaultRouter
from account.views.account_viewset import AccountViewSet

router = DefaultRouter()

router.register("", AccountViewSet)

urlpatterns = router.urls
