# -*- coding: utf-8 -*-

import uuid

from django.db import models
from django.test import TestCase

from djorm_pguuid.fields import UUIDField

from .models import Sample1, Sample2, Sample3


class UUIDFieldTests(TestCase):
    def setUp(self):
        Sample1.objects.all().delete()
        Sample2.objects.all().delete()
        Sample3.objects.all().delete()

    def test_explicit_uuid(self):
        obj = Sample1.objects.create(title="foo", uuid='01234644-0126-0113-0123-1123426749ab')
        obj = Sample1.objects.get(pk=obj.pk)
        self.assertEqual(str(obj.pk), '01234644-0126-0113-0123-1123426749ab')

    def test_random_uuid(self):
        obj = Sample1.objects.create(title="foo")
        obj = Sample1.objects.get(pk=obj.pk)

        self.assertIsInstance(obj.uuid, uuid.UUID)

    def test_get_by_uuid_as_uuid_instance(self):
        obj = Sample1.objects.create(title="foo", uuid='01234644-0126-0113-0123-1123426749ab')
        obj = Sample1.objects.get(pk=uuid.UUID("01234644-0126-0113-0123-1123426749ab"))
        self.assertEqual(obj.title, 'foo')

    def test_get_by_uuid_as_str_01(self):
        obj = Sample1.objects.create(title="foo", uuid='01234644-0126-0113-0123-1123426749ab')
        obj = Sample1.objects.get(pk="01234644-0126-0113-0123-1123426749ab")
        self.assertEqual(obj.title, 'foo')

    def test_get_by_uuid_as_str_02(self):
        obj = Sample2.objects.create(title="foo", uuid='01234644-0126-0113-0123-1123426749ab')
        obj = Sample2.objects.get(uuid="01234644-0126-0113-0123-1123426749ab")
        self.assertEqual(obj.title, 'foo')

    def test_create_null_when_can_not(self):
        with self.assertRaises(ValueError):
            Sample2.objects.create(title='foo')

    def test_simple_assignment(self):
        instance = Sample2()
        instance.uuid = "01234644-0126-0113-0123-1123426749ab"
        self.assertIsInstance(instance.uuid, uuid.UUID)

    def test_uuid_editable_01(self):
        uuid_field = Sample1._meta.get_field_by_name('uuid')[0]
        self.assertFalse(uuid_field.editable)

    def test_uuid_editable_02(self):
        uuid_field = Sample2._meta.get_field_by_name('uuid')[0]
        self.assertTrue(uuid_field.editable)

    def test_create_null(self):
        obj = Sample3.objects.create(title='foo')
        self.assertEqual(obj.uuid, None)

    def test_uuid_null_blank_error(self):
        with self.assertRaises(AttributeError):
            class Sample4(models.Model):
                uuid = models.UUIDField(blank=True, null=False)
