from itertools import product
import numpy as np


def _obj2str(a, none_char='-'):
    """ Casts object a to str. """
    if isinstance(a, float):
        # if the float is 2.49999999 then round
        if str(a)[::-1].find('.') > 5:
            return '{:.5f}'.format(a)
    elif a is None:
        return none_char
    return str(a)


_array2str = np.vectorize(_obj2str)


def print_table(matrix: np.ndarray,
                include_sum: bool = False) -> None:
    """ Prints matrix data in a nice table format.

    The matrix element matrix[i][j] should correspond to information about
    order j+2 and n-body i+1.

    Example
    --------
    >> matrix = numpy.array([[None, None], [4.0, 3.0]])
    >> print_table(matrix)

     body/order |  2  |  3
    ------------------------
         1      |  -  |  -
         2      | 4.0 | 3.0

    Parameters
    ----------
    matrix
        matrix to be printed
    include_sum
        whether or not to print the sum along each row and column
    """
    table_str = table_array_to_string(matrix, include_sum)
    print(table_str)


def table_array_to_string(matrix: np.ndarray,
                          include_sum: bool = False) -> str:
    """Generate nice table string from a numpy array with floats/ints.

    Parameters
    ----------
    matrix
        matrix to be printed
    include_sum
        whether or not to print the sum along each row and column
    """
    table_array = _generate_table_array(matrix, include_sum)
    table_array_str = _array2str(table_array)
    table_str = _generate_table_str(table_array_str)
    return table_str


def _generate_table_array(table_array: np.ndarray,
                          include_sum: bool = False):
    """Generate table in numpy array format.

    Parameters
    ----------
    table_array
        matrix to be printed
    include_sum
        whether or not to print the sum along each row and column
    """

    # initialze table
    n_rows, n_cols = table_array.shape
    A = _build_table_frame(order=n_cols+1, nbody=n_rows, include_sum=include_sum)

    # fill table
    for order, nbody in product(range(2, n_cols+2), range(1, n_rows+1)):
        if nbody <= order:
            A[nbody, order-1] = table_array[nbody-1, order-2]

    if include_sum:
        for i, row in enumerate(A[1:-1, 1:-1], start=1):
            A[i, -1] = sum(val for val in row if val is not None)
        for i, col in enumerate(A[1:-1, 1:-1].T, start=1):
            A[-1, i] = sum(val for val in col if val is not None)
        A[-1, -1] = ''

    return A


def _generate_table_str(table_array: np.ndarray) -> str:
    """Generate a string from a numpy array of strings.

    Parameters
    ----------
    table_array
        matrix to be printed
    """
    table_str = []
    n_rows, n_cols = table_array.shape

    # find maximum widths for each column
    widths = []
    for i in range(n_cols):
        widths.append(max(len(val) for val in table_array[:, i])+2)

    # formatting str for each row
    row_format = '|'.join('{:^'+str(width)+'}' for width in widths)

    # finalize
    for i in range(n_rows):
        if i == 1:
            table_str.append('-' * (sum(widths)+n_cols-1))
        table_str.append(row_format.format(*table_array[i, :]))
    table_str = '\n'.join(table_str)
    return table_str


def _build_table_frame(order: int,
                       nbody: int,
                       include_sum: bool = False):
    """ Builds/initializes table/array. """
    if include_sum:
        A = np.empty((nbody+2, order+1), dtype='object')
        A[0, -1] = 'sum'
        A[-1, 0] = 'sum'
    else:
        A = np.empty((nbody+1, order), dtype='object')

    A[0][0] = 'body/order'
    A[0, 1:order] = range(2, order+1)
    A[1:nbody+1, 0] = range(1, nbody+1)
    return A


if __name__ == '__main__':
    # input dummy cutoff table
    # insert row for nbody=1
    cutoffs = np.array([[None, None, None, None, None],
                        [6.0, 6.0, 6.0, 3.7, 3.7],
                        [5.0, 5.0, 5.0, 3.0, 3.0],
                        [3.7, 3.7, 3.7, 0.0, 0.0]])

    # input dummy cluster count table
    cluster_counts = np.array([[1, 3, 5, 5, 2],
                               [12, 22, 39, 42, 58],
                               [19, 41, 123, 421, 912],
                               [42, 112, 410, 617, 3271]])

    print_table(cutoffs)
    print('\n')
    print_table(cluster_counts, include_sum=False)
    print('\n')
    print_table(cluster_counts, include_sum=True)
