from unittest import TestCase
from django.test import TestCase
from app.calc import add, subtract


class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that two number are added together"""
        self.assertEqual(add(3, 8), 11)
        
    def test_subtract_number(self):
        """Test that two number are added together"""
        self.assertEqual(subtract(5, 3), 2)
