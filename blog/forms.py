from django import forms
from .models import Comment

# 定义评论表单类
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # 指定表单对应的模型
        exclude = ["post"]  # 排除不需要在表单中显示的字段
        labels = {
            "user_name": "Your Name",  # 为user_name字段添加标签
            "user_email": "Your Email",  # 为user_email字段添加标签
            "text": "Your Comment"  # 为text字段添加标签
        }
