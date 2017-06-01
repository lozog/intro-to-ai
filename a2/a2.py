import numpy as np

# with help from Briuaku's answer:
# https://stackoverflow.com/questions/24432209/python-index-an-array-using-the-colon-operator-in-an-arbitrary-dimension
def restrict(factor, variable, value):
    if factor.shape[variable] == 1:
        # restrict on a variable not used in the factor
        reshape_index = [2] * (factor.ndim-1)
        return factor.reshape(reshape_index)
    else:
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
    for elem in np.nditer(factor, op_flags=['readwrite']):
        elem /= totalSum
    return factor

def _multiplyList(factorList):
    if len(factorList) == 1:
        return factorList[0]
    elif len(factorList) == 2:
        return multiply(factorList[0], factorList[1])
    else:
        return multiply(factorList[0], factorList[1:])

def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
    for factor in factorList:
        for idx,evidence in evidenceList:
            factor = restrict(factor, idx, evidence)
        # for
    # for

    for var in orderedListOfHiddenVariables:
        # multiply all factors that have var in them
        factorsToMultiply = []
        for factor in factorList:
            if factor.shape[var] > 1:
                factorsToMultiply.append(factor)
        # for

        factorList = [f for f in factorList if f not in factorsToMultiply]
        product = _multiplyList(factorsToMultiply)
        summed = sumout(product, var)
        factorList.append(summed)
    # for

    product = _multiplyList(factorList)
    return normalize(product)

####### Tests for restrict

# factor = np.arange(4).reshape(1,2,2)
# factor = factor + 4
# print(factor)
# print('')
# factor = restrict(factor, 0, 1)

# print(factor)
# print('')
# factor = restrict(factor, 1, 1)
# print(factor)

####### Tests for multiply

# factor1 = np.arange(4).reshape(2,2,1)
# factor2 = factor1 + 4
# factor2 = factor2.reshape(1,2,2)
# print(factor1)
# print(factor2)
# print(multiply(factor1, factor2))

# f1 = np.array([0.9, 0.1])
# f2 = np.array([0.91, 0.14])
# f3 = multiply(f1, f2)
# print(f3)
# f4 = normalize(f3)
# print(f4)

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
