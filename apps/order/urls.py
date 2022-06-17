from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import OrderViewSet

router=SimpleRouter()
router.register('orders', OrderViewSet, basename='orders/')

urlpatterns = [
    path('', include(router.urls)),    
]
