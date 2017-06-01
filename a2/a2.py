import numpy as np

# with help from Briuaku's answer:
# https://stackoverflow.com/questions/24432209/python-index-an-array-using-the-colon-operator-in-an-arbitrary-dimension
def restrict(factor, variable, value):
    # take the (value)-th value of the (variable)-th dimension
    slice_index = [slice(None)] * factor.ndim
    slice_index[variable] = value
    return factor[ tuple(slice_index) ]

def multiply(factor1, factor2):
    # f = factor1.reshape(2,2,1)
    # g = factor2.reshape(1,2,2)
    return factor1 * factor2

def sumout(factor, variable):
    return factor.sum(variable)

def normalize(factor):
    totalSum = factor.sum()
    for row in factor:
        for elem in row:
            elem /= totalSum
    return factor

def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
    print("TODO: implement")

####### Tests for restrict

# factor = np.arange(8).reshape(2,2,2)
# print(factor)
# print(restrict(factor, 1, 0))

####### Tests for multiply

# factor1 = np.arange(4).reshape(2,2,1)
# factor2 = factor1 + 4
# factor2 = factor2.reshape(1,2,2)
# print(factor1)
# print(factor2)
# print(multiply(factor1, factor2))

####### Tests for sumout

# print('sumout')
# factor = np.arange(8).reshape(2,2,2)
# # factor = np.array([[0.6, 0.4], [0.1, 0.9]])

# print(factor)
# print(sumout(factor, 0))

# ####### Tests for normalize
#
# factor = np.arange(8, dtype=np.float64).reshape(2,2,2)
# print(factor)
# print(normalize(factor))
