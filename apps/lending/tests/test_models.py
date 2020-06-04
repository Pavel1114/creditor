from django.test import TestCase

from apps.lending.tests.factories import BorrowerFactory


class TestBorrowerModel(TestCase):
    def test_str_method(self):
        borrower = BorrowerFactory.create()
        self.assertEqual(borrower.iin, str(borrower))
