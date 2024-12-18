from django.shortcuts import render,redirect
from django.shortcuts import render,get_object_or_404
from .cart import Cart 
from Shop.models import Product,Order
from django.http import JsonResponse
from django.contrib import messages
# myapp/views.py
from django.contrib.auth.decorators import login_required  
from Shop.models import Profile,AllInOne
from Shop.forms import UpdateUserInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantity = cart.get_quants()
    color = cart.get_color()
    total = cart.get_total() 
    return render(request,'cart_summary.html',{'cart_products':cart_products,'quantitys':quantity,'color':color,'total':total})

@login_required(login_url='login')
def send_test_email(request):
    profile_get_mail = get_object_or_404(Profile,user_id=request.user.id)
    subject = 'سفارش شما'
    message = 'سفارش شما ثبت و در حال پردازش است'
    recipient_list = [profile_get_mail.email,]  # Replace with your email

    send_mail(
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=True 
    )


def create_order_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        get_old_cart = get_object_or_404(Profile,user_id=request.user.id)
        form = UpdateUserInfo(request.POST, instance=request.user.profile)
        cart_products = cart.get_prods()  # Assuming 'cart' is an instance of your cart class
        qty = cart.get_quants()
        colors = cart.get_color()
        
        
        if form.is_valid():
            # Save the updated user information
            profile = form.save()
            
        # Iterate over the cart products and create orders
        for product in cart_products:
            quantity = qty.get(f'{product.id}',)  # Get the quantity from the form
            color = colors.get(f'{product.id}',)  # Get the color name from the cart
                    
            if quantity:
                order = Order(
                    product=product,
                    customer=profile,
                    quantity=int(quantity),
                    color=color,
                    price=product.price,
                    is_sale=product.is_sale,
                    sale_price=product.sale_price,
                    address=profile.address1,
                    phone=profile.phone,  # You can also get phone from the profile
                    email=profile.email,
                    city=profile.city,
                    state=profile.state,
                    zipcode=profile.zipcode,
                    all_price=int(quantity)*int(product.price),
                    date=timezone.now(),  # Use current time
                    status=False  # Assuming the order is pending
                )
                order.status = True
                order.save()
                cart.delete(product=product.id)
            cart.delete(product=product.id)
        cart.clear()
        messages.success(request,'سفارش شما با موفقیت ثبت شد')
        send_test_email(request,)
        save = get_old_cart.old_cart
        try:
            get_old_cart.old_save = save + get_old_cart.old_save()
            get_old_cart.save()
        except Exception:
            pass
        # Redirect to a success page or order summary
        return redirect('homepage')  # Redirect to a success page or order summary

    return redirect('cart_view')


# if request.method == 'POST':
#         # Instantiate the form with the submitted data
#         form = UpdateUser Info(request.POST, instance=request.user.profile)

#         if form.is_valid():
#             # Save the updated user information
#             profile = form.save()

#             # Retrieve products from the cart
#             cart_products = cart.get_prods()  # Assuming 'cart' is an instance of your cart class
#             qty = cart.get_quants()  # Get quantities from the cart

#             # Create orders for each product in the cart
#             for product in cart_products:
#                 quantity = qty.get(product.id, 1)  # Default to 1 if not found
#                 order = Order(
#                     product=product,
#                     quantity=quantity,
#                     address=profile.address1,  # Use the first address from the profile
#                     phone=profile.phone,  # Use the updated phone number
#                     date=timezone.now(),
#                     status=False  # Assuming the order is pending
#                 )
#                 order.save()

# In your add_to_cart view
def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        color_name = request.POST.get('color_name')

        # Fetch the product object based on product_id
        product = get_object_or_404(Product, id=product_id)

        # Create cart instance
        cart.add(product, product_qty, color_name)

        return JsonResponse({'status': 'success', 'message': 'Product added to cart.'}) 


def cart_delete(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))  # Ensure product_id is a string

        cart.delete(product=product_id)  # Call the delete method from the Cart class

        messages.success(request, 'محصولی از سبد خرید حذف شد')  # Success message in Persian
        return JsonResponse({'product': product_id, 'message': 'محصولی از سبد خرید حذف شد'})


def profile_view(request, user_id):
    # Fetch the profile for the given user ID
    profile = get_object_or_404(Profile, user_id=user_id)
    
    # Pass the old_cart to the template
    print(profile)
    return render(request, 'profile.html', {'old_cart': profile.old_cart})    
    
def shopverify(request):
    cart = Cart(request,)
    if request.user.is_authenticated:
        get_old_cart = get_object_or_404(Profile,user_id=request.user.id)
        currect_user = Profile.objects.get(user__id=request.user.id)
        form = UpdateUserInfo(request.POST or None,instance=currect_user)

        if form.is_valid() :#or shop_form.is_valid():
            form.save()
            cart.clear()
            save = get_old_cart.old_cart
            try:
                get_old_cart.old_save += save
                get_old_cart.save()
            except Exception:
                pass
            messages.success(request,'اطلاعات شما ثبت شد')
            return redirect('homepage')
        return render(request,'shopverify.html',{'form':form,})#'shop_form':shop_form,})
    
    else:
        messages.success(request,'ابتدا وارد شوید')
        return redirect('homepage')
    
@login_required(login_url='login')
def fill_form(request):
    if request.method == 'POST':
        # در اینجا می‌توانید اطلاعات خاصی را از دیتابیس دریافت کنید
        profile = Profile.objects.get(user=request.user)  # به عنوان مثال، اولین پروفایل را می‌گیریم
        form = UpdateUserInfo(instance=profile)  # فرم را با داده‌های پروفایل پر می‌کنیم
    else:
        form = UpdateUserInfo()  # فرم خالی برای GET request

    return render(request, 'shopverify.html', {'form': form})

