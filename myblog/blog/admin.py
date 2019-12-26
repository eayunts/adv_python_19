from django.contrib import admin
from .models import Post, Comment, Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Slug')    
admin.site.register(Blog, BlogAdmin)

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Slug', 'Date')    
    search_fields = ['Title', 'Content']
    #prepopulated_fields = {'Slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Post, PostAdmin)
#admin.site.register(Comment, CommentAdmin)
