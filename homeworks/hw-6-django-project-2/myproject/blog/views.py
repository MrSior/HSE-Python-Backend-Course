from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Count, Avg
from rest_framework.response import Response
from .models import User, Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        aggregated_data = Post.objects.aggregate(
            total_posts=Count('id'),
        )
        return Response(aggregated_data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='by-post/(?P<post_id>\d+)')
    def by_post(self, request, post_id=None):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='by-post/(?P<post_id>\d+)')
    def by_post(self, request, post_id=None):
        likes_count = Like.objects.filter(post_id=post_id).count()
        return Response({"post_id": post_id, "likes_count": likes_count})