from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    connections = generic.GenericForeignKey()  # The objects connected to this calendar.

    start_datetime = models.DateTimeField(verbose_name=_('Start'), db_index=True)
    end_datedatetime = models.DateTimeField(verbose_name=_('End'), db_index=True)
