from rest_framework.routers import DefaultRouter

from .views import PromptViewSet


app_name = "api"

router = DefaultRouter()
router.register("prompts", PromptViewSet, basename="prompt")

urlpatterns = router.urls
