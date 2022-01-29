from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    pass

admin.site.register(Category)
admin.site.register(Page, PageAdmin)



