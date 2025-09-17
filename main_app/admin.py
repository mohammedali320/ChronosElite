from django.contrib import admin
from .models import Category, Watch, Order, OrderItem  

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

admin.site.register(Category)
admin.site.register(Watch)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem) 
