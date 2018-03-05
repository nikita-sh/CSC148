"""
Queue lab function.
"""

from csc148_queue import Queue


def list_queue(lst: list, q: Queue):
    """
    Takes all elements of a given list and adds them to the queue. Then, checks
    the queue for items that are not lists and prints them. If the item being
    checked is a list, it is added to the queue. This process repeats until it
    is empty.

    >>> q = Queue()
    >>> l1 = [1, 3, 5]
    >>> l2 = [1, [3, 5], 7]
    >>> l3 = [1, [3, [5, 7], 9], 11]
    >>> list_queue(l1, q)
    1
    3
    5
    >>> list_queue(l2, q)
    1
    7
    3
    5
    >>> list_queue(l3, q)
    1
    11
    3
    9
    5
    7
    """
    for i in lst:
        q.add(i)
    while not q.is_empty():
        nxt = q.remove()
        if type(nxt) != list:
            print(nxt)
        else:
            for i in nxt:
                q.add(i)


if __name__ == "__main__":
    q = Queue()
    val = int(input("Enter an integer:"))
    if val == 148:
        pass
    else:
        q.add(val)
    while val != 148:
        val = int(input("Enter an integer:"))
        if val == 148:
            break
        else:
            q.add(val)
    total = 0
    while not q.is_empty():
        total += q.remove()
    print(total)
