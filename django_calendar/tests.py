from collections import Iterable
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django_calendar import api
from django_calendar.api import get_backend


class CalendarTests(TestCase):
    def test_get_backend(self):
        backend = get_backend()
        self.assertTrue(hasattr(backend, 'create_event'))
        self.assertTrue(hasattr(backend, 'get_events'))

    def test_api(self):
        event = api.create_event(
            start_datetime=timezone.now() + timedelta(days=2),
            end_datetime=timezone.now() + timedelta(days=2, hours=1),
        )

        self.assertTrue(event)

        events = api.get_events(
            from_date=timezone.now(),
            to_date=timezone.now() + timedelta(days=7)
        )

        self.assertTrue(isinstance(events, Iterable))
        self.assertTrue(len(events) > 0)

