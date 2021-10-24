from rest_framework import routers

from Article.views import ArticleViewSet

router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet, basename='article')
urlpatterns = router.urls
