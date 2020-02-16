from django.contrib import admin

# Register your models here.
from .models import Product,Contact,Orders,OderUpdate

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OderUpdate)
