from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from import_export.resources import ModelResource
from admin_panel.models import User, Category, Product, UserProduct, Order, Dispatcher, Post

class CustomImportExport(ImportExportModelAdmin, ExportActionModelAdmin):
    pass


# setup export
class UserResource(ModelResource):
    class Meta:
        model = User
        import_id_fields = ('id',)


class UserProductResource(ModelResource):
    class Meta:
        model = UserProduct
        fields = ['id', 'product__name', 'user__username', 'amount', 'order']


class OrderResource(ModelResource):
    class Meta:
        model = Order
        fields = ['id', 'user__username', 'is_paid', 'price', 'product_amount', 'address', 'created_at']


@admin.register(User)
class UserAdmin(CustomImportExport):
    resource_classes = [UserResource]
    list_display = ('id', 'user_id', 'fio', 'username', 'created_at')
    list_display_links = ('id', 'user_id')
    list_editable = ('fio', 'username')


@admin.register(Category)
class CategoryAdmin(CustomImportExport):
    list_display = [field.name for field in Category._meta.fields]
    list_editable = ('name',)


@admin.register(Product)
class ProductAdmin(CustomImportExport):
    list_display = [field.name for field in Product._meta.fields]
    list_editable = [field.name for field in Product._meta.fields if field.name != 'id']
    list_filter = ['category']


@admin.register(UserProduct)
class UserProductAdmin(CustomImportExport):
    resource_classes = [UserProductResource]
    list_display = ('id', 'product', 'user', 'amount')
    list_display_links = ('id', 'product', 'user')
    list_filter = ['user']


@admin.register(Order)
class OrderAdmin(CustomImportExport):
    resource_classes = [OrderResource]
    list_display = ('id', 'user', 'is_paid', 'created_at')


@admin.register(Dispatcher)
class DispatcherAdmin(CustomImportExport):
    list_display = [field.name for field in Dispatcher._meta.fields]


@admin.register(Post)
class PostAdmin(CustomImportExport):
    list_display = [field.name for field in Post._meta.fields]
    list_editable = [field.name for field in Post._meta.fields if field.name != 'id' and field.name != 'created_at']


# sort models from admin.py by their registering (not alphabetically)
def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    app_list = list(app_dict.values())
    return app_list


admin.AdminSite.get_app_list = get_app_list
