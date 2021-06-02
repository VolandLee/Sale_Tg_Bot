import numpy

data = [1, 2, 3, 4, 5]

arr = numpy.array(data)

print(arr)
r_arr = (10 - 6) * numpy.random.random_sample((20,)) + 2
r_arr = r_arr.astype(numpy.int64)
print(r_arr)
ar = numpy.concatenate((arr, r_arr))

a = numpy.arange(16).reshape(4, 4)
b = numpy.ones(16).reshape(4, 4)
l = numpy.concatenate((a, b), axis=1)
print(l)
