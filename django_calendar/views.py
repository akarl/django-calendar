# Create your views here.
from django_ical.views import ICalFeed
from django_calendar import api


class EventFeed(ICalFeed):
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'

    def items(self):
        return api.get_events()

    def item_link(self, item):
        return item.owner.get_absolute_url()




