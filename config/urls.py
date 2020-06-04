from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.lending.views import ApplicationViewSet, ProgramViewSet, BorrowerViewSet

router = DefaultRouter()
router.register('applications', ApplicationViewSet)
router.register('program', ProgramViewSet)
router.register('borrower', BorrowerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls))
]
