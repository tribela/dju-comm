from django.db import models


class SchoolEmailDomain(models.Model):
    domain = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.domain
