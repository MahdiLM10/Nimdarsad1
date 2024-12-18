from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_modified = models.DateField(User,auto_now=True)
    # phone = models.models.PhoneNumberField(max_le)
    email = models.EmailField(max_length=30,blank=True)
    phone = models.CharField(max_length=15,blank=True)
    address1 = models.CharField(max_length=250,blank=True)
    address2 = models.CharField(max_length=250,blank=True)
    city = models.CharField(max_length=25,blank=True)
    state = models.CharField(max_length=25,blank=True)
    zipcode = models.CharField(max_length=25,blank=True)
    old_cart = models.CharField(max_length=200,blank=True,null=True)
    old_save = models.CharField(max_length=300,blank=True,null=True)

    def __str__(self,):
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance,email=instance.email)
        user_profile.save()

post_save.connect(create_profile,sender=User)

class Category(models.Model):
    name = models.CharField(max_length=40)
    


    def __str__(self,):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    


    def __str__(self,):
        return f'{self.first_name} {self.last_name}'
    


class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500,default='',blank=True,null=True)
    price = models.DecimalField(default=0,decimal_places=0,max_digits=12)
    omdeh = models.DecimalField(default=0,decimal_places=0,max_digits=12,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to='upload/product/')
    star = models.IntegerField(default=0,blank=True,null=True,validators=[MaxValueValidator(5),MinValueValidator(0)])
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=0,max_digits=12)
    color = models.CharField(max_length=20,blank=False)
    


    def __str__(self,):
        return self.name
    

class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1,blank=True)
    color = models.CharField(max_length=15,blank=True,null=True,default=None)
    address = models.CharField(max_length=400,default='',blank=True)
    email = models.EmailField(max_length=30,blank=True)
    phone = models.CharField(max_length=15,blank=True)
    city = models.CharField(max_length=25,blank=True)
    state = models.CharField(max_length=25,blank=True)
    zipcode = models.CharField(max_length=25,blank=True)
    price = models.DecimalField(default=0,decimal_places=0,max_digits=12)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=0,max_digits=12)
    all_price = models.DecimalField(default=0,decimal_places=0,max_digits=12)
    date = models.DateField(default=datetime.today(),)
    status = models.BooleanField(default=False)


    def __str__(self,):
        return f"The Order Create By {self.customer} and Status is {self.status}"
    
    
    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Prepare email details
        subject = f"New Order Created: {self.address}"
        message = f"Order Details:\n\nProduct: {self.product}\nOrderPerson: {self.customer}\nQuantity: {self.quantity}\nPrice:  {self.price}\nSell_Price:  {self.sale_price}\nColor:  {self.color}\nall_Price:  {self.all_price}"
        recipient_list = ['admin@gmail.com']  # You can add admin email here

        # Send email
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


@receiver(post_save, sender=Order)
def send_order_email(sender, instance, created, **kwargs):
    if created:
        subject = f"New Ticket Created: {instance.address}"
        message = f"Order Details:\n\nProduct: {instance.product}\nOrderPerson: {instance.customer}\nQuantity: {instance.quantity}\nPrice:  {instance.price}\nSell_Price:  {instance.sale_price}\nColor:  {instance.color}\nall_Price:  {instance.all_price}"
        recipient_list = ['admin@gmail.com']  # You can add admin email here

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line

    def __str__(self):
        return f"Ticket Created at {self.created_at.date()} by {self.user}"


    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Prepare email details
        subject = f"New Ticket Created: {self.title}"
        message = f"Ticket Details:\n\nTitle: {self.title}\nDescription: {self.description}\nCreated At: {self.created_at}\nUser:  {self.user.username}"
        recipient_list = ['admin@gmail.com']  # You can add admin email here

        # Send email
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


@receiver(post_save, sender=Ticket)
def send_ticket_email(sender, instance, created, **kwargs):
    if created:
        subject = f"New Ticket Created: {instance.title}"
        message = f"Ticket Details:\n\nTitle: {instance.title}\nDescription: {instance.description}\nCreated At: {instance.created_at}\nUser:  {instance.user.username}"
        recipient_list = ['admin@gmail.com']  # You can add admin email here

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        
        
        
class AllInOne(models.Model):
    title = models.CharField(max_length=90,blank=True)
    description = models.CharField(max_length=500,blank=False)
    address1 = models.CharField(max_length=300,default='',blank=True)
    email = models.EmailField(max_length=30,blank=True)
    phone = models.CharField(max_length=15,blank=True)
    city = models.CharField(max_length=25,blank=True)
    zipcode = models.CharField(max_length=25,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.email} ساخته شده با این ایمیل"
    
    
    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Prepare email details
        subject = f"سفارشی عمده برای شما سریعا پیگیری کنید"
        message = f"خرید عمده :\n\nموضوع: \n{self.title}\nآدرس ارسال: \n{self.address1}\n ایمیل: \n{self.email}\n تلفن: \n{self.phone}\n شهر: \n{self.city}\n کدپستی: \n{self.zipcode}\n توضیحات: \n{self.description}\nتاریخ ایجاد: \n{datetime.now()}\nایجاد کننده:  \n{self.user.username}"
        recipient_list = ['admin@gmail.com',]  # You can add admin email here

        # Send email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    
@receiver(post_save, sender=AllInOne)
def send_all_in_one(sender, instance, created, **kwargs):
    if created:
        subject = f"ثبت سفارش شما‌:{instance.title}"
        message = f"خرید شما با موفقیت ثبت شد! به زودی یکی از همکاران ما با شما تماس خواهد گرفت."
        recipient_list = [instance.email,]  # You can add admin email here

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)