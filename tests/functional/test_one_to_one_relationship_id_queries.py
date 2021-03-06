#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import F, Q
from django.test import TransactionTestCase

from tests.common.support.models import TestModel, TestModel2


class PrimaryKeyQueriesTestCase(TransactionTestCase):
    def setUp(self):
        one2one_1 = TestModel2.objects.create(id=1)
        one2one_2 = TestModel2.objects.create(id=2)
        one2one_3 = TestModel2.objects.create(id=3)

        TestModel.objects.create(id=1, one2one=one2one_1)
        TestModel.objects.create(id=2, one2one=one2one_2)
        TestModel.objects.create(id=3, one2one=one2one_3)
        TestModel.objects.create(id=4)

    def test_can_fetch_a_record_equal_to_1(self):
        expected = TestModel.objects.get(one2one_id=1)
        actual = TestModel.objects.get(TestModel.one2one_id == 1)

        self.assertEqual(actual, expected)

    def test_one2one_id_is_1_when_fetching_a_record_with_one2one_id_that_is_equal_to_1(self):
        expected = 1
        actual = TestModel.objects.get(TestModel.one2one_id == 1).one2one_id

        self.assertEqual(actual, expected)

    def test_can_fetch_records_greater_than_1(self):
        expected = TestModel.objects.filter(one2one_id__gt=1)
        actual = TestModel.objects.filter(TestModel.one2one_id > 1)

        self.assertEqual(list(actual), list(expected))

    def test_can_fetch_records_lower_than_2(self):
        expected = TestModel.objects.filter(one2one_id__lt=2)
        actual = TestModel.objects.filter(TestModel.one2one_id < 2)

        self.assertEqual(list(actual), list(expected))

    def test_can_fetch_records_greater_or_equal_to_bar_plus_one(self):
        expected = TestModel.objects.filter(one2one_id__gte=F('bar') + 1)
        actual = TestModel.objects.filter(TestModel.one2one_id >= TestModel.bar + 1)

        self.assertEqual(list(actual), list(expected))

    def test_can_fetch_records_with_one2one_id_greater_than_one_and_bar_equal_to_one(self):
        expected = TestModel.objects.filter(one2one_id__gt=1, bar=1)
        actual = TestModel.objects.filter((TestModel.one2one_id > 1) & (TestModel.bar == 1))

        self.assertEqual(list(actual), list(expected))

    def test_can_fetch_records_with_one2one_id_greater_than_one_or_bar_equal_to_one(self):
        expected = TestModel.objects.filter(Q(one2one_id__gt=1) | Q(bar=1))
        actual = TestModel.objects.filter((TestModel.one2one_id > 1) | (TestModel.bar == 1))

        self.assertEqual(list(actual), list(expected))

    def test_can_fetch_records_with_one2one_baz_equal_to_1(self):
        expected = TestModel.objects.filter(one2one__baz=1)
        actual = TestModel.objects.filter(TestModel.one2one.baz == 1)

        self.assertEqual(list(actual), list(expected))