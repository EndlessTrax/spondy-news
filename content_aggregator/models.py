from django.db import models


CATEGORY_CHOICES = [
    ("ARTICLE", "Article"),
    ("RESEARCH", "Research"),
    ("EVENT", "Event"),
]


class Entry(models.Model):
    class Meta:
        verbose_name_plural = "entries"

    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField(unique=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"
