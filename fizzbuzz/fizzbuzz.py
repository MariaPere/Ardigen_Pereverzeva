def fizzbuzzFunction(number):

        if number % 15 == 0:
            return 'FizzBuzz'

        elif number % 3 == 0:
            return 'Fizz'

        elif number % 5 == 0:
            return 'Buzz'
        else:
            return number

def main():

    n = 1
    m = 10000

    if m <= 10000 and n >= 1 and n < m:

        for number in range(n, m):
            print(fizzbuzzFunction(number))
    else:
        print('wrong parametrs n and m')

if __name__ == '__main__':
    main()
