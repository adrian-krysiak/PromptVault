from django.db import models


# REPOSITORY LAYER
class PromptQuerySet(models.QuerySet):
    def active(self):
        """Returns only active prompts"""
        return self.filter(is_active=True)


class Prompt(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Repo connected to the model
    objects = PromptQuerySet.as_manager()

    def __str__(self):
        return self.title
