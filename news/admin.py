from django.contrib import admin
from news.models import Category,News,Comment
# Register your models here.
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['title']
#     list_filter = ['title']
# class NewsAdmin(admin.ModelAdmin):
#     list_display = ['title','category','image_tag']
#     list_filter = ['category']
#     readonly_fields = ('image_tag',)
#     prepopulated_fields = {'slug':('title',)} 
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['subject','comment','status','create_at']
#     list_filter = ['status']
#     readonly_fields = ('subject','comment','ip','user','news','rate',)
    
admin.site.register(Category)
admin.site.register(News)
admin.site.register(Comment)