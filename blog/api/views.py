from django.db.models import Q

from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView,
RetrieveAPIView, RetrieveUpdateAPIView)

from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAdminUser,
IsAuthenticatedOrReadOnly)

from blog.models import Post

from .permissions import IsOwnerOrReadOnly

from .serializers import PostCreateUpdateSerializer, PostDetailSerializer, PostListSerializer

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"

class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self,*args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Post.objects.all()
        #Search Function
        search = self.request.GET.get('q')
        if search:
            queryset_list=queryset_list.filter(
            Q(title__icontains=search)|
            Q(content__icontains=search)|
            Q(user__first_name__icontains=search)|
            Q(user__last_name__icontains=search)
            ).distinct()
        return  queryset_list

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "slug"

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
