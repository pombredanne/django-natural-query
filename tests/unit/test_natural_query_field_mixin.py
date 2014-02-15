#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import expectedFailure

from django.db.models import Q, F, Field
from django.test import SimpleTestCase
from mock import sentinel, patch

from natural_query.mixins import NaturalQueryFieldMixin
from tests.unit.support import patch_q_objects_equality, patch_f_objects_equality


class NaturalQueryFieldMixinTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        patch_q_objects_equality()
        patch_f_objects_equality()

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    @property
    def system_under_test(self):
        sut = NaturalQueryFieldMixin()
        sut.name = 'field'

        return sut

    @property
    def field(self):
        return Field(name=sentinel.FIELD_NAME)

    def test_equals_operator_generates_the_right_expression_for_the_exact_lookup(self):
        sut = self.system_under_test
        expected = Q(field__exact=sentinel.VALUE)

        actual = sut == sentinel.VALUE

        self.assertEqual(actual, expected)

    def test_concated_equals_operator_generates_the_right_expression_for_the_exact_lookup(self):
        sut = self.system_under_test
        expected = Q(field__exact=sentinel.VALUE)

        actual = sentinel.VALUE == sut == sentinel.VALUE

        self.assertEqual(actual, expected)

    def test_equals_operator_generates_the_right_expression_for_the_exact_lookup_when_comparing_to_another_field(self):
        sut = self.system_under_test
        expected = Q(field__exact=F(sentinel.FIELD_NAME))

        actual = sut == self.field

        self.assertEqual(actual, expected)

    def test_greater_than_operator_generates_the_right_expression_for_the_gt_lookup(self):
        sut = self.system_under_test
        expected = Q(field__gt=sentinel.VALUE)

        actual = sut > sentinel.VALUE

        self.assertEqual(actual, expected)

    def test_greater_than_operator_generates_the_right_expression_for_the_gt_lookup_when_comparing_to_another_field(self):
        sut = self.system_under_test
        expected = Q(field__gt=F(sentinel.FIELD_NAME))

        actual = sut > self.field

        self.assertEqual(actual, expected)

    def test_greater_than_or_equal_operator_generates_the_right_expression_for_the_gte_lookup(self):
        sut = self.system_under_test
        expected = Q(field__gte=sentinel.VALUE)

        actual = sut >= sentinel.VALUE

        self.assertEqual(actual, expected)

    def test_greater_than_or_equal_operator_generates_the_right_expression_for_the_gte_lookup_when_comparing_to_another_field(self):
        sut = self.system_under_test
        expected = Q(field__gte=F(sentinel.FIELD_NAME))

        actual = sut >= self.field

        self.assertEqual(actual, expected)

    def test_less_than_operator_generates_the_right_expression_for_the_lt_lookup(self):
        sut = self.system_under_test
        expected = Q(field__lt=sentinel.VALUE)

        actual = sut < sentinel.VALUE

        self.assertEqual(actual, expected)

    def test_less_than_operator_generates_the_right_expression_for_the_lt_lookup_when_comparing_to_another_field(self):
        sut = self.system_under_test
        expected = Q(field__lt=F(sentinel.FIELD_NAME))

        actual = sut < self.field

        self.assertEqual(actual, expected)

    def test_less_than_or_equal_operator_generates_the_right_expression_for_the_lte_lookup(self):
        sut = self.system_under_test
        expected = Q(field__lte=sentinel.VALUE)

        actual = sut <= sentinel.VALUE

        self.assertEqual(actual, expected)

    def test_less_than_or_equal_operator_generates_the_right_expression_for_the_lte_lookup_when_comparing_to_another_field(self):
        sut = self.system_under_test
        expected = Q(field__lte=F(sentinel.FIELD_NAME))

        actual = sut <= self.field

        self.assertEqual(actual, expected)

    def test_not_equal_operator_generates_the_right_negated_expression_for_the_exact_lookup(self):
        sut = self.system_under_test
        expected = ~Q(field__exact=sentinel.VALUE)

        actual = sut != sentinel.VALUE

        self.assertEqual(actual, expected)

    def test_not_equal_operator_generates_the_right_negated_expression_for_the_exact_lookup_when_comparing_to_another_field(self):
        sut = self.system_under_test
        expected = ~Q(field__exact=F(sentinel.FIELD_NAME))

        actual = sut != self.field

        self.assertEqual(actual, expected)

    def test_concated_gte_operator_generates_the_right_expression_for_the_greater_than_or_equal_lookup(self):
        """
        This should generate an expression that picks the lower value for comparison.
        """
        sut = self.system_under_test
        expected = Q(field__gte=sentinel.LOWER_VALUE)

        actual = sentinel.HIGHER_VALUE <= sut >= sentinel.LOWER_VALUE

        self.assertEqual(actual, expected)

    def test_concated_gt_operator_generates_the_right_expression_for_the_greater_than_lookup(self):
        """
        This should generate an expression that picks the lower value for comparison.
        """
        sut = self.system_under_test
        expected = Q(field__gt=sentinel.LOWER_VALUE)

        actual = sentinel.HIGHER_VALUE < sut > sentinel.LOWER_VALUE

        self.assertEqual(actual, expected)


class NaturalQueryFieldMixinUnsupportedOperationsTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        patch_q_objects_equality()
        patch_f_objects_equality()

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    @property
    def system_under_test(self):
        sut = NaturalQueryFieldMixin()
        sut.name = 'field'

        return sut

    @property
    def field(self):
        return Field(name=sentinel.FIELD_NAME)

    @expectedFailure
    def test_concated_equals_operator_generates_the_wrong_expression_for_the_exact_lookup(self):
        sut = self.system_under_test
        expected = Q(field__exact=sentinel.VALUE)

        actual = sut == sentinel.VALUE == sentinel.VALUE

        self.assertEqual(actual, expected)

    @expectedFailure
    def test_concated_greater_than_or_equals_operator_generates_the_wrong_expression_for_the_range_lookup(self):
        sut = self.system_under_test
        expected = Q(field__range=[sentinel.LOWER_VALUE, sentinel.HIGHER_VALUE])

        actual = sentinel.HIGHER_VALUE >= sut >= sentinel.LOWER_VALUE

        self.assertEqual(actual, expected)

