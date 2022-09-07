from django.db import models


# Create your models here.

class LiveStreaming(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    camera_username = models.CharField(verbose_name="摄像头用户名", max_length=64, blank=True, null=True)
    camera_password = models.CharField(verbose_name="摄像头密码", max_length=64, blank=True, null=True)
    camera_ip = models.CharField(verbose_name="设备IP", max_length=64, blank=True, null=True)
    camera_port = models.IntegerField(verbose_name="设备端口", blank=True, null=True)

    live_photo = models.FileField(verbose_name="封面图", upload_to='static/streaming_photo/')
    live_title = models.CharField(verbose_name="直播标题", max_length=32)
    live_desc = models.CharField(verbose_name="直播描述", max_length=64)

    class Meta:
        db_table = "livestreaming"
        verbose_name = "直播管理"

    def __str__(self):
        return self.live_title
