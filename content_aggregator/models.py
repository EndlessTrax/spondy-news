from django.db import models


CATEGORY_CHOICES = [("NEWS", "News"), ("RESEARCH", "Research"), ("EVENTS", "Events")]


class Entry(models.Model):
    class Meta:
        verbose_name_plural = "entries"

    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self) -> str:
        return f"{self.title} - Published on {self.pub_date}"
