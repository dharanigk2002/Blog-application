from django.contrib import admin
from .models import Post, Category, AboutUs

class PostModel(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')

admin.site.register(Post, PostModel)
admin.site.register(Category)
admin.site.register(AboutUs)
