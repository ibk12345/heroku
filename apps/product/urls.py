from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ProductViewSet, FavouriteView,ReviewViewSet, PostImageView

router=SimpleRouter()
router.register('products', ProductViewSet, basename='products/')
router.register('reviews', ReviewViewSet, basename='reviews/')

urlpatterns = [
    path('', include(router.urls)),
    path('favourites/', FavouriteView.as_view()),
    path('add_image/', PostImageView.as_view()),
    
]
