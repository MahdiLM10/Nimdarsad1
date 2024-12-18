from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
# from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from .models import Product,Category,Profile,Ticket
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView
from .forms import SignUpForm,TicketForm,UpdateUserInfo,UpdateViews,LostPassword,AllInOnePageForm #ChangePasswordForm
from django.db.models import Q
from django.views.generic import TemplateView
import json
from Cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
# from django.contrib.auth.views import (PasswordChangeView,PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetView)
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
from time import sleep
from django.urls import reverse_lazy
from django.http import HttpResponse
import os
from django.core.mail import send_mail
# from pyment.forms import ShippingFrom
# from pyment.models import ShopAddressGet
# from django.views import View


def shoppage(request):
    products = Product.objects.all()
    return render(request,'shoppage.html',{'products':products})

def homepage(request):
    visitor_count_view(request)
    return render(request,'index.html',{})

# def product(request):
#     return render(request,'product.html',{})


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


class About(TemplateView):

    template_name = 'about.html'


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('homepage')


    def get_success_url(self):
        messages.success(request=self.request,message='خوش آمدید به سایت نیم درصد')
        return super().get_success_url()
    


# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             currect_user = Profile.objects.get(user__id=request.user.id)
#             saved_cart = currect_user.old_cart


#             if saved_cart:
#                 converted_cart = json.loads(saved_cart)

#                 cart = Cart(request,)


#                 for key,value in converted_cart.items():
#                     cart.db_add(product=key,quantity=value)



#             messages.success(request, ("با موفقیت وارد شدید "))
#             return redirect('homepage')
#         else:
#             messages.success(request, ("نام کاربری یا رمز عبور اشتباه است"))
#             return redirect('login')
#     else:
#         return render(request, "registration/login.html")

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user=request.user)  # Fixed typo in variable name
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)

                for product_id, product_details in converted_cart.items():
                    quantity = product_details['quantity']
                    color = product_details['color']  # Assuming color is stored in the saved cart
                    cart.db_add(product=product_id, quantity=quantity, color=color)

            messages.success(request, "با موفقیت وارد شدید")  # Success message in Persian
            return redirect('homepage')
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است")  # Error message in Persian
            return redirect('login')
    else:
        return render(request, "registration/login.html")

def logout_user(request):
    logout(request)
    messages.success(request, ("با موفقیت خارج شدید"))
    return redirect('homepage')

@login_required(login_url='login')  # Ensure that only logged-in users can create tickets
def submit_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)  # Create the ticket instance but don't save yet
            ticket.user = request.user  # Set the user to the currently logged-in user
            ticket.save()  # Now save the ticket
            messages.success(request,'پیغام شما برای پشتیبانی ارسال شد')
            # tkt = Ticket.objects.get(user_id=request.user.id)
            # get_ticket1 = tkt.description
            # get_ticket2 = tkt.title
            # subject = 'پیام ارسالی'
            # message = f'رئیس پیغامی برای شما آمده است‌{get_ticket1,get_ticket2}'
            # from_email = settings.EMAIL_HOST_USER
            # recipient_list = ['admin@gmail.com']  # Replace with the recipient's email
            # send_mail(subject, message, from_email, recipient_list)
            return redirect('homepage')  # Redirect to a list of tickets or a success page
    else:
        form = TicketForm()
    return render(request, 'poshtibani.html', {'form': form})

  
    
def categorysummary(request):
    all_cat = Category.objects.all()
    return render(request,'category_summary.html',{'category':all_cat})



def update_user(request):
    if request.user.is_authenticated:
        currect_user = User.objects.get(id=request.user.id)
        user_form = UpdateViews(request.POST or None,instance=currect_user)
        
        if user_form.is_valid():
            user_form.save()
            login(request,currect_user)
            messages.success(request,'پروفایل شما ویرایش شد')
            return redirect('homepage')
        return render(request,'update_user.html',{'user_form':user_form})

    else:
        messages.success(request,'ابتدا وارد شوید')
        return redirect('homepage')

    
def update_password(request):
    if request.user.is_authenticated:
        currect_user = request.user

        if request.method == 'POST':
            form = LostPassword(currect_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request,'رمز شما ویرایش شد')
                login(request,currect_user)
                return redirect('update_user')

            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                return redirect('update_password')
        else :
            form = LostPassword(currect_user)
            return render(request,'passwordlost.html',{'form':form})
    else:
        messages.success(request,'ابتدا وارد شوید')
        return redirect('homepage')
        


def info(request):
    if request.user.is_authenticated:
        currect_user = Profile.objects.get(user__id=request.user.id)
        # shop_user = ShopAddressGet.objects.get(user__id=request.user.id)

        form = UpdateUserInfo(request.POST or None,instance=currect_user)
        # shop_form = ShippingFrom(request.POST or None,instance=shop_user)


        
        if form.is_valid() :#or shop_form.is_valid():
            form.save()
            # shop_form.save()
            messages.success(request,'اطلاعات کاربری شما ویرایش شد')
            return redirect('homepage')
        return render(request,'info.html',{'form':form,})#'shop_form':shop_form,})
    
    else:
        messages.success(request,'ابتدا وارد شوید')
        return redirect('homepage')
    

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched)|Q(description__icontains=searched))

        if not searched:
            messages.success(request,'چنین محصولی موجود نیست')
        else:
            return render(request,'search.html',{'searched':searched})
    return render(request,'search.html',{})





