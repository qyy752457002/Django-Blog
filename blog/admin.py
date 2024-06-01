from django.contrib import admin

# Register your models here.
from .models import Post, Author, Tag, Comment

class PostAdmin(admin.ModelAdmin):
    # 定义在 admin 界面中显示的字段
    list_display = ('title', "date", 'author')
    # 定义可用于过滤数据的字段
    list_filter = ("author", "tags", "date")
    # 定义自动填充 slug 字段，使用 title 字段的值
    prepopulated_fields = {"slug": ("title",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")

admin.site.register(Post, PostAdmin)  # 注册 Post 模型并应用 PostAdmin 设置
admin.site.register(Author)  # 注册 Author 模型
admin.site.register(Tag)  # 注册 Tag 模型
admin.site.register(Comment, CommentAdmin) # 注册 Comment 模型并应用 CommentAdmin 设置
