import numpy as np


def chunk(lst, n: int):
    splitted = np.array_split(lst, n)
    return [v.tolist() for v in splitted if (len(v) > 0)]
