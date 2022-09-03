# Generated by Django 3.2.8 on 2022-08-20 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=11, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=16, verbose_name='密码')),
                ('gender', models.IntegerField(choices=[(1, '男'), (0, '女')], verbose_name='性别')),
                ('nickname', models.CharField(blank=True, max_length=11, null=True, verbose_name='用户名')),
                ('avatar', models.FileField(upload_to='avatar/', verbose_name='头像')),
                ('mobile', models.CharField(blank=True, max_length=13, null=True, verbose_name='头像')),
                ('subscribe', models.BooleanField(default=False, verbose_name='是否订阅')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]