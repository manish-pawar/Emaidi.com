from django.contrib import admin

# Register your models here.

from .models import Customer, Worker, Skill, Wishlist, Order

admin.site.register(Customer)
admin.site.register(Worker)
admin.site.register(Skill)
admin.site.register(Wishlist)
admin.site.register(Order)