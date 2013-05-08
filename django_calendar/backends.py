from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
import sys
from django_calendar.models import Event


class BaseBackend(object):
    def get_for_object(self, content_object):
        raise NotImplementedError()

    def get_for_range(self, from_date, to_date, content_object=None):
        raise NotImplementedError()

    def create(self, **kwargs):
        raise NotImplementedError()


class ORMBackend(BaseBackend):
    def get_for_object(self, content_object):
        return Event.objects.filter(content_object=content_object)

    def get_for_range(self, from_date, to_date, content_object=None):
        return Event.objects.filter(start_datetime__range=[from_date, to_date], connections=content_object)

    def create(self, **kwargs):
        return Event.objects.create(**kwargs)


def get_backend():
    """
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
