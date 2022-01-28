import numpy as np


def chunk(lst, n: int):
    splitted = np.array_split(lst, n)
    return [v for v in splitted if (len(v) > 0)]
