# -*- coding: utf-8 -*-

import uuid

from psycopg2.extensions import register_adapter

from django.db.models import Field, SubfieldBase
from django.utils.encoding import force_bytes
from django.utils import six


class UUIDAdapter(object):
    def __init__(self, value):
        if not isinstance(value, uuid.UUID):
            raise TypeError('UUIDAdapter only understands UUID objects.')
        self.value = value

    def getquoted(self):
        return force_bytes(u"'{0}'".format(self.value))


from django.db.models import Field, SubfieldBase


class UUIDField(six.with_metaclass(SubfieldBase, Field)):
    description = 'Universally unique identifier.'

    def __init__(self, auto_add=False, *args, **kwargs):
        self._auto_add = auto_add

        kwargs.setdefault('unique', True)
        kwargs.setdefault('blank', False)

        if auto_add:
            kwargs.setdefault('editable', False)

        if kwargs["blank"] and not kwargs.get('null', False):
            raise AttributeError('Blank UUIDs are stored as NULL. Therefore, setting '
                                 '`blank` to True requires `null` to be True.')

        super(UUIDField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'uuid'

    def get_prep_value(self, value):
        if not value:
            if self.null or self._auto_add:
                return None

            raise ValueError('Explicit UUID required unless either '
                             '`null` or `auto_add` are True.')

        if isinstance(value, uuid.UUID):
            return value

        return uuid.UUID(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        register_adapter(uuid.UUID, UUIDAdapter)
        return super(UUIDField, self).get_db_prep_value(
                     value, connection, prepared=prepared)

    def pre_save(self, instance, add):
        if self._auto_add and add and not getattr(instance, self.attname):
            random_uuid = uuid.uuid4()
            setattr(instance, self.attname, random_uuid)
            return random_uuid

        return super(UUIDField, self).pre_save(instance, add)

    def to_python(self, value):
        if isinstance(value, uuid.UUID) or not value:
            return value
        return uuid.UUID(value)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([(
        (UUIDField,),
        [],
        {
            'auto_add': ['_auto_add', { 'default': False }],
            'unique': ['unique', { 'default': True }],
        },
    )], (r'^djorm_pguuid\.fields\.UUIDField',))
except ImportError:
    pass
