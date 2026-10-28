from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import ChallengeViewSet, index

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]