import numpy as np

def calculate(list):
    if len(list) != 9:
        raise ValueError("List must contain nine numbers.")
    matrix = np.reshape(list, [3,3])
    list1 = np.array(list)
    calculations = {
        'mean': [matrix.mean(axis=0).tolist(), matrix.mean(axis=1).tolist(), list1.mean()],
        'variance': [matrix.var(axis=0).tolist(), matrix.var(axis=1).tolist(), list1.var()],
        'standard deviation': [matrix.std(axis=0).tolist(), matrix.std(axis=1).tolist(), list1.std()],
        'max': [matrix.max(axis=0).tolist(), matrix.max(axis=1).tolist(), list1.max()],
        'min': [matrix.min(axis=0).tolist(), matrix.min(axis=1).tolist(), list1.min()],
        'sum': [matrix.sum(axis=0).tolist(), matrix.sum(axis=1).tolist(), list1.sum()]
    }
    return calculations