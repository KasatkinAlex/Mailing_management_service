from django.contrib import admin

from main.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_at',)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name_product', 'price', 'category_id',)
#     list_filter = ('category_id',)
#     search_fields = ('name_product', 'description')
#
#
# @admin.register(BlogPost)
# class BlogPostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'publication_sign', 'views_count')
#     search_fields = ('title', 'content')
#
#
# @admin.register(VersionProduct)
# class VersionProductAdmin(admin.ModelAdmin):
#     list_display = ('version_number', 'version_title', 'version_activ')
#     search_fields = ('version_title', 'version_number', 'version_activ')
