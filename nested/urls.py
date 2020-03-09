from rest_framework.routers import SimpleRouter

from nested.views import BookViewSet

router = SimpleRouter()
router.register('table', BookViewSet)
urlpatterns = router.urls
