# Swapping two  numbers (without using third variable)
"""a = 18
b = 29

temp = a
a = b
b = temp

print("After swap :",a,b)



a = 5
b = 9

a = a+b
b =a-b
a =a-b

print("After swap: ",a, b)


a , b = 8 , 2
a , b = 2 ,8

print("After swap : ", a ,b)"""

# check whether a number is even or odd

"""num = int(input("Enter a number: "))
if num % 2 ==0:
    print(f"{num} is even")
else:
    print(f"{num} is odd")


num = int(input("Enter a number: "))
if num & 1:
    print(f"{num} is odd")
else:
    print(f"{num} is even")"""



# check leap year
"""
number = int(input("Enter year : "))
if(number % 4 ==0 and number % 100 !=0) or (number %400 ==0):
     print(f"{number} is leap year")
else:
    print(f"{number} is not a leap year")
"""

#comupte the sum of first n natural number

"""a = int(input("Enter First number: "))
b = int(input("Enter Second number:"))

sum = a + b
print("Sum of First and Second number is :", sum)


a = 245
b = 3737
sum = a+b
print("Sum of a and b is: ",sum)

print(4566 + 656563)"""

#compute the first n fibonacci numbers

"""num = int(input("Enter a number: "))
a,b =0,1
print("Fibonacci series sequence:")
for i in range(num):
    print(a, end ="  ")
    a,b =b ,a+b
    """