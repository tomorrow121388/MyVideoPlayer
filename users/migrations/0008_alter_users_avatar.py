# Generated by Django 3.2.8 on 2022-09-04 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_users_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.FileField(default='static/avatar/default/default.png', upload_to='avatar/', verbose_name='头像'),
        ),
    ]
