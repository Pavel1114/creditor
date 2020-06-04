import requests
from django.core.exceptions import ValidationError

from apps.lending.models import Application
from config.celery import app


def program_validator(application):
    borrower = application.borrower
    program = application.program
    if not (program.min_age < borrower.age < program.max_age):
        raise ValidationError('не проходит по возрасту')
    if not (program.min_amount < application.amount < program.max_amount):
        raise ValidationError('не проходит по сумме кредита')


def iin_is_ip_validator(application):
    try:
        res = requests.get('https://stat.gov.kz/api/juridical/gov/',
                           params={'lang': 'ru', 'bin': application.borrower.iin})
        if res.status_code == 200 and res.json()['success']:
            raise ValidationError('ИИН принадлежит ИП')
        
    except ValidationError as e:
        raise e
    except:
        # todo необходимо обрабатывать ошибки связанные с запросами
        pass


validators = [iin_is_ip_validator, program_validator]


@app.task
def check_application(application_pk):
    application = Application.objects.get(pk=application_pk)
    try:
        for validator in validators:
            validator(application)
    except ValidationError as e:
        application.status = Application.STATUSES.denied
        application.reason = e.message
        application.save()
    else:
        application.status = Application.STATUSES.approved
        application.save()
