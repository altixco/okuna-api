# Generated by Django 2.2 on 2019-04-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_auth', '0030_user_invite_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='invite_count',
            field=models.SmallIntegerField(default=0),
        ),
    ]
