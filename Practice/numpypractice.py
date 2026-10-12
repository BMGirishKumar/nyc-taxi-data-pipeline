import numpy as np

#array=np.array([[['a','b','c','d','e'],['f','g','h','i','j']]
#                ,[['k','l','m','n','o'],['p','q','r','s','t']]])


#word=array[0,0,0] + array[1,1,0]

#print(word)
#print(array[0,1,2])
#print(array.shape)
#print(array.ndim)
#print(type(array))


#array=np.array([[1,2,3,4],
#                [5,6,7,8],
#                [9,10,11,12],
#                [13,14,15,16]])

#array[start:end:step]

#print(array[::2])

#print(array[0:2,2:])


#Scalar arithmetic operations on numpy arrays

#array=np.array([1,2,3,4])

#print(array+2)
#print(array ** 2)


#Vector arithmetic operations on numpy arrays

#array=np.array([1.01,2.5,3.3,4.44])

#print(np.sqrt(array))
#print(np.ceil(array))

#print(np.pi)

#radii=np.array([1,2,3])

#print(np.pi*radii**2)

#Elementwise arithmetic operations on numpy arrays

#array1=np.array([1,2,3,4,3])
#array2=np.array([5,6,7,8,3])

#print(array1**array2)

#Comparison operations on numpy arrays


scores=np.array([90,80,70,60,50])

scores[scores < 60] = 0

print(scores < 60)
