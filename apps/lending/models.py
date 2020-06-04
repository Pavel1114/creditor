import uuid

from django.core.validators import RegexValidator, MinValueValidator
from django.db.models import CharField, DecimalField, PositiveIntegerField, ForeignKey, \
    PROTECT, UUIDField, DateField
from model_utils import Choices
from model_utils.models import TimeStampedModel


class Borrower(TimeStampedModel):
    iin = CharField('ИНН', validators=[RegexValidator(r'^\d{12}$', 'ИНН должен состоять из 12 цифр')],
                    max_length=12, unique=True)
    birthday = DateField('дата рождения', editable=False)

    class Meta:
        verbose_name = 'заёмщик'
        verbose_name_plural = 'заёмщики'

    def __str__(self):
        return self.iin


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
