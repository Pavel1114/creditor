from rest_framework.fields import SerializerMethodField, ReadOnlyField
from rest_framework.reverse import reverse
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from apps.lending.models import Application, Program, Borrower, iin_validators


class BorrowerSerializer(ModelSerializer):
    age = ReadOnlyField()

    class Meta:
        model = Borrower
        fields = ['iin', 'birthday', 'age']
        read_only_fields = ['birthday']
        # override validators for exclude unique checking
        extra_kwargs = {'iin': {'validators': iin_validators}}


class ProgramSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Program
        fields = ['name', 'min_amount', 'max_amount', 'min_age', 'max_age']


class ApplicationSerializer(HyperlinkedModelSerializer):
    url = SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'uuid', 'url', 'created', 'program', 'borrower', 'amount', 'status', 'reason']

    def get_url(self, obj):
        request = self.context.get('request', None)
        return reverse('application-detail', kwargs={'uuid': obj.uuid}, request=request)


class ApplicationCreateSerializer(ModelSerializer):
    borrower = BorrowerSerializer(label='заёмщик')

    class Meta:
        model = Application
        fields = ['program', 'amount', 'borrower']
