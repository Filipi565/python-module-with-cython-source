cpdef factorial(int number):
    cdef int fat
    for i in range(1, number+1):
        fat *= i
    return fat