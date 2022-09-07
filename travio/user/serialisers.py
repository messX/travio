from rest_framework import serializers
from rest_framework.settings import api_settings

from travio.user.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(many=True, view_name='article-detail', read_only=True)
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'email', 'username', 'password', 'is_active', 'date_joined', 'last_login', 'articles', 'comments')
        extra_kwargs = {'password': {'write_only': True}}


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()