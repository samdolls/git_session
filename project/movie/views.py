from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Movie, Comment, Tag
from .serializers import MovieSerializer, CommentSerializer, TagSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)

        movie = serializer.instance
        self.handle_tags(movie)

        return Response(serializer.data)
    
    def perform_update(self, serializer):
        movie = serializer.save()
        movie.tag.clear()
        self.handle_tags(movie)

    def handle_tags(self, movie):
        words = movie.content.split(' ')
        tag_list = []
        for w in words:
            if w[0] == '#':
                tag_list.append(w[1:])
        
        for t in tag_list:
            tag, created = Tag.objects.get_or_create(name = t)
            movie.tag.add(tag)
        
        movie.save()
    
class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class MovieCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, movie_id = None):
        movie = get_object_or_404(Movie, id = movie_id)
        queryset = self.filter_queryset(self.get_queryset().filter(movie=movie))
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)
    
    def create(self, request, movie_id = None):
        movie = get_object_or_404(Movie, id = movie_id)
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(movie = movie)
        return Response(serializer.data)
    
class TagViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "name"
    lookup_url_kwarg = "tag_name"

    def retrieve(self, request, *args, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag = get_object_or_404(Tag, name = tag_name)
        movies = Movie.objects.filter(tag = tag)
        serializer = MovieSerializer(movies, many = True)
        return Response(serializer.data)