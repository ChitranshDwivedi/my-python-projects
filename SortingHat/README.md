# Sorting Hat

A tiny Python program that sorts you into a Hogwarts house. Enter your name and the Sorting Hat picks one of the four houses at random.

## How It Works

- Asks for your name and strips extra spaces
- Passes the name to a `sort()` function
- `sort()` picks one house at random using `random.choice()`
- Prints the result

Houses: Gryffindor, Slytherin, Hufflepuff, Ravenclaw

## How to Run

1. Make sure Python 3 is installed.
2. Save the code as `sorting_hat.py`.
3. Run it from a terminal:

```
python sorting_hat.py
```

## Example

```
What is your name? Chitransh
Chitransh, you belong in Ravenclaw!
```

(The house is random, so you'll get a different one on different runs.)

## What I Practiced

- Importing and using the `random` module
- Writing functions that take a parameter and return a value
- Using a `main()` function to keep the program organized
- Cleaning input with `.strip()`

## Possible Improvements

- Ask a few personality questions and score the answers instead of picking randomly
- Let the user sort multiple people in one run
- Add a "quit" option
