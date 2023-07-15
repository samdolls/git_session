from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):

    movie = serializers.SerializerMethodField()

    def get_movie(self, instance):
        return instance.movie.name
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['movie']

class MovieSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only = True)
    created_at = serializers.CharField(read_only = True)
    updated_at = serializers.CharField(read_only = True)
    comments = serializers.SerializerMethodField(read_only = True)
    tag = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url = True, required = False)

    class Meta:
        model = Movie
        fields = '__all__'

    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many = True)
        return serializer.data
    
    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    