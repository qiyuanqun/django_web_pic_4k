from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField


# Create your models here.
class Pic_4k(models.Model):
    '''4k图片模型类'''
    img_name = models.CharField(max_length=250)  # 名字
    img_path = models.CharField(max_length=250)  # 路径
    img_cls = models.CharField(max_length=15)  # 分类
    img_size = models.CharField(max_length=250)  # 尺寸

    # 已经在底层操作设置为自动填写
    img_cre_time = models.DateTimeField()  # 添加时间

    def __str__(self):
        return self.img_name

    class Meta:
        db_table = 'pic_4k'  # 表名

class User(AbstractUser):
    '''用户模型类'''
    # 自动填写
    reg_time = models.DateTimeField(auto_now_add=True)  # 注册时间

    class Meta:
        db_table = 'user'  # 表名

class UploadFile(models.Model):
    '''上传文件模型类'''
    file_name = models.CharField(max_length=250)  # 文件名
    file_desc = HTMLField(blank=True)  # 文件简介
    file_path = models.CharField(max_length=250)  # 路径
    file_size = models.CharField(max_length=15)  # 尺寸

    file_up_time = models.DateTimeField(auto_now_add=True)  # 上传时间 django自动填写
    file_down_num = models.IntegerField(default=0)  # 下载次数 默认0

    file_user = models.ForeignKey('User')  # 上传用户

    class Meta:
        db_table = 'upload_file'