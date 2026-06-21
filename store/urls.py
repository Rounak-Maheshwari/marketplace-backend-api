from django.urls import path
from .views import ProductsListandSearchView, ProductDetailView, CategoryListView, CartView, CartItemAddView, CartItemRemoveUpdateView, ClearCartView, AddressListView, AddressCreateView, AddressUpdateDeleteView, WishlistListView, WishlistCreateView, WishlistDeleteView, CreateOrderVeiw, OrderListView

urlpatterns = [
    path('store/products/', ProductsListandSearchView.as_view()),
    path('store/products/<int:id>', ProductDetailView.as_view()),
    path('store/categories/', CategoryListView.as_view()),
    path('store/cart/', CartView.as_view()),
    path('store/cart/add/', CartItemAddView.as_view()),
    path('store/cart/update-remove-item/<int:pk>', CartItemRemoveUpdateView.as_view()),
    path('store/clear-cart/', ClearCartView.as_view()),
    path('store/user/addresses/', AddressListView.as_view()),
    path('store/user/addresses/add/', AddressCreateView.as_view()),
    path('store/user/addresses/update-delete/<int:pk>', AddressUpdateDeleteView.as_view()),
    path('store/user/wishlist/', WishlistListView.as_view()),
    path('store/user/wishlist/create/', WishlistCreateView.as_view()),
    path('store/user/wishlist/delete/<int:pk>', WishlistDeleteView.as_view()),
    path('store/user/order/create/', CreateOrderVeiw.as_view()),
    path('store/user/orders/', OrderListView.as_view()),
]