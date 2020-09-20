from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)  # 更改admin 介面
    # 在admin介面show  model 欄位'created'


admin.site.register(Todo, TodoAdmin)
