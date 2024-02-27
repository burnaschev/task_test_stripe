from django.contrib import admin

from products.models import Order, Item, Discount, Tax


class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        items = instance.items.all()
        total_amount = sum(item.price for item in items)
        if instance.discount:
            total_amount -= instance.discount.amount
        if instance.tax:
            total_amount *= (1 + instance.tax.rate / 100)
        instance.total_amount = total_amount
        instance.save()


admin.site.register(Order, OrderAdmin)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')


@admin.register(Tax)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')
