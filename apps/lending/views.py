from django.db import transaction
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.lending.models import Application, Program, Borrower
from apps.lending.serializers import ApplicationSerializer, ProgramSerializer, ApplicationCreateSerializer, \
    BorrowerSerializer
from apps.lending.tasks import check_application


class BorrowerViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer


class ApplicationViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrower_data = serializer.validated_data.pop('borrower')
        borrower, created = Borrower.objects.get_or_create(**borrower_data)
        application = serializer.save(borrower=borrower)
        transaction.on_commit(lambda: check_application.delay(application.id))
        headers = self.get_success_headers(serializer.data)
        full_serializer = ApplicationSerializer(application, context={'request': request})
        return Response(full_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProgramViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
