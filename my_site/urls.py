"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # 管理站点的URL配置
    path('admin/', admin.site.urls),
    # 包含blog应用的URL配置
    path("", include("blog.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 这一行代码添加了静态文件（如图片、视频等）的URL模式，以便在开发环境中能够访问这些文件。
# settings.MEDIA_URL 是媒体文件的基本URL路径，例如 '/media/'。
# settings.MEDIA_ROOT 是媒体文件存储的实际文件系统路径。

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# 这一行代码添加了静态文件（如CSS、JavaScript等）的URL模式，以便在开发环境中能够访问这些文件。
# settings.STATIC_URL 是静态文件的基本URL路径，例如 '/static/'。
# settings.STATIC_ROOT 是静态文件存储的实际文件系统路径。
