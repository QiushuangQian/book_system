from django.contrib import admin
from book.models import Category, Book, Comment
from book.models import UserProfile

class CommentAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'score', 'content')

# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)