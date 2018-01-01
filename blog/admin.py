from django.contrib import admin

from .models import Location, Post, Image

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','timestamp','updated']
    list_display_links = ['id','title']
    class Meta:
        model = Post

class ImageAdmin(admin.ModelAdmin):
    list_display = ['location', 'image']
    class Meta:
        model = Image

admin.site.register(Post, PostAdmin)
admin.site.register(Location)
admin.site.register(Image, ImageAdmin)

# Register your models here.
