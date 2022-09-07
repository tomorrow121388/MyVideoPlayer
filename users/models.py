from django.db import models


# Create your models here.


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Users(BaseModel):
    username = models.CharField(verbose_name="账号", max_length=11, unique=True)
    password = models.CharField(verbose_name="密码", max_length=128)
    gender_choice = (
        (1, "男"),
        (0, "女")
    )
    gender = models.IntegerField(verbose_name="性别", choices=gender_choice)
    nickname = models.CharField(verbose_name="用户名", max_length=11)
    avatar = models.FileField(verbose_name="头像", upload_to='avatar/', default="static/avatar/default/default.png")
    mobile = models.CharField(verbose_name="手机号", blank=True, null=True, max_length=13)
    # subscribe = models.BooleanField(verbose_name="是否订阅", default=False)
    introduct = models.CharField(verbose_name="简介", max_length=63, default="这个人很懒，不会写简介！")

    class Meta:
        db_table = "Users"
        verbose_name = "用户管理"

    def __str__(self):
        return self.nickname
