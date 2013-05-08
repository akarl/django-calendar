"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import timedelta
from django.db.models.query import QuerySet

from django.test import TestCase
from django.utils import timezone
from django_calendar import api
from django_calendar.api import get_backend
from django_calendar.backends import BaseBackend


class ORMTest(TestCase):
    def test_get_backend(self):
        backend = get_backend()
        self.assertTrue(isinstance(backend, BaseBackend))

    def test_api_range(self):
        events = api.get_for_range(
            from_date=timezone.now(),
            to_date=timezone.now() + timedelta(days=7)
        )

        self.assertTrue(isinstance(events, QuerySet))

    def test_api_create(self):
        raise NotImplementedError()
        #event = api.create()
