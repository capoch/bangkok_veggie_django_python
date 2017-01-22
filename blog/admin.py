from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','timestamp','updated']
    list_display_links = ['id','title']
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)

# Register your models here.
