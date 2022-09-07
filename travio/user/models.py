from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from pytz import unicode

from travio.travio import settings


class MyUserManager(BaseUserManager):

    def create_user(self, email, username, password):
        """
        Creates and saves a User with the given email and password
        """
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        if not password:
            raise ValueError('User must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=100,
        unique=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_admin = models.BooleanField(
        default=False
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    objects = MyUserManager()

    USER_NAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'email']

    class Meta:
        ordering = ['-id']

    @property
    def is_staff(self):
        return self.is_admin


class Article(models.Model):
    author = models.ForeignKey(
        User,
        related_name='articles'
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=getattr(settings, 'ARTICLE_TITLE_MAX_LENGTH', None)
    )
    context = models.TextField(
        max_length=getattr(settings, 'ARTICLE_CONTEXT_MAX_LENGTH', None)
    )
    hits = models.PositiveIntegerField(
        default=0
    )
    state_choices = (
        ('shown', 'Shown'),
        ('deleted', 'Deleted'),
    )
    state = models.CharField(
        verbose_name=_('State'),
        max_length=10,
        choices=state_choices,
        default='shown'
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created datetime'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated datetime'),
        auto_now=True
    )

    class Meta:
        ordering = ['-id']

class Comment(models.Model):
    """
    Comment under specific article
    """
    article = models.ForeignKey(
        Article,
        related_name = 'comments'
    )
    author = models.ForeignKey(
        User,
        related_name = 'comments'
    )
    context = models.TextField(
        verbose_name = _('Context'),
        max_length = getattr(settings, 'COMMENT_CONTEXT_MAX_LENGTH', None)
    )
    state_choices = (
        ('shown', 'Shown'),
        ('deleted', 'Deleted'),
    )
    state = models.CharField(
        max_length = 10,
        choices = state_choices,
        default = 'shown'
    )
    created_at = models.DateTimeField(
        verbose_name = _('Created datetime'),
        auto_now_add = True,
        editable = False
    )
    updated_at = models.DateTimeField(
        verbose_name = _('Updated datetime'),
        auto_now = True
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.id) or u''