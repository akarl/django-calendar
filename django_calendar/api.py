from icalendar.cal import Event
from django_calendar.backends import get_backend

get_events = get_backend().get_events
create_event = get_backend().create_event
