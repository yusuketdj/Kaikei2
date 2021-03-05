from django.contrib import admin
from .models import Customer, Shouhin, Accounting

# Register your models here.
admin.site.register(Customer)
admin.site.register(Shouhin)
admin.site.register(Accounting)