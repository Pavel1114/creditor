from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig


class CreditorAdminSite(AdminSite):
    site_title = 'Creditor'
    site_header = 'Creditor'


class CreditorAdminConfig(AdminConfig):
    default_site = 'config.admin_site.CreditorAdminSite'
