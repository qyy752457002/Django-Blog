from django.urls import path

from . import views

urlpatterns = [
    # 配置首页 URL，使用 StartingPageView 视图类
    path("", views.StartingPageView.as_view(), name="starting-page"), 
    
    # 配置所有文章列表页的 URL，使用 AllPostsView 视图类
    path("posts", views.AllPostsView.as_view(), name="posts-page"),  
    
    # 配置单个文章详情页的 URL，使用 SinglePostView 视图类，slug 用于传递文章的唯一标识符
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="post-detail-page"),  # /posts/my-first-post
    
    # 配置稍后阅读列表页的 URL，使用 ReadLaterView 视图类
    path("read-later", views.ReadLaterView.as_view(), name="read-later")  
]

''' 
在 Django 的 URL 配置中，name 参数的作用是为每个 URL 模式分配一个唯一的名称。
这些名称用于在 Django 项目中引用 URL，从而使代码更加可读和易于维护。

name 参数的作用是为 URL 模式提供一个别名，以便在代码中更方便地引用和管理 URL。
'''