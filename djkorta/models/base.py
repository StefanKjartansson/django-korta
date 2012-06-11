#!/usr/bin/env python
# -*- coding: utf-8 -
"""
djkorta.models.base
~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by the Stefán Kjartansson, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext as _

from model_utils.models import TimeStampedModel

from .. import korta_reference


class ReferenceCommon(TimeStampedModel):
    """
    Abstract model for Korta related classes, all reference
    generation is delegated here.
    """

    reference = models.CharField(verbose_name=_(u'Reference'), max_length=20,
        unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            ref = korta_reference()
            while self.__class__.objects.filter(reference=ref).exists():
                ref = korta_reference()
            self.reference = ref
        super(ReferenceCommon, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-created', ]
