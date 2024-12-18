from django.urls import path 
# from django.conf.urls import handler404  
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('Product/',views.shoppage,name='shoppage'),
    path('Product/<int:pk>/',views.ProductView.as_view(),name='product'),
    path('About/',views.About.as_view(),name='about'),
    path('SignUp/',views.SignUpView.as_view(),name='signup'),
    path('LogIn/',views.login_user,name='login'),
    path('LogOut/',views.logout_user,name='logout'),
    path('Submit_Ticket/',views.submit_ticket,name='ticket'),
    path('Search/',views.search,name='search'),
    path('Profile/',views.info,name='info'),
    path('Updateuser/',views.update_user,name='update_user'),
    path('OmdehShop/',views.all_in_one,name='all_in_one'),
    path('FormGet/',views.fill_all_in_one,name='fill_all_in_one'),
    path('Updatepassword/',views.update_password,name='update_password'), 
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done',views.CustomPasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('Hamkari/',views.Hamkari,name='hamkari'),
    path('visitor-count/', views.visitor_count_view, name='visitor_count'),
    # path('Search/',views.search,name='search'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_done'),
    # path('change/password/', views.ChangePasswordView.as_view(), name='change_password'),
    # path('password_reset/done/',views.PasswordReset.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),

]

# # Add this line to set the custom 404 handler
# handler404 = views.custom_404_view
