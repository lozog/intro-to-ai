import numpy as np

# with help from Briuaku's answer:
# https://stackoverflow.com/questions/24432209/python-index-an-array-using-the-colon-operator-in-an-arbitrary-dimension
def restrict(factor, variable, value):
    # take the (value)-th value of the (variable)-th dimension
    slice_index = [slice(None)] * factor.ndim
    slice_index[variable] = value

    shape = [x for x in factor.shape]
    shape[variable] = 1

    return factor[ tuple(slice_index) ].reshape(shape)

def multiply(factor1, factor2):
    return factor1 * factor2

def sumout(factor, variable):
    shape = [x for x in factor.shape]
    summed = factor.sum(variable)
    shape[variable] = 1
    return summed.reshape(shape)

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

def _inArray(factorList, factor):
    for i,f in enumerate(factorList):
        if (f == factor).all():
            return True
    # for
    return False

def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
    # call restrict on all factors that contain any of the variables in the evidence
    for idx,evidence in enumerate(evidenceList):
        if evidence == -1:
            continue
        # find factors that are influenced by evidence
        factorsUsingEvidence = []
        for idx2,factor in enumerate(factorList):
            shape = factor.shape
            if shape[idx] > 1:
                factorList[idx2] = restrict(factor, idx, evidence)
        # for
    # for

    # for each hidden variable, create a new factor by multiplying factors that contain hidden variable
    for var in orderedListOfHiddenVariables:
        factorsToMultiply = []
        for factor in factorList:
            if factor.shape[var] > 1:
                factorsToMultiply.append(factor)

        factorList = [f for f in factorList if not _inArray(factorsToMultiply, f)]

        product = _multiplyList(factorsToMultiply)

        # sum out the hidden variable
        summed = sumout(product, var)
        factorList.append(summed)
    # for

    # multiply remaining factors
    product = _multiplyList(factorList)

    # normalize and return
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

####### Tests for normalize

# factor = np.arange(8, dtype=np.float64).reshape(2,2,2)
# print(factor)
# print(normalize(factor))

####### Tests for inference

f1 = np.array([0.1, 0.9]).reshape(2,1,1)
f2 = np.array([[0.6, 0.4], [0.1, 0.9]]).reshape(2,2,1)
f3 = np.array([[0.8, 0.2], [0.3, 0.7]]).reshape(1,2,2)
#
# f4 = restrict(f3, 2, 1)
# # print(f4.shape)
# # print(f4)
# _f4 = multiply(f2, f4)
#
# f5 = sumout(_f4, 1)
# print(f5)
# print(f5.shape)
#
# f6 = multiply(f1, f5)
# print(f6)
# print(normalize(f6))
# print(normalize(f6).shape)

result = inference([f1,f2,f3], [0], [1], [-1,-1,1])
print("result:")
print(result)

# y1 = np.array([[1, 2], [1, 3], [1, 2], [2, 2]])
# y2 = np.array([[100, 200], [100,300], [100, 200], [200, 200]])
# z = np.array([1, 2])
# print((y1 == z).all(1).any())
# print((y2 == z).all(1).any())
