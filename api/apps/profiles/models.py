from django.db import models

from api.apps.core.models import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )

    bio = models.TextField(blank=True)

    image = models.URLField(blank=True)

    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )

    sold = models.ForeignKey(
        'licences.Licence',
        related_name='sold_by',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        self.follows.add(profile)

    def unfollow(self, profile):
        self.follows.remove(profile)

    def is_following(self, profile):
        return self.follows.filter(pk=profile.pk).exists()

    def sold(self, licence):
        self.sold.add(licence)

    def has_solded(self, licence):
        return self.sold.filter(pk=licence.pk).exists()