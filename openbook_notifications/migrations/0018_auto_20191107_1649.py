# Generated by Django 2.2.5 on 2019-11-07 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_communities', '0031_communitynotificationsubscription'),
        ('openbook_notifications', '0017_communitynewpostnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communitynewpostnotification',
            name='community_post_subscription',
        ),
        migrations.AddField(
            model_name='communitynewpostnotification',
            name='community_notification_subscription',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='openbook_communities.CommunityNotificationSubscription'),
            preserve_default=False,
        ),
    ]
