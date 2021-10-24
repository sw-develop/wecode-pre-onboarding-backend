from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Article.models import Article
from Article.permissions import IsOwner
from Article.serializers import GetArticleSerializer, CreateUpdateArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetArticleSerializer
        elif self.request.method == 'POST' or 'UPDATE':
            return CreateUpdateArticleSerializer

    def get_permissions(self):
        if self.action == 'update' or 'partial_update' or 'destroy':
            permission_classes = [IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    """
    POST /article/ - 글 작성
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create_article(serializer, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create_article(self, serializer, request):
        serializer.save(
            user=request.user  # user 필드 값 설정
        )

    """
    GET /article/<int:pk>/ - 특정 글 확인
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.isAuthorOfArticle(request, instance) is False:  # 작성자가 아닌 다른 사람이 확인한 경우에만 조회수 증가
            instance.increasingViews()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def isAuthorOfArticle(self, request, instance):
        if instance.user == request.user:
            return True
        else:
            return False

    """
    UPDATE /article/<int:pk>/ - 특정 글 수정
    """

    """
    DELETE /article/<int:pk>/ - 특정 글 삭제 
    """
