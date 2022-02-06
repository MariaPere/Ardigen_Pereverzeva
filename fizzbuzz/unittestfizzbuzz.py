import unittest
from fizzbuzz import fizzbuzzFunction

class FizzbuzzTest(unittest.TestCase):

    def testNumberFizz(self):
        for number in [36, 3, 6, 39]:
            print('test', number)
            assert fizzbuzzFunction(number) == 'Fizz'

    def testNumberBuzz(self):

        for number in [5, 10]:
            print('test', number)
            assert fizzbuzzFunction(number) == 'Buzz'

    def testNumberFizzBuzz(self):

        for number in [15, 30, 45, 60]:
            print('test', number)
            assert fizzbuzzFunction(number) == 'FizzBuzz'
