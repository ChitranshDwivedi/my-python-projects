def add(a, b):
    c = a + b
    return c    

def subtract(a, b):
    d = a - b
    return d

def multiply(a,b):
    p = a * b
    return p

def divide(a,b):
    q = a / b
    return q

while True:
    try:     
        a = input("Enter first number. ")
        if a == "quit":
            break
        a = int(a)

        b = input("Enter second number. ")
        if b == "quit":
            break
        b = int(b)

        x = input("add / subtract / multiply / divide ? ")
        if x == "quit":
            break

        if x == "add":
            print (f"The sum of the two numbers is : {add(a,b)}")
        
        elif x == "subtract":
            print (f"The difference of the two numbers is : {subtract(a,b)}")

        elif x == "multiply":
            print (f"The multiplication of the two numbers gives : {multiply(a,b)}")

        elif x == "divide":
            print (f"The division of the two numbers gives : {divide(a,b)}")

        else:
            print("Invalid Input. Try again.")

    except ValueError:
        print("Invalid Input. Try again.")
    
    except ZeroDivisionError:
        print("cannot divide by zero.")
