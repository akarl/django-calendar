from __builtin__ import iter
from datetime import datetime
from django_calendar.backends import get_backend


def get_for_object(content_object):
    """
    Returns an iterable or queryset with all the events for a content_type.

    :param content_object:
    :type content_object: Model
    :returns: A queryset or iterable.
    """
    return get_backend().get_for_object(content_object)


def get_for_range(from_date, to_date, content_object=None):
    """
    Gets all <Event> objects between two dates.

    :param from_date: From this date.
    :type from_date: datetime.datetime
    :param to_date: To this date, not including this date.
    :type to_date: datetime.datetime
    :param content_object: The contenttype to filter on.
    :type content_object: ContentType
    :returns: A queryset or iterable.
    """
    return get_backend().get_for_range(from_date, to_date, content_object)


def create(start_datetime, end_datetime, connections, **kwargs):
    """
    Cretes an event.

    :param start_datetime: The date and time for the start of the event.
    :type start_datetime: datetime.datetime
    :param end_datetime: The date and time for the end of the event.
    :type end_datetime: datetime.datetime
    :param connections: The objects connected to this event.
    :type connections: iterable
    :returns: An event object.
    :rtype: Event
    """
    return get_backend().create(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        connections=connections,
        **kwargs
    )
