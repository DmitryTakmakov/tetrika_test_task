def task(array: str) -> int:
    """
    Returns the index of the first 0 in a sorted array of 1s and 0s.
    Array is passed as a string.

    :param array: sorted array
    :return: the index of the first 0
    """
    first_null = array.index('0')
    return first_null


if __name__ == '__main__':
    print(task('111111111111111111111111100000000'))
    # >> OUT: 25
