# Python Calculator

A simple command-line calculator written in Python. It supports addition, subtraction, multiplication, and division, and keeps running until you type `quit`.

## Features

- Four operations: add, subtract, multiply, divide
- Each operation is its own function
- Handles invalid input (letters instead of numbers, unknown operations) without crashing
- Handles division by zero with a friendly message
- Type `quit` at any prompt to exit

## How to Run

1. Make sure Python 3 is installed.
2. Save the code as `calculator.py`.
3. Run it from a terminal:

```
python calculator.py
```

## Example

```
Enter first number. 12
Enter second number. 4
add / subtract / multiply / divide ? divide
The division of the two numbers gives : 3.0
Enter first number. quit
```

## What I Practiced

- Writing and calling functions with `return`
- `while` loops with `break`
- `try` / `except` for `ValueError` and `ZeroDivisionError`
- `if` / `elif` / `else` chains

## Possible Improvements

- Support decimal numbers (use `float` instead of `int`)
- Add more operations (power, modulus)
- Build a Tkinter GUI version
