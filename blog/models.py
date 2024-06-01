from django.db import models
from django.core.validators import MinLengthValidator

# 创建你的模型类

# 标签模型
class Tag(models.Model):
    # 标签名称，最大长度为20
    caption = models.CharField(max_length=20)

    # 返回标签的名称
    def __str__(self):
        return self.caption

# 作者模型
class Author(models.Model):
    # 作者的名字，最大长度为100
    first_name = models.CharField(max_length=100)
    # 作者的姓氏，最大长度为100
    last_name = models.CharField(max_length=100)
    # 作者的电子邮件地址
    email_address = models.EmailField()

    # 返回作者的全名
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # 返回作者的全名
    def __str__(self):
        return self.full_name()

# 帖子模型
class Post(models.Model):
    # 帖子标题，最大长度为150
    title = models.CharField(max_length=150)
    # 帖子摘要，最大长度为200
    excerpt = models.CharField(max_length=200)
    # 帖子图片，可以为空，上传目录为“posts”
    image = models.ImageField(upload_to="posts", null=True)
    # 帖子发布日期，自动设置为当前日期
    date = models.DateField(auto_now=True)
    # 帖子的唯一标识符，用于在URL中引用帖子，具有唯一性和数据库索引
    slug = models.SlugField(unique=True, db_index=True)
    # 帖子内容，最小长度为10
    content = models.TextField(validators=[MinLengthValidator(10)])
    # 帖子的作者，外键引用Author模型，如果作者被删除，则设为NULL，关联名称为“posts”
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    # 帖子的标签，多对多关系引用Tag模型
    tags = models.ManyToManyField(Tag)

    # 返回帖子的标题
    def __str__(self):
        return self.title

# 评论模型
class Comment(models.Model):
    # 用户名，最大长度为120
    user_name = models.CharField(max_length=120)
    # 用户电子邮件地址
    user_email = models.EmailField() 
    # 评论文本，最大长度为400
    text = models.TextField(max_length=400)
    # 评论对应的帖子，外键引用Post模型，帖子被删除时，评论也被删除，关联名称为“comments”
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")

    # 返回用户名
    def __str__(self):
        return self.user_name
