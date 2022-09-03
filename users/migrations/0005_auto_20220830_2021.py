# Generated by Django 3.2.8 on 2022-08-30 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_users_introduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='introduct',
            field=models.CharField(default='这个人很懒，不会写简介！', max_length=63, verbose_name='简介'),
        ),
        migrations.AlterField(
            model_name='users',
            name='nickname',
            field=models.CharField(max_length=11, verbose_name='用户名'),
        ),
    ]