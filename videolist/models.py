import datetime

from django.db import models


# Create your models here.


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Classification(BaseModel):
    list_display = ("title",)
    group = models.CharField(verbose_name="视频分组", max_length=100, blank=True, null=True)
    status = models.BooleanField(verbose_name="状态", default=True)

    def __str__(self):
        return self.group

    class Meta:
        db_table = "classification"
        verbose_name = "视频分类管理"


class Video(BaseModel):
    # status_choice = (
    #     ('0', '发布中'),
    #     ('1', '未发布'),
    # )
    title = models.CharField(verbose_name="标题", max_length=100)
    desc = models.CharField(verbose_name="简介", max_length=1000, blank=True, null=True, default="暂无")
    video_group = models.ForeignKey(verbose_name="视频类", to='Classification', to_field='id', on_delete=models.CASCADE,
                                    null=True)
    file = models.FileField(verbose_name="视频文件", max_length=2000, null=True)
    cover_photo = models.FileField(verbose_name="封面图片", max_length=2000, blank=True, null=True)
    # status = models.CharField(verbose_name="发布状态", max_length=1, choices=status_choice,default=0)

    users_favorite = models.ManyToManyField(verbose_name="喜欢", to="users.Users", related_name="favorite_video")
    users_info = models.ForeignKey(verbose_name="用户", to="users.Users", to_field="id", on_delete=models.CASCADE)
    users_collection = models.ManyToManyField(verbose_name="收藏", to="users.Users", related_name="collected_video")
    users_view_count = models.IntegerField(verbose_name="观看次数", default=0)

    class Meta:
        db_table = 'video'
        verbose_name = "视频管理"

    def user_favorite_count(self):
        return self.users_favorite.count()

    def user_favorite_static(self, user_obj):
        if user_obj in self.users_favorite.all():
            # print("0000", user_obj, self.users_favorite.all())
            return 1
        else:
            return 0

    def user_favorite_rule(self, user_obj):
        if user_obj in self.users_favorite.all():
            self.users_favorite.remove(user_obj)
        else:
            self.users_favorite.add(user_obj)

    def user_collect_count(self):
        return self.users_collection.count()

    def user_collect_static(self, user_obj):
        if user_obj in self.users_collection.all():
            return 1
        else:
            return 0

    def user_collect_rule(self, user_obj):
        if user_obj in self.users_collection.all():
            self.users_collection.remove(user_obj)
        else:
            self.users_collection.add(user_obj)

    def user_comment_count(self):
        num = self.comment_set.count()
        return num

    def __str__(self):
        return f"分类:{self.video_group}    标题:{self.title}"


class Comment(BaseModel):
    video_comment = models.ForeignKey(verbose_name="视频外键", to=Video, to_field="id", on_delete=models.CASCADE)
    user_comment = models.ForeignKey(verbose_name="用户外键", to="users.Users", to_field="id", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="内容", max_length=255)

    class Meta:
        db_table = "comment"
        verbose_name = "评论管理"

    def __str__(self):
        return f"视频id:{self.video_comment.id} 用户id:{self.user_comment.id} 内容:{self.content}"
