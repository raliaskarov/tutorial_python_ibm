""" this module demonstrates pylint """

# Define a function named 'add' that takes two arguments, 'number1' and 'number2'.
def add(number1, number2):
    """Return sum of two numners
    
    Args:
        number1, number 2 (int or float): numbers to add

    Returns:
        int or float: sum of two
    """

    return number1 + number2

NUM1 = 4
NUM2  = 5

TOTAL = add(NUM1, NUM2)

print(f"The sum of {NUM1} and {NUM2} is {TOTAL}.")
