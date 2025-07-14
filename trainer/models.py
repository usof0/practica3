from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    english = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    example = models.TextField(blank=True, null=True)
    is_learned = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.english} - {self.translation}"

    def get_absolute_url(self):
        return reverse('word-list')

    class Meta:
        ordering = ['-created_at']

class WordImport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='word_imports/')
    imported_at = models.DateTimeField(auto_now_add=True)
    words_imported = models.PositiveIntegerField(default=0)
