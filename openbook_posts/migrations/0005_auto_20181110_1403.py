# Generated by Django 2.1.3 on 2018-11-10 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_posts', '0004_auto_20181022_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(blank=True, max_length=560, null=True, verbose_name='text'),
        ),
    ]