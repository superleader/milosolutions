from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import DateField, PositiveSmallIntegerField
from random import randint


class Account(User):
    birthday = DateField()
    random_number = PositiveSmallIntegerField(default=randint(1, 100))

    def get_absolute_url(self):
        return reverse('account-detail', args=[self.id])