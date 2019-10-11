from django.contrib import admin
from main.views import Runcolors


@admin.register(Runcolors)
class RunColorsAdmin(admin.ModelAdmin):
    fields = ()
    list_display = ('product_name', 'product_number', 'url')
    search_fields = ('product_number',)
