from django.contrib import admin
from .models import category_data,sub_category_data,product_data,customer_data,cart_data,order_data,payment_data,review_data,order_item_data

# Register your models here.
admin.site.register(category_data)
admin.site.register(sub_category_data)
admin.site.register(product_data)
admin.site.register(customer_data)
admin.site.register(cart_data)
admin.site.register(order_data)
admin.site.register(payment_data)
admin.site.register(review_data)
admin.site.register(order_item_data)