# def send_mail_all(request):
#     all_get = get_object_or_404(AllInOne,user_id=request.user.id)
#     subject = 'سفارش شما'
#     message = f'{all_get.title}\n{all_get.description}\n{all_get.user}'
#     recipient_list = ['admin@gmail.com',]  # Replace with your email

#     send_mail_all(
#         subject,
#         message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=recipient_list,
#         fail_silently=True 
#     )
        

# def send_all_in_one(request):
#     all_get = get_object_or_404(AllInOne,user_id=request.user.id)
#     subject = 'سفارش شما'
#     message = f'{all_get.title}\n{all_get.description}\n{all_get.user}'
#     recipient_list = ['admin@gmail.com',]  # Replace with your email

    
#     # if request.user.is_authenticated:
#     #     currect_user = Profile.objects.get(user__id=request.user.id)
#     #     form = UpdateUserInfo(request.POST or None, instance=currect_user)
#     #     if form.is_valid():
#     #         form.save()
#     #         return redirect('homepage')
#     #     return redirect('homepage')
#     # else:
#     #     form = UpdateUserInfo()
#     # return render(request, 'shopverifyall.html', {'form': form})

#     if request.user.is_authenticated:
#         currect_user = Profile.objects.get(user__id=request.user.id)
#         form = UpdateUserInfo(request.POST or None,instance=currect_user)
#         if form.is_valid() :#or shop_form.is_valid():
#             form.save()
#             try:
#                 send_mail_all(
#                 subject,
#                 message,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=recipient_list,
#                 fail_silently=True 
#             )
#             except:
#                 pass
#             return redirect('homepage')
#         return render(request,'shopverifyall.html',{'form':form})
#     else:
#         form = UpdateUserInfo()
#     return redirect('send_all_in_one')

# @login_required(login_url='login')
# def fill_all_in_one(request):
#     if request.method == 'POST':
#         # در اینجا می‌توانید اطلاعات خاصی را از دیتابیس دریافت کنید
#         profile = Profile.objects.get(user=request.user)  # به عنوان مثال، اولین پروفایل را می‌گیریم
#         form = UpdateUserInfo(instance=profile)# فرم را با داده‌های پروفایل پر می‌کنیم
#     else:
#         form = UpdateUserInfo()  # فرم خالی برای GET request

#     return render(request, 'shopverifyall.html', {'form': form})

# def cart_add(request):
#     cart = Cart(request)

#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
#         product_qty = int(request.POST.get('product_qty'))
#         product = get_object_or_404(Product, id=product_id)
#         cart.add(product=product,quantity=product_qty)

#         cart_quintity = cart.__len__()


#         # response = JsonResponse({'Product name':product.name})
#         # return response
#         response = JsonResponse({'qty':cart_quintity})
#         messages.success(request,'به سبد خرید اضافه شد')
#         return response
    



# def cart_add(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         product_qty = request.POST.get('product_qty')
#         color_name = request.POST.get('color_name')

#         # Fetch the product object based on product_id
#         product = get_object_or_404(Product, id=product_id)

#         # Remove the last item in the cart if it exists
#         if cart.cart:  # Check if there are any items in the cart
#             cart.remove_last()

#         # Create cart instance and add the new product
#         cart.add(product, product_qty, color_name)

#         return JsonResponse({'status': 'success', 'message': 'Product added to cart.'})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


# def color_add(request):
#     cart = Cart(request)
    
    
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
#         color_name = str(request.POST.get('color_name'))
#         colors = get_object_or_404(Product, id=product_id)
#         cart.add_color(product_id=colors,color=color_name)
        
#     colorResponse = JsonResponse({'color':colors})
#     return colorResponse
#     # messages.success(request,'به سبد خرید اضافه شد')
# def cart_update(request):
#     cart = Cart(request)

#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
#         product_qty = int(request.POST.get('product_qty'))

#         cart.update(product=product_id, quantity = product_qty)

#         response = JsonResponse({'qty':product_qty})
#         messages.success(request,'سبد خرید شما به روزرسانی شد')
#         return response


# def cart_update(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         quantity = request.POST.get('quantity')
#         color = request.POST.get('color')  # Get the color from the request

#         cart = Cart(request)
#         cart.update(product_id, quantity, color)

#         # Optionally, return a success message or the updated cart
#         return JsonResponse({'success': True, 'cart': cart.cart})

    # return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
# @csrf_exempt  # Use this only if you are not using CSRF tokens properly
# def cart_update(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         quantity = request.POST.get('quantity')
#         color = request.POST.get('color')

#         # Here you would call your Cart class to update the cart
#         cart = Cart(request)
#         cart.update(product_id, quantity, color)

#         messages.success(request,'سبد خرید شما به روزرسانی شد')
#         return JsonResponse({'success': True, 'message': 'سبد خرید به روزرسانی شد'})

#     # return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)




    # return JsonResponse({'error': 'Invalid request.'}, status=400)  # Handle invalid requests

# def color_update(request):
#     cart = Cart(request)

#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
#         color_name = str(request.POST.get('color_name'))

#         cart.update_color(product=product_id, color = color_name)

#         response = JsonResponse({'color':color_name})
#         return response
#         # messages.success(request,'سبد خرید شما به روزرسانی شد')

# def cart_delete(request):
#     cart = Cart(request)

#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))

#         cart.delete(product=product_id)

#         response = JsonResponse({'product':product_id})
#         messages.success(request,'محصولی از سبد خرید حذف شد')
#         return response


# def shopdone(request):
#     return render(request,'shop_done.html',{})