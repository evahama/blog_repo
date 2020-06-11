from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    
    list_display= ('title','slug','author','publish','created','updated','status')
    search_fields = ['title','body']
    list_filter=('created','publish','author')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields=('author',)
    ordering=['status','publish']

admin.site.register(Post,PostAdmin)
