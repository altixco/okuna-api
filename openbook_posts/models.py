# Create your models here.
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your views here.
from openbook_auth.models import User
from openbook_posts.validators import hex_color_validator


class Post(models.Model):
    text = models.CharField(_('text'), max_length=560, blank=False, null=False)
    created = models.DateTimeField(editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(Post, self).save(*args, **kwargs)


class PostImage(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(_('image'), blank=False, null=False)


class PostComment(models.Model):
    created = models.DateTimeField(editable=False)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_comments')
    text = models.CharField(_('text'), max_length=280, blank=False, null=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(PostComment, self).save(*args, **kwargs)


class PostReaction(models.Model):
    created = models.DateTimeField(editable=False)
    reactor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(PostReaction, self).save(*args, **kwargs)


class PostReactionEmoji(models.Model):
    name = models.CharField(_('name'), max_length=32, blank=False, null=False)
    shortcut = models.CharField(_('shortcut'), max_length=16, blank=False, null=False)
    # Hex colour. #FFFFFF
    color = models.CharField(_('color'), max_length=7, blank=False, null=False, validators=[hex_color_validator])
    image = models.ImageField(_('image'), blank=False, null=False)
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(PostReactionEmoji, self).save(*args, **kwargs)
