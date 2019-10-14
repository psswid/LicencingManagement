from django.db import models

from api.apps.core.models import BaseModel


class Licence(BaseModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField()
    body = models.TextField()
    sold_by = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='licences'
    )
    tags = models.ManyToManyField(
        'licences.Tag', related_name='licences'
    )

    def __str__(self):
        return self.title


class Comment(BaseModel):
    body = models.TextField()

    licence = models.ForeignKey(
        'licences.Licence', related_name='comments', on_delete=models.CASCADE
    )

    sold_by = models.ForeignKey(
        'profiles.Profile', related_name='comments', on_delete=models.CASCADE
    )


class Tag(BaseModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag