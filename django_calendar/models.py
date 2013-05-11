from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django_ical.views import ICalFeed


class Event(models.Model):
    start_datetime = models.DateTimeField(verbose_name=_('Start'), db_index=True)
    end_datetime = models.DateTimeField(verbose_name=_('End'), db_index=True)

    owner = generic.GenericForeignKey()  # The object who owns to this calendar.
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(db_index=True, blank=True, null=True)

    def clean(self):
        if self.start_datetime >= self.end_datetime:
            raise ValidationError('The start datetime may not be later than or equal to the end datetime')
