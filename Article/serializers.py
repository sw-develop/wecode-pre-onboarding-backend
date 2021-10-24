from rest_framework import serializers

from Article.models import Article


# 글 작성 및 수정
class CreateUpdateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content']


# 특정 글 조회
class GetArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        depth = 1
