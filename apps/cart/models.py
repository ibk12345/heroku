from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product
# from apps.order.models import Order

User=get_user_model()

class ShoppingCart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    date_created = models.DateTimeField(auto_now_add=True)

    def get_total_all_price(self):
        cart_items = self.cart_item.all()
        total = sum([item.get_total_price_item() for item in cart_items])
        return total

    def __str__(self):
        return f'cart_id:{self.id} owner:{self.user}'


class CartItem(models.Model):

    product: Product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True, related_name='product_in_cart')
    cart_shopping = models.ForeignKey(to=ShoppingCart, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.PositiveIntegerField(default=1)
    ordered=models.BooleanField(default=False)
    order=models.PositiveIntegerField(default=0)



    def get_total_price_item(self):
        if self.ordered==False:
            return self.product.price * self.quantity
        return 0


    def __str__(self) -> str:
        return f'{self.id} {self.cart_shopping.user.email}'
