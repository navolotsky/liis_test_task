from django.conf import settings
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False, help_text="Whether the article is available to non-subscribers.")
    added_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("view_not_public_article", "Can view not public article"),
            ("do_anything", "Can do anything")
        ]
