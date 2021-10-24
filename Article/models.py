from django.contrib.auth.models import User
from django.db import models
from django.db.models import F


class Article(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="article_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=32, null=False)
    content = models.TextField(null=False)
    views = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'article'

    def increasingViews(self):  # 조회수 증가
        self.views = F('views') + 1
        self.save()
        self.refresh_from_db()
