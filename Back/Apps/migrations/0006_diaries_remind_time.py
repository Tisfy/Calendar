# Generated by Django 3.2 on 2022-02-15 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps', '0005_alter_diaries_publish_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaries',
            name='remind_time',
            field=models.DateTimeField(null=True, verbose_name='提醒时间'),
        ),
    ]
