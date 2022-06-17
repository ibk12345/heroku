from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
import django_filters.rest_framework as filters
from rest_framework.response import Response 
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .permissions import IsAuthorOrAdminPermission
from .serializers import *
from .models import Favourite, Product, Likes, Product_Image
from apps.product.paginations import ProductPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductDetailSerializer
    pagination_class = ProductPagination
    filter_backends=(DjangoFilterBackend,OrderingFilter, SearchFilter)
    filterset_fields = ["is_published", "name"]
    search_fields = ['name']
    ordering_fields=['name', 'price']

    def get_serializer_class(self):
        if self.action=='list':
            return ProductListSerializer      
        else:
            return super().get_serializer_class()
        
    def retrieve(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.watch += 1
        product.save()
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['toggle_like','favourite']:
            return [IsAuthenticated()]
        return []

    #products/id/toggle_like/
    @action(detail=True, methods=['GET'])
    def toggle_like(self, request,pk):
        product=self.get_object()
        user=request.user
        like_obj, created=Likes.objects.get_or_create(product=product, user=user)
        like_obj.is_liked=not like_obj.is_liked
        like_obj.save()
        if like_obj.is_liked==True:
            return Response('You liked this product')
        return Response('You disliked this product')

    @action(detail=True, methods=['GET'])
    def favourite(self, request,pk):
        product=self.get_object()
        user=request.user
        fav_obj, created=Favourite.objects.get_or_create(product=product, user=user)
        fav_obj.favourite=not fav_obj.favourite
        fav_obj.save()
        if fav_obj.favourite==True:
            return Response('Added to favs')
        return Response('Not in favs')


class ReviewViewSet(viewsets.ModelViewSet):

    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
        
    def get_permissions(self):
        if self.action=='retrieve':
            return []
        if self.action=='create':
            return [IsAuthenticated()]
        #update, partial_update, destroy
        return[IsAuthorOrAdminPermission()]
        
    def get_serializer_context(self):
        return{'request':self.request}

class FavouriteView(ListAPIView):
    queryset=Product.objects.all()
    serializer_class=FavouriteSerializer
    permission_class=[IsAuthenticated,]

    def get_queryset(self):
        queryset=super().get_queryset()
        if getattr(self, "swagger_fake_view", False):
            return Product.objects.none()
        queryset=queryset.filter(favourites__user=self.request.user, favourites__favourite=True)
        return queryset


class PostImageView(ListCreateAPIView):
    queryset = Product_Image.objects.all()
    serializer_class = PostImageSerializer
    permission_class=[IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        data=request.FILES
        if data.get('image', 0):
            return self.create(request, *args, **kwargs)
        else:
            return Response("You haven't add any images")
    

