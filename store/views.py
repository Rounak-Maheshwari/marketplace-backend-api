from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Category, Cart, CartItem, Address, Wishlist, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer, AddressSerializer, WishlistSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class CategoryListView(GenericAPIView, ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductsListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductDetailView(GenericAPIView, RetrieveModelMixin):
    permission_classes = [AllowAny]
    queryset = Product
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CartItemAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1)) 

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart, cart_created = Cart.objects.get_or_create(user=request.user)

        item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not item_created:
            item.quantity += quantity

        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class CartItemRemoveUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=pk, cart=cart)
            
            cart_item.delete()
            return Response("Cart Item successfully Removed.", status=status.HTTP_200_OK)
            
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Cart item not found or unauthorized access attempt."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
    def patch(self, request, pk):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, id=pk)

            quantity = request.data.get('quantity')

            if cart_item.product.total_stock < quantity:
                    return Response(
                        {"detail": f"Cannot update. Only {cart_item.product.total_stock} items left in stock."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            cart_item.quantity = quantity
            cart_item.save()

            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response(
                {"detail": "Cart or target product record was not found or access is unauthorized."},
                status=status.HTTP_404_NOT_FOUND
            )

class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.cart_items.all().delete()

            return Response(
                {"message": "Cart cleared successfully!"}, 
                status=status.HTTP_200_OK
            )

        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )



class AddressListView(GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated]
    
    serializer_class = AddressSerializer
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class AddressCreateView(GenericAPIView, CreateModelMixin):
    permission_classes = [IsAuthenticated]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AddressUpdateDeleteView(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class WishlistListView(GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class WishlistCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            product_id = request.data.get('product_id')
            product = Product.objects.get(id=product_id)    
        except Product.DoesNotExist:
            return Response("Product Does not Exist", status=status.HTTP_404_NOT_FOUND)

        wishlist = Wishlist.objects.create(user=user, product=product)
        wishlist.save()
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WishlistDeleteView(GenericAPIView, DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class CreateOrderVeiw(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            address_id = request.data.get('address_id')
            address = Address.objects.get(user=user, id=address_id)
        except Address.DoesNotExist:
            return Response('Address Does not exist', status=status.HTTP_400_BAD_REQUEST)
        payment_mode = request.data.get('payment_mode')
        is_paid = request.data.get('is_paid', False)

        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return Response({"detail": "Cannot place order with an empty cart."}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({"detail": "Shopping cart not initialized."}, status=status.HTTP_404_NOT_FOUND) 
        
        order = Order.objects.create(
            user = user,
            address = address,
            payment_mode = payment_mode,
            is_paid = is_paid,
            status = "Placed"
        )

        for item in cart_items:
            product = item.product
            quantity = item.quantity
            print("Product", quantity)

            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        
        cart_items.delete()
        serializer = OrderSerializer(order) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class OrderListView(GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kargs):
        return self.list(request, *args, **kargs)