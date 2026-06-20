from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, CartItem, Cart, Address, Wishlist

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ["id", "cart", "product", "quantity", "total_amount"]
        

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(read_only=True, many=True)
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Address
        fields = "__all__"

    def create(self, validated_data):
        current_user = self.context.get("user")
        if not current_user or not current_user.is_authenticated:
            raise serializers.ValidationError("Authentication credentials were not provided.")
        validated_data['user'] = current_user
        return super().create(validated_data)
        
    
class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(read_only=True, many=True)
    user = serializers.ReadOnlyField(source='user.id')
    address = serializers.ReadOnlyField(source='address.id')
    total_price = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = "__all__"



