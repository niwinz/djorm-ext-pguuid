djorm-ext-pguuid
================

PostgreSQL native uuid field for Django.


Introduction
------------

Django by default, has a large collection of possible types that can be used to define the
model. But sometimes we need to use some more complex types offered by PostgreSQL. In this
case, we will look the integrating of PostgreSQL native uuid field with Django.

Compatible with both: python3.3+ and python2.7+


How install it?
---------------

You can clone the repo from github and install with simple python setup.py install
command. Or use a pip, for install it from Python Package Index.

.. code-block:: console

    pip install djorm-ext-pguuid



Quickstart
----------

**djorm-ext-pguuid** exposes a simple django model field `djorm_pguuid.fields.UUIDField`.

This is a sample definition of model using a UUIDField:

.. code-block:: python

    from django.db import models
    from djorm_pguuid.fields import UUIDField
    from djorm_expressions.models import ExpressionManager

    class Register(models.Model):
        # auto_add keyword parameter ensure a random
        # uuid generation if it is not specified.
        id = UUIDField(auto_add=True, primary_key=True)
        name = models.CharField(max_length=200, blank=True)

        objects = ExpressionManager()



Creating objects
~~~~~~~~~~~~~~~~

This is a sample example of creating objects with array fields.

.. code-block:: pycon

    >>> import uuid
    >>> Register.objects.create(id=uuid.UUID("01234644-0126-0113-0123-1123426749ab"))
    <Register: Register object>
    >>> Register.objects.create(id="01234644-0126-0113-0123-1123426749ab")
    <Register: Register object>
