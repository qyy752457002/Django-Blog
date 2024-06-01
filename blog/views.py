from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from .models import Post
from .forms import CommentForm

# 主页视图，显示最新的3篇文章
class StartingPageView(ListView):
    template_name = "blog/index.html"  # 指定模板文件
    model = Post  # 指定模型
    ordering = ["-date"]  # 按日期倒序排序
    context_object_name = "posts"  # 模板中的上下文变量名

    # 获取查询集并返回最新的3篇文章
    def get_queryset(self):
        queryset = super().get_queryset()  # 调用父类的get_queryset方法获取所有文章
        data = queryset[:3]  # 仅获取最新的3篇文章
        return data

# 显示所有文章的视图
class AllPostsView(ListView):
    template_name = "blog/all-posts.html"  # 指定模板文件
    model = Post  # 指定模型
    ordering = ["-date"]  # 按日期倒序排序
    context_object_name = "all_posts"  # 模板中的上下文变量名

# 显示单篇文章详情的视图
class SinglePostView(View):
    # 检查文章是否存储在session中
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")  # 从session中获取存储的文章列表
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts  # 检查当前文章是否在存储的列表中
        else:
            is_saved_for_later = False

        return is_saved_for_later

    # 处理GET请求，显示文章详情
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)  # 根据slug获取对应的文章
        
        context = {
            "post": post,
            "post_tags": post.tags.all(),  # 获取文章的所有标签
            "comment_form": CommentForm(),  # 创建一个空的评论表单
            "comments": post.comments.all().order_by("-id"),  # 获取文章的所有评论，并按ID倒序排列
            "saved_for_later": self.is_stored_post(request, post.id)  # 检查文章是否已存储
        }
        return render(request, "blog/post-detail.html", context)  # 渲染文章详情模板

    # 处理POST请求，保存评论
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)  # 将POST数据绑定到评论表单
        post = Post.objects.get(slug=slug)  # 根据slug获取对应的文章

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)  # 创建但不保存评论实例
            comment.post = post  # 将评论关联到对应的文章
            comment.save()  # 保存评论实例

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))  # 重定向到文章详情页

        context = {
            "post": post,
            "post_tags": post.tags.all(),  # 获取文章的所有标签
            "comment_form": comment_form,  # 将表单包含在上下文中，即使验证失败
            "comments": post.comments.all().order_by("-id"),  # 获取文章的所有评论，并按ID倒序排列
            "saved_for_later": self.is_stored_post(request, post.id)  # 检查文章是否已存储
        }
        return render(request, "blog/post-detail.html", context)  # 渲染文章详情模板

# 保存和显示用户稍后阅读的文章视图
class ReadLaterView(View):
    # 处理GET请求，显示存储的文章
    def get(self, request):
        stored_posts = request.session.get("stored_posts")  # 从session中获取存储的文章列表

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []  # 如果没有存储的文章，设置一个空列表
            context["has_posts"] = False  # 标记为没有存储的文章
        else:
            posts = Post.objects.filter(id__in=stored_posts)  # 根据存储的文章ID获取文章
            context["posts"] = posts  # 将获取的文章列表放入上下文
            context["has_posts"] = True  # 标记为有存储的文章

        return render(request, "blog/stored-posts.html", context)  # 渲染存储文章的模板

    # 处理POST请求，添加或移除存储的文章
    def post(self, request):
        stored_posts = request.session.get("stored_posts")  # 从session中获取存储的文章列表

        if stored_posts is None:
            stored_posts = []  # 如果没有存储的文章，初始化为空列表

        post_id = int(request.POST["post_id"])  # 从POST请求中获取文章ID

        if post_id not in stored_posts:
            stored_posts.append(post_id)  # 如果文章ID不在存储列表中，则添加
        else:
            stored_posts.remove(post_id)  # 如果文章ID已在存储列表中，则移除

        request.session["stored_posts"] = stored_posts  # 更新session中的存储文章列表
        
        return HttpResponseRedirect("/")  # 重定向到主页
