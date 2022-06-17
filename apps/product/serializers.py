from email.mime import image
from rest_framework import serializers

from .models import Product, Review, Product_Image

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=('id', 'name', 'category', 'price', 'watch', 'is_published')
    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['author']=instance.author.email
        # representation['category']=instance.category.title
        representation['reviews']=instance.reviews.all().count()
        return representation

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        exclude=("author",)

    def validate(self,attrs):
        request=self.context.get('request')
        attrs['author']=request.user
        return attrs
    
    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['author']=instance.author.email
        # representation['category']=instance.category.title
        representation['images'] = PostImageSerializer(instance.images.all(),
                                                       many=True).data
        representation['reviews']=ReviewSerializer(instance.reviews.all(), many=True).data
        representation['likes']=instance.likes.filter(is_liked=True).count()
        representation['favs']=instance.favourites.filter(favourite=True).count()
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        exclude=("author",)
    
    def validate(self,attrs):
        request=self.context.get('request')
        attrs['author']=request.user
        return attrs
    
    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['author']=instance.author.email
        representation['product']=instance.product.name
        return representation

class FavouriteSerializer(serializers.ModelSerializer):
    class  Meta:
        model=Product
        fields='__all__'
    

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_Image
        fields = ("image","product")

    def _get_image_url(self, obj):
        if obj.image:
            print(1)
            url = obj.image.url
            request = self.context.get('request')
            if request:
                print(2)
                url+= ', '+request.build_absolute_uri(url)
        else:
            print(3)
            url=''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation





