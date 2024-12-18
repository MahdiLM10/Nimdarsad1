from django.contrib import admin
from .models import Customer,Order,Category,Product,Profile,Ticket,AllInOne
from django.contrib.auth.models import User
# Register your models here.

class UserShow(admin.ModelAdmin):
    model = Order
    list_display = ['customer','status','product']

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order,UserShow)
admin.site.register(Profile)
admin.site.register(Ticket)
admin.site.register(AllInOne)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username','first_name','last_name',]
    list_filter = ['username','first_name','last_name']
    inlines = [ProfileInline]


# admin.site.unregister(User)
# admin.site.register(User,UserAdmin)