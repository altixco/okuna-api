# Generated by Django 2.2.4 on 2019-08-12 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_auth', '0043_auto_20190710_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotificationssettings',
            name='post_comment_user_mention_notifications',
            field=models.BooleanField(default=True, verbose_name='post comment user mention notifications'),
        ),
        migrations.AddField(
            model_name='usernotificationssettings',
            name='post_user_mention_notifications',
            field=models.BooleanField(default=True, verbose_name='post user mention notifications'),
        ),
    ]
