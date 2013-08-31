# -*- coding: utf-8 -*-

from django.db import models
from djorm_pguuid.fields import UUIDField


class Sample1(models.Model):
    uuid = UUIDField(auto_add=True, primary_key=True)
    title = models.CharField(max_length=250)


class Sample2(models.Model):
    uuid = UUIDField()
    title = models.CharField(max_length=250)


class Sample3(models.Model):
    uuid = UUIDField(null=True)
    title = models.CharField(max_length=250)
