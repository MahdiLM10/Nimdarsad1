from django.urls import path 
from . import views


urlpatterns = [
    path('add/',views.cart_add,name='cart_add'),
    path('delete/',views.cart_delete,name='cart_delete'),
    path('',views.cart_summary,name='cart_summary'),
    path('ShopVerify/',views.shopverify,name='shopverify'),
    path('Form/',views.fill_form,name='fillform'),
    path('create_order/',views.create_order_view, name='create_order'),
    # path('shopallinone/',views.send_all_in_one,name='send_all_in_one'),
    # path('ShopInOne/',views.fill_all_in_one,name='fill_all_in_one'),
    # path('update/',views.cart_update,name='cart_update'),
    # path('color/',views.color_add,name='color_add'),

]
