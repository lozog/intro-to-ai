import numpy as np

# with help from Briuaku's answer:
# https://stackoverflow.com/questions/24432209/python-index-an-array-using-the-colon-operator-in-an-arbitrary-dimension
def restrict(factor, variable, value):
    # take the (value)-th value of the (variable)-th dimension
    slice_index = [slice(None)] * factor.ndim
    slice_index[variable] = value
    return factor[ tuple(slice_index) ]

def multiply(factor1, factor2):
    print("TODO: implement")

def sumout(factor, variable):
    totalSum = factor.sum()


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

####### Tests for normalize

factor = np.arange(8, dtype=np.float64).reshape(2,2,2)
print(factor)
print(normalize(factor))
