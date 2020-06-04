from datetime import timedelta, datetime
from random import randrange

from factory import DjangoModelFactory, lazy_attribute_sequence

from apps.lending.models import Borrower


class BorrowerFactory(DjangoModelFactory):
    @lazy_attribute_sequence
    def iin(self, n):
        min_birthday_datetime = datetime(1920, 1, 1)
        birthday = min_birthday_datetime + timedelta(
            seconds=randrange((datetime(1999, 1, 1) - min_birthday_datetime).days * 24 * 60 * 60))
        return birthday.strftime('%y%m%d') + f'3{n:05}'

    class Meta:
        model = Borrower
