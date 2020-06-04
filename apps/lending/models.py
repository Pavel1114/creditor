import uuid
from builtins import property
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db.models import CharField, DecimalField, PositiveIntegerField, ForeignKey, \
    PROTECT, UUIDField, DateField
from django.utils import timezone
from model_utils import Choices
from model_utils.models import TimeStampedModel


def get_birthday_from_iin(iin):
    if int(iin[6]) < 5:
        date_str = '19' + iin[:6]
    else:
        date_str = '20' + iin[:6]
    return datetime.strptime(date_str, '%Y%m%d').date()


def validate_birthday_in_iin(value):
    try:
        birthday = get_birthday_from_iin(value)
    except ValueError:
        raise ValidationError('неверный ИИН', code='invalid_iin')
    if birthday > timezone.now().date():
        raise ValidationError('неверный ИИН', code='invalid_iin_birthday_in_future')


iin_validators = [RegexValidator(r'^\d{12}$', 'ИНН должен состоять из 12 цифр'), validate_birthday_in_iin]


class Borrower(TimeStampedModel):
    iin = CharField('ИНН', validators=iin_validators, max_length=12, unique=True)
    birthday = DateField('дата рождения', editable=False)

    class Meta:
        verbose_name = 'заёмщик'
        verbose_name_plural = 'заёмщики'

    def __str__(self):
        return self.iin

    def save(self, *args, **kwargs):
        self.birthday = get_birthday_from_iin(self.iin)
        super().save(*args, **kwargs)

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.birthday.year - (
                (today.month, today.day) < (self.birthday.month, self.birthday.day))


class Program(TimeStampedModel):
    name = CharField('название', max_length=200)
    min_amount = DecimalField('минимальная сумма кредита', max_digits=20, decimal_places=2)
    max_amount = DecimalField('максимальная сумма кредита', max_digits=20, decimal_places=2)
    min_age = PositiveIntegerField('минимальный возраст заёмщика', default=21, validators=[
        MinValueValidator(18, 'значение не может быть меньше %(limit_value)')])
    max_age = PositiveIntegerField('максимальный возраст заёмщика')

    class Meta:
        verbose_name = 'программа кредитования'
        verbose_name_plural = 'программы кредитования'

    def __str__(self):
        return self.name


class Application(TimeStampedModel):
    STATUSES = Choices(('pending', 'на рассмотрении'), ('approved', 'одобрено'), ('denied', 'отказано'))

    uuid = UUIDField(default=uuid.uuid4)
    program = ForeignKey(Program, verbose_name='программа', on_delete=PROTECT, related_name='applications')
    borrower = ForeignKey(Borrower, verbose_name='заёмщик', on_delete=PROTECT, related_name='applications')
    amount = DecimalField('сумма', max_digits=20, decimal_places=2)
    status = CharField('статус', choices=STATUSES, default=STATUSES.pending, max_length=50)
    reason = CharField('причина отказа', max_length=200, blank=True)

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return f'заявка {self.id}'


class BlackIin(TimeStampedModel):
    iin = CharField('ИНН', validators=iin_validators, max_length=12, unique=True)

    class Meta:
        verbose_name = 'заблокированный ИИН'
        verbose_name_plural = 'заблокированные ИИН'

    def __str__(self):
        return self.iin
