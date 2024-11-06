from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, \
    Contact, ConfirmEmailToken

from django.contrib import admin
from django.http import HttpResponseRedirect
from .tasks import do_import

import logging

logger = logging.getLogger('django')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('type', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'type')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('date_joined',)


# @admin.register(Shop)
# class ShopAdmin(admin.ModelAdmin):
#     """
#     Панель управления магазинами
#     """
#     fieldsets = (
#         (None, {'fields': ('name', 'user', 'url', 'state',)}),
#     )
#     list_display = ('name', 'state', 'display_categories')
#     list_filter = ('state', 'categories')
#     search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Панель управления категориями
    """
    fieldsets = (
        (None, {'fields': ('name', 'shops')}),
    )
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Панель управления продуктами
    """
    fieldsets = (
        (None, {'fields': ('name', 'category')}),
    )
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    """
    Панель управления информацией о продуктах
    """

    fieldsets = (
        (None, {'fields': ('model', 'product', 'external_id', 'shop', 'quantity', 'price', 'price_rrc')}),
    )
    list_display = ('model', 'shop', 'quantity', 'price', 'price_rrc')
    list_filter = ('shop', 'product')
    search_fields = ('model', 'external_id')


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    """
    Панель управления параметрами
    """
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    """
    Панель управления параметрами
    """
    fieldsets = (
        (None, {'fields': ('product_info', 'parameter', 'value')}),
    )
    list_display = ('product_info', 'parameter', 'value')
    list_filter = ('product_info', 'parameter')
    search_fields = ('value',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Панель управления заказами
    """
    fieldsets = (
        (None, {'fields': ('user', 'state', 'contact')}),
    )
    list_display = ('user', 'dt', 'state')
    list_filter = ('state', 'user')
    search_fields = ('user',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Панель управления позициями заказа
    """
    fieldsets = (
        (None, {'fields': ('order', 'product_info', 'quantity')}),
    )
    list_display = ('order', 'product_info', 'quantity')
    list_filter = ('order', 'product_info')
    search_fields = ('order',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Панель управления контактами
    """
    fieldsets = (
        (None, {'fields': ('user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')}),
    )
    list_display = ('user', 'city', 'street', 'house')
    list_filter = ('user',)
    search_fields = ('user',)


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)


class ImportDataAdmin(admin.ModelAdmin):
    logger.debug("ImportDataAdmin")
    # list_display = ('__str__',)
    fieldsets = (
        (None, {'fields': ('name', 'user', 'url', 'state',)}),
    )
    list_display = ('name', 'state', 'display_categories')
    list_filter = ('state', 'categories')
    search_fields = ('name',)

    def import_data(self, request, queryset):
        url = request.POST.get('url')  # получаем url из формы
        do_import.delay(url)
        self.message_user(request, "Import task started")
        logger.debug("ImportDataAdmin: import_data")
        return HttpResponseRedirect(request.get_full_path())

    import_data.short_description = "Import data from URL"

    actions = ['import_data']


admin.site.register(Shop, ImportDataAdmin)
