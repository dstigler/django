import sys
import datetime
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay, BDay,BusinessDay, CustomBusinessHour
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, DateOffset, EasterMonday, Easter, MO,  Day, next_monday, previous_friday
from enum import Enum
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from customers.models import Customer

holidays = [

        Holiday('Neujahrstag', month=1, day=1),
        Holiday('Heilige Drei Könige', month=1, day=6),
        EasterMonday,
        Holiday('Staatsfeiertag', month=5, day=1),
        Holiday('Christi Himmelfahrt', month=1, day=1, offset=[Easter(), Day(39)]),
        Holiday('Pfingstmontag', month=1, day=1, offset=[Easter(), Day(50)]),
        Holiday('Fronleichnam', month=1, day=1, offset=[Easter(), Day(60)]),
        Holiday('Mariä Himmelfahrt', month=8, day=15),
        Holiday('Nationalfeiertag', month=10, day=26),
        Holiday('Allerheiligen', month=11, day=1),
        Holiday('Mariä Empfängnis', month=12, day=8),
        Holiday('Erster Weihnachtstag', month=12, day=25),
        Holiday('Zweiter Weihnachtstag', month=12, day=26),
    ]
class AustriaBusinessCalendar(AbstractHolidayCalendar):
    rules = holidays

calendar=AustriaBusinessCalendar()


class OrderState(Enum):
    Open = "Open"
    Started = "Started"
    Finished = "Finished"

class Order(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(default=timezone.timedelta(days=1))
    date_pickup = models.DateTimeField()
    date_start = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.Empty) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(
        max_length=10,
        default=OrderState.Open.value,
        choices=[(tag.name, tag.value) for tag in OrderState]  # Choices is a list of Tuple
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk': self.pk}) 

    def get_startdate(self):

        # today = pd.datetime.today()
        # print(today)
        # print( today - BDay(4))
        # return self.date_pickup - BDay(self.duration.days())
        #print(calendar.holidays(start='2020-01-01', end='2020-12-31'))
        start_after_calculation = self.date_pickup - CustomBusinessDay(self.duration.days, calendar=calendar)
        if self.duration.seconds > 0:
            start_after_calculation = start_after_calculation - CustomBusinessHour(self.duration.seconds//3600, calendar=calendar, start='06:59', end='14:59') # - datetime.timedelta(seconds=self.duration.seconds);  
        return start_after_calculation

    def get_state_visualisation(self):
        urgency = self.get_state_urgency()
        if urgency == 0:
            return "-success"
        elif urgency == 2:
            return "-warning"
        elif urgency == 3:
            return "-danger"
        return ""

    def get_state_urgency(self):
        #print('{0} ID:{1} Start:{2} Pickup:{3}'.format(timezone.now(), self.pk, self.get_startdate(), self.date_pickup))
        if self.state == OrderState.Finished.name:
            return 0
        elif self.state in (OrderState.Started.name, OrderState.Open.name) and self.date_pickup < timezone.now():
            return 3
        elif self.state == OrderState.Open.name and self.date_start < timezone.now():
            return 2
        return 1