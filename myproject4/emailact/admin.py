# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Product,Stock
class  Productadmin(admin.ModelAdmin):
    list_display=['pid','pname','pcost','pmfdt','pexpdt']
    list_filter = ['pname']
    class mete:
        model=Product
class Stockadmin(admin.ModelAdmin):
    list_display = ['prodid','tot_qty','last_update','next_update']
    list_filter = ['prodid']
    class meta:
        model=Stock

admin.site.register(Stock,Stockadmin)
admin.site.register(Product,Productadmin)