# Generated by Django 2.2.2 on 2019-06-20 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_common', '0013_language'),
        ('openbook_posts', '0034_auto_20190605_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='openbook_common.Language'),
        ),
    ]