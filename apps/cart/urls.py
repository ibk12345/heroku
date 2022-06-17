from django.urls import path

from apps.cart.views import ShoppingCartView, AddProductInCartView

urlpatterns = [
    path('', ShoppingCartView.as_view()),
    path('<int:pk>/', ShoppingCartView.as_view()),
    path('add_cart_item/', AddProductInCartView.as_view()),

]