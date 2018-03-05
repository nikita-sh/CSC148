"""
Stack lab function.
"""

from stack import *


def list_stack(lst: list, s: Stack):
    """
    Takes all elements of a given list and adds them to the stack. Then, checks
    the stack for items that are not lists and prints them. If the item being
    checked is a list, it is added to the stack. This process repeats until it
    is empty.

    >>> s = Stack()
    >>> l = [1, 3, 5]
    >>> list_stack(l, s)
    5
    3
    1
    >>> l2 =  [1, [3, 5], 7]
    >>> list_stack(l2, s)
    7
    5
    3
    1
    >>> l3 = [1, [3, [5, 7], 9], 11]
    >>> list_stack(l3, s)
    11
    9
    7
    5
    3
    1
    """
    for i in lst:  # Adds each element of list to the stack
        s.add(i)
    while not s.is_empty():
        nxt = s.remove()
        if type(nxt) != list:
            print(nxt)
        else:
            for i in nxt:
                s.add(i)


if __name__ == "__main__":
    s = Stack()
    text = input("Type a string:")
    if text == 'end':
        pass
    else:
        s.add(text)
    while text != 'end':
        text = input("Type a string:")
        if text == 'end':
            break
        else:
            s.add(text)
    while not s.is_empty():
        print(s.remove())
