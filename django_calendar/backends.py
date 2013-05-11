from collections import Iterable
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
import sys
from django_calendar.models import Event


class BaseBackend(object):
    """
    This backend is a simple backend to Django's ORM.
    If you want to change the model you need to extend this class and change the model attribute.

    If you want to have another type of database you can extend this backend and override the `get_events`
    and the `create_event` methods with your implementation to your database.
    """

    model = Event

    def get_events(self, from_date=None, to_date=None, owner=None):
        """
        Gets all <Event> filtered with the arguments.

        :param from_date: From this date.
        :type from_date: datetime.datetime
        :param to_date: To this date, not including this date.
        :type to_date: datetime.datetime
        :param owner: The owner to filter on.
        :type owner: Model
        :returns: An iterable containing events.
        :rtype: collections.Iterable
        """
        kwargs = {}

        if from_date and to_date:
            kwargs['start_datetime__range'] = [from_date, to_date]

        if owner:
            if isinstance(owner, Iterable):
                kwargs['owner__in'] = owner
            else:
                kwargs['owner'] = owner

        return self.model.objects.filter(**kwargs)

    def create_event(self, start_datetime, end_datetime, owner=None, **kwargs):
        """
        Cretes an event.

        :param start_datetime: The date and time for the start of the event.
        :type start_datetime: datetime.datetime
        :param end_datetime: The date and time for the end of the event.
        :type end_datetime: datetime.datetime
        :param connections: An iterable of objects connected to this event.
        :returns: An event object.
        :rtype: Event
        """
        if owner:
            kwargs['owner'] = owner

        return self.model.objects.create(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            **kwargs
        )


def get_backend():
    """
    This method gets the correct backend from `CALENDAR_BACKEND` in your settings file.

    :rtype: BaseBackend
    """
    backend_path = settings.CALENDAR_BACKEND

    try:
        backend_modulename, backend_classname = backend_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured('{0} isn\'t a backend module'.format(backend_path))

    # See if the module has already been imported.
    try:
        backend_module = sys.modules[backend_modulename]
    except KeyError:
        # ok, then import it.
        try:
            backend_module = import_module(backend_modulename)
        except ImportError as e:
            raise ImproperlyConfigured('Error importing backend {0}: "{1}"'.format(backend_modulename, e))

    try:
        backend_class = getattr(backend_module, backend_classname)
    except AttributeError:
        raise ImproperlyConfigured(
            'Backend module "{0}" does not define a "{1}" class'.format(backend_modulename, backend_classname)
        )

    backend_instance = backend_class()

    if not isinstance(backend_instance, BaseBackend):
        raise ImproperlyConfigured(
            'Backend class "{0}" is not a subclass of "django_calendar.backends.BaseBackend"'.format(backend_classname)
        )

    return backend_instance
