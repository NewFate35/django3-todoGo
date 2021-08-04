from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ['user', 'title', 'description', 'important', 'created', 'completedAt']
    list_filter = ['important', 'created', 'completedAt']


admin.site.register(Todo, TodoAdmin)