class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/custom_password_reset_form.html'
    # form_class = ChangePasswordForm
    email_template_name = 'registration/custom_password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
    
    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     return render(request, self.template_name, {'form': form})

    
    
    # def form_valid(self, form):
    #     # You can add custom logic here if needed
    #     return super().form_valid(form)
    
class CustomPasswordResetDone(PasswordResetDoneView):
    template_name= 'registration/custom_password_reset_done_view.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/custom_password_confirm.html'
    form_class = LostPassword
    # email_template_name = 'registration/custom_password_reset_email.html'
    success_url = reverse_lazy('password_reset_complete')
    
class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/custom_password_rest_complete.html'
        
        
def Hamkari(request):
    return render(request,'hamkari.html',{})



def all_in_one(request):
    if request.method == 'POST':
        form = AllInOnePageForm(request.POST)
        if form.is_valid():
            all_in_one_item = form.save(commit=False)
            all_in_one_item.user = request.user  # Set the user to the currently logged-in user
            all_in_one_item.save()
            messages.success(request,'تیکت برای ارسال سفارش عمده ثبت شد')
            return redirect('homepage')  # Redirect to a success page or another view
    else:
        form = AllInOnePageForm()
    
    return render(request, 'all_in_one.html', {'form': form})

@login_required(login_url='login')
def fill_all_in_one(request):
    if request.method == 'POST':
        # در اینجا می‌توانید اطلاعات خاصی را از دیتابیس دریافت کنید
        profile = Profile.objects.get(user=request.user)  # به عنوان مثال، اولین پروفایل را می‌گیریم
        form = AllInOnePageForm(instance=profile)# فرم را با داده‌های پروفایل پر می‌کنیم
    else:
        form = AllInOnePageForm()  # فرم خالی برای GET request

    return render(request,'all_in_one.html', {'form': form})


def visitor_count_view(request):
    # Define the path to the text file
    file_path = os.path.join('C:/Users/Programmer/Desktop', 'visitor_count.txt')
    ip_log_file_path = os.path.join('C:/Users/Programmer/Desktop', 'visitor_ips.txt')
    try:
        # Read the current count from the file
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                count = int(file.read().strip())
        else:
            count = 0

        # Increment the count
        count += 1

        # Save the updated count back to the file
        with open(file_path, 'w') as file:
            file.write(str(count))
    except:
        pass 
    
    try:    
        # Get the visitor's IP address
        ip_address = request.META.get('REMOTE_ADDR')

        # Log the visitor's IP address to the IP log file
        with open(ip_log_file_path, 'a') as ip_file:
            ip_file.write(f"{ip_address}\n")

        # Print the visitor's IP address to the console (optional)
        print(f"Visitor IP: {ip_address}")

        # Return an empty response or a simple message
    except:
        pass
    return HttpResponse(status=204)  # No Content

# def all_in_one(request):
#     if request.method == 'POST':
#         form = AllInOnePageForm(request.POST)
#         if form.is_valid():
#             # shop = form.save(commit=False)
#             # shop.user = request.user
#             # shop.save()
#             shop = form.save(commit=False)
#             shop.user = request.user
#             shop.save()

#             subject = 'سفارش جدید'
#             message = f'موضوع: {shop.title}\nتوضیحات: {shop.description}\nکاربر: {shop.user}'
#             recipient_list = ['admin@gmail.com']  # Replace with your email

#             send_mail(
#                 subject,
#                 message,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=recipient_list,
#                 fail_silently=True
#             )

#             return redirect('send_all_in_one')

        
#     else:
#         form = AllInOnePageForm()
#     return render(request, 'all_in_one.html', {'form': form})
# def search(request):
#     if request.method == "POST":
#         searched = request.POST['searched']
#         searched = Product.objects.filter(Q(name__icontains=searched)|Q(description__icontains=searched))

#         if not searched:
#             messages.success(request,'چنین محصولی موجود نیست')
#         else:
#             return render(request,'search.html',{'searched':searched})
#     return render(request,'search.html',{})



# def custom_404_view(request, exception):
#     return render(request, 'index.html', status=404)

    # def form_valid(self,form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


# def categoryview(request,cat):
#     cat = cat.replace('-',' ')
#     try:
#         category = Category.objects.get(name=cat)
#         products = Product.objects.filter(category = category)
#         return render(request,'category.html',{'products':products,'category':category})
#     except :
#         messages.success(request,'دسته بندی موجود نیست')
#         return redirect('homepage')
    

    
    