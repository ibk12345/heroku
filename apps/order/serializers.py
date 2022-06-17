from rest_framework import serializers

from .models import Order
from apps.cart.models import ShoppingCart
from apps.cart.serializers import CartItemSerializer



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields='__all__'

    def validate(self, attrs):
        user = self.context.get("request").user
        cart_item=ShoppingCart.objects.filter(user=user)[0].cart_item.filter(ordered=False)

        if not cart_item:
                msg = "User doesn't have any item in his cart"
                raise serializers.ValidationError(msg, code='no cart item')
        return attrs
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = CartItemSerializer(instance.shopping_cart.cart_item.filter(ordered=True, order=instance.id), many=True).data
        # representation['total_price'] = instance.shopping_cart.cart_item.filter(order=instance.id).get_total_all_price()
        representation['owner']=instance.shopping_cart.user.email
        return representation