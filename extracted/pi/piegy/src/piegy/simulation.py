'''
Main Module of Stochastic Simulation
-------------------------------------------

Contains all the necessary tools to build a model and run models based on Gillespie Algorithm.

Class & Functions:
- model:                creates a stochastic mode. Run the model by ``simulation.run(mod)``
- run:                  runs stochastic simulation on a model.
- demo_model:           returns a demo model.
- UV_expected_val:      calculates the expected population of U, V at steady state, assuming no migration and any stochastic process.
- check_overflow_func:  check whether an overflow might happen in simulation. This is usually done automatically when init-ing a model.
'''

from .tools.find_C import find_C

import numpy as np
import os
import ctypes
from ctypes import c_size_t, c_ubyte, c_uint32, c_int32, c_int64, c_double, c_bool, c_char_p, c_char
import numpy as np
from numpy.ctypeslib import ndpointer


# check whether overflow / too large values might be encountered
# these values are considered as exponents in exp()
EXP_OVERFLOW_BOUND = 709  # where exp(x) almost reaches overflow bound
EXP_TOO_LARGE_BOUND = 30  # where exp(x) reaches ~10e13 and accuracy goes below 10^-3 (10^-3 isn't accurate any more)


# read the C core into LIB
# initialized upon first run
LIB = None
# possible result values returned from C
SIM_SUCCESS = 0
SIM_DATA_EMPTY = 1
SIM_SMALL_MAXTIME = 2
SIM_OVERFLOW = 3
ACCURACY_ERROR = 4


'''
The C core
'''

class model_c(ctypes.Structure):
    '''
    The C-cored model
    '''

    _fields_ = [
        ('N', c_size_t),
        ('M', c_size_t),
        ('maxtime', c_double),
        ('record_itv', c_double),
        ('sim_time', c_size_t),
        ('boundary', c_bool),

        ('I', ctypes.POINTER(c_uint32)),
        ('X', ctypes.POINTER(c_double)),
        ('P', ctypes.POINTER(c_double)),

        ('print_pct', c_int32),
        ('seed', c_int32),

        ('data_empty', c_bool),
        ('max_record', c_size_t),
        ('arr_size', c_size_t),
        ('compress_itv', c_uint32),

        ('U1d', ctypes.POINTER(c_double)),
        ('V1d', ctypes.POINTER(c_double)),
        ('Upi_1d', ctypes.POINTER(c_double)),
        ('Vpi_1d', ctypes.POINTER(c_double)),
    ]
    def get_array(self, name):
        """Return internal data as NumPy array, e.g. .get_array('U')"""
        ptr = getattr(self, name)
        return np.ctypeslib.as_array(ptr, shape=(self.arr_size,))


def read_lib():
    global LIB
    if LIB != None:
        return

    LIB = ctypes.CDLL(find_C(), winmode = 0)
    LIB.mod_init.argtypes = [
        ctypes.POINTER(model_c), c_size_t, c_size_t,
        c_double, c_double, c_size_t, c_bool,
        ndpointer(dtype=np.uint32, flags="C_CONTIGUOUS"),
        ndpointer(dtype=np.float64, flags="C_CONTIGUOUS"),
        ndpointer(dtype=np.float64, flags="C_CONTIGUOUS"),
        c_int32, c_int32
    ]
    LIB.mod_init.restype = c_bool

    LIB.mod_free_py.argtypes = [ctypes.POINTER(model_c)]
    LIB.mod_free_py.restype = None

    LIB.run.argtypes = [ctypes.POINTER(model_c), ctypes.POINTER(c_char), c_size_t]
    LIB.run.restype = c_ubyte  # which is uint8





'''
For access by Python
'''             

class model:
    '''
    Store model data and input parameters.
    Initialize a model object to run models.

    Public Class Functions:

        __init__:
            Create a model object. Also initialize data storage.

        __str__:
            Print model object in a nice way.

        copy:
            Return a deep copy of self. Can choose whether to copy data as well. Default is to copy.

        clear_data:
            clear all data stored, set U, V, Upi, Vpi to zero arrays

        change_maxtime:
            Changes maxtime of self. Update data storage as well.

        set_seed:
            Set a new seed. 

        compress_data:
            compress data by only storing average values
    '''

    def __init__(self, N, M, maxtime, record_itv, sim_time, boundary, I, X, P, print_pct = 25, seed = None, check_overflow = True):

        self.check_valid_input(N, M, maxtime, record_itv, sim_time, boundary, I, X, P, print_pct, seed, check_overflow)
        
        self.N = N                      # int, N x M is spatial dimension
        self.M = M                      # int, can't be 1. If want to make 1D space, use N = 1. And this model doesn't work for 1x1 space (causes NaN)
        self.maxtime = maxtime          # float or int, run model for how long time
        self.record_itv = record_itv    # float, record data every record_itv of time
        self.sim_time = sim_time        # int, run this many of rounds (of single_test)
        self.boundary = boundary        # bool, the N x M space have boundary or not (i.e., zero-flux (True) or periodical (False))
        self.I = np.array(I)            # N x M x 2 np.array, initial population. Two init-popu for every patch (U and V)
        self.X = np.array(X)            # N x M x 4 np.array, matrices. The '4' comes from 2x2 matrix flattened to 1D
        self.P = np.array(P)            # N x M x 6 np.array, 'patch variables', i.e., mu1&2, w1&2, kappa1&2
        if print_pct == None:
            self.print_pct = -1
        else:
            self.print_pct = print_pct      # int, print how much percent is done, need to be non-zero
        if seed == None:
            self.seed = -1                # non-negative int, seed for random number generation
        else:
            self.seed = seed
        self.check_overflow = check_overflow

        if check_overflow:
            check_overflow_func(self)

        # initialize storage bins.
        self.set_data(data_empty = True, max_record = int(maxtime / record_itv), compress_itv = 1, 
                      U = None, V = None, Upi = None, Vpi = None)




    def check_valid_input(self, N, M, maxtime, record_itv, sim_time, boundary, I, X, P, print_pct, seed, check_overflow):
        # check whether the inputs are valid

        if (N < 1) or (M < 1):
            raise ValueError('N < 1 or M < 1')
        if (N == 1) and (M == 1):
            raise ValueError('Model fails for 1x1 space')
        if (M == 1):
            raise ValueError('Please set N = 1 for 1D space.')
        if maxtime <= 0:
            raise ValueError('Please set a positive number for maxtime')
        if record_itv <= 0:
            raise ValueError('Please set a positive number for record_itv')
        if sim_time <= 0:
            raise ValueError('Please set a positive number for sim_time')
        if type(boundary) != bool:
            raise TypeError('boundary not a bool. Please use True for zero-flux (with boundary) or False for periodical (no boundary)')
        
        if (type(I) != list) and (type(I) != np.ndarray):
            raise TypeError('Please set I as a list or np.ndarray')
        if np.array(I).shape != (N, M, 2):
            raise ValueError('Please set I as a N x M x 2 shape list or array. 2 is for init values of U, V at every patch')
        
        if (type(X) != list) and (type(X) != np.ndarray):
            raise TypeError('Please set X as a list or np.ndarray')
        if np.array(X).shape != (N, M, 4):
            raise ValueError('Please set X as a N x M x 4 shape list or array. 4 is for the flattened 2x2 payoff matrix')
        
        if (type(P) != list) and (type(P) != np.ndarray):
            raise TypeError('Please set P as a list or np.ndarray')
        if np.array(P).shape != (N, M, 6):
            raise ValueError('Please set P as a N x M x 6 shape list or array. 6 is for mu1, mu2, w1, w2, kappa1, kappa2')
        
        if not ((print_pct == None) or (isinstance(print_pct, int) and (print_pct >= -1))):
            # if not the two acceptable values: None or some >= -1 int
            raise ValueError('Please use an int > 0 for print_pct or None for not printing progress.')
        
        if not ((seed == None) or (isinstance(seed, int) and (seed >= -1))):
            raise ValueError('Please use a non-negative int as seed, or use None for no seed.')
        
        if not isinstance(check_overflow, bool):
            raise ValueError('Please use a bool for check_overflow')
        

    def check_valid_data(self, data_empty, max_record, compress_itv):
        # check whether a set of data is valid, used when reading a saved model
        if type(data_empty) != bool:
            raise TypeError('data_empty not a bool')
        
        if type(max_record) != int:
            raise TypeError('max_record not an int')
        if max_record < 0:
            raise ValueError('max_record < 0')
        
        if type(compress_itv) != int:
            raise TypeError('compress_itv not an int')
        if compress_itv < 0:
            raise ValueError('compress_itv < 0')
   

    def __str__(self):
        # print this mod in a nice format

        self_str = ''
        self_str += 'N = ' + str(self.N) + '\n'
        self_str += 'M = ' + str(self.M) + '\n'
        self_str += 'maxtime = ' + str(self.maxtime) + '\n'
        self_str += 'record_itv = ' + str(self.record_itv) + '\n'
        self_str += 'sim_time = ' + str(self.sim_time) + '\n'
        self_str += 'boundary = ' + str(self.boundary) + '\n'
        self_str += 'print_pct = ' + str(self.print_pct) + '\n'
        self_str += 'seed = ' + str(self.seed) + '\n'
        self_str += 'check_overflow = ' + str(self.check_overflow) + '\n'
        self_str += 'data_empty = ' + str(self.data_empty) + '\n'
        self_str += 'compress_itv = ' + str(self.compress_itv) + '\n'
        self_str += '\n'

        # check whether I, X, P all same (compare all patches to (0, 0))
        I_same = True
        X_same = True
        P_same = True
        for i in range(self.N):
            for j in range(self.M):
                for k in range(2):
                    if self.I[i][j][k] != self.I[0][0][k]:
                        I_same = False
                for k in range(4):
                    if self.X[i][j][k] != self.X[0][0][k]:
                        X_same = False
                for k in range(6):
                    if self.P[i][j][k] != self.P[0][0][k]:
                        P_same = False
        
        if I_same:
            self_str += 'I all same: ' + str(self.I[0][0]) + '\n'
        else:
            self_str += 'I:\n'
            for i in range(self.N):
                for j in range(self.M):
                    self_str += str(self.I[i][j]) + ' '
                self_str += '\n'
            self_str += '\n'
        
        if X_same:
            self_str += 'X all same: ' + str(self.X[0][0]) + '\n'
        else:
            self_str += 'X:\n'
            for i in range(self.N):
                for j in range(self.M):
                    self_str += str(self.X[i][j]) + ' '
                self_str += '\n'
            self_str += '\n'

        if P_same:
            self_str += 'P all same: ' + str(self.P[0][0]) + '\n'
        else:
            self_str += 'P:\n'
            for i in range(self.N):
                for j in range(self.M):
                    self_str += str(self.P[i][j]) + ' '
                self_str += '\n'

        return self_str
    

    def copy(self, copy_data = True):
        # return deep copy of self
        # copy_data decides whether to copy data as well
        if type(copy_data) != bool:
            raise TypeError('Please give a bool as argument: whether to copy data or not')

        sim2 = model(N = self.N, M = self.M, maxtime = self.maxtime, record_itv = self.record_itv, sim_time = self.sim_time, boundary = self.boundary,
                          I = np.copy(self.I), X = np.copy(self.X), P = np.copy(self.P), 
                          print_pct = self.print_pct, seed = self.seed, check_overflow = self.check_overflow)

        if copy_data:
            # copy data as well
            if self.data_empty:
                print("Warning: model has empty data")
            sim2.set_data(self.data_empty, self.max_record, self.compress_itv, self.U, self.V, self.Upi, self.Vpi)

        return sim2


    def calculate_ave(self):
        # get the average value over sim_time many models
        if self.sim_time != 1:
            for i in range(self.N):
                for j in range(self.M):
                    for t in range(self.max_record):
                        self.U[i][j][t] /= self.sim_time
                        self.V[i][j][t] /= self.sim_time
                        self.Upi[i][j][t] /= self.sim_time
                        self.Vpi[i][j][t] /= self.sim_time


    def change_maxtime(self, maxtime):
        # change maxtime
        if (type(maxtime) != float) and (type(maxtime) != int):
            raise TypeError('Please pass in a float or int as the new maxtime.')
        if maxtime <= 0:
            raise ValueError('Please use a positive maxtime.')
        self.maxtime = maxtime
        self.init_storage()


    def set_seed(self, seed):
        # set seed
        self.seed = seed


    def clear_data(self):
        # clear all data stored, set all to 0
        self.init_storage()


    def set_data(self, data_empty, max_record, compress_itv, U, V, Upi, Vpi):
        # set data to the given data values
        # copies are made
        self.check_valid_data(data_empty, max_record, compress_itv)

        self.data_empty = data_empty
        self.max_record = max_record
        self.compress_itv = compress_itv
        self.U = np.copy(U)
        self.V = np.copy(V)
        self.Upi = np.copy(Upi)
        self.Vpi = np.copy(Vpi)


    def compress_data(self, compress_itv = 5):
        # compress data by only storing average values
        if self.data_empty:
            raise RuntimeError('Model has empty data. Cannot compress')

        if type(compress_itv) != int:
            raise TypeError('Please use an int as compress_itv')
        if compress_itv < 1:
            raise ValueError('Please use record_itv >= 1')
        if compress_itv == 1:
            return
        
        self.compress_itv *= compress_itv  # may be reduced over and over again
        self.max_record = int(self.max_record / compress_itv)  # number of data points after reducing

        U_reduced = np.zeros((self.N, self.M, self.max_record), dtype = np.float64)
        V_reduced = np.zeros((self.N, self.M, self.max_record), dtype = np.float64)
        Upi_reduced = np.zeros((self.N, self.M, self.max_record), dtype = np.float64)
        Vpi_reduced = np.zeros((self.N, self.M, self.max_record), dtype = np.float64)

        for i in range(self.N):
            for j in range(self.M):
                for k in range(self.max_record):
                    lower = k * compress_itv  # upper and lower bound of current record_itv
                    upper = lower + compress_itv
                    U_reduced[i][j][k] = np.mean(self.U[i, j, lower : upper])
                    V_reduced[i][j][k] = np.mean(self.V[i, j, lower : upper])
                    Upi_reduced[i][j][k] = np.mean(self.Upi[i, j, lower : upper])
                    Vpi_reduced[i][j][k] = np.mean(self.Vpi[i, j, lower : upper])
        
        self.U = U_reduced
        self.V = V_reduced
        self.Upi = Upi_reduced
        self.Vpi = Vpi_reduced



def run(mod, message = ""):
    '''
    C-cored simulation
    '''

    read_lib()

    if not mod.data_empty:
        raise ValueError('mod has non-empty data.')

    msg_len = len(message) * 2
    msg_bytes = message.encode('utf-8')
    msg_buffer = ctypes.create_string_buffer(msg_bytes, msg_len) 
    
    I = np.ascontiguousarray(mod.I.flatten(), dtype = np.uint32)
    X = np.ascontiguousarray(mod.X.flatten(), dtype = np.float64)
    P = np.ascontiguousarray(mod.P.flatten(), dtype = np.float64)

    mod_c = model_c()
    init_sucess = LIB.mod_init(ctypes.byref(mod_c), 
                           mod.N, mod.M, mod.maxtime, mod.record_itv, mod.sim_time, mod.boundary,
                           I, X, P, mod.print_pct, mod.seed)
    if not init_sucess:
        LIB.mod_free_py(ctypes.byref(mod_c))
        del mod_c
        raise RuntimeError('Model initialization failed')
    
    result = LIB.run(ctypes.byref(mod_c), msg_buffer, msg_len)

    if result == SIM_SUCCESS:
        mod.set_data(False, mod.max_record, 1, mod_c.get_array('U1d').reshape(mod.N, mod.M, mod.max_record), 
                    mod_c.get_array('V1d').reshape(mod.N, mod.M, mod.max_record), 
                    mod_c.get_array('Upi_1d').reshape(mod.N, mod.M, mod.max_record), 
                    mod_c.get_array('Vpi_1d').reshape(mod.N, mod.M, mod.max_record))
        LIB.mod_free_py(ctypes.byref(mod_c))
        del mod_c
    elif result == SIM_SMALL_MAXTIME:
        LIB.mod_free_py(ctypes.byref(mod_c))
        del mod_c
        raise RuntimeError('maxtime too small.')
    elif result == SIM_OVERFLOW:
        LIB.mod_free_py(ctypes.byref(mod_c))
        del mod_c
        raise OverflowError('Overflow in simulation. Possibly due to too large w1, w2, or payoff.')
    elif result == ACCURACY_ERROR:
        LIB.mod_free_py(ctypes.byref(mod_c))
        del mod_c
        raise RuntimeError('Accuracy dropped catastrophically during simulation. Possibly due to too large w1, w2, or payoff.')
    else:
        LIB.mod_free_py(ctypes.byref(mod_c))
        del mod_c
        raise RuntimeError('Unclassified error.')




def demo_model():
    '''
    Returns a demo model.model object
    '''

    N = 10                  # Number of rows
    M = 10                  # Number of cols
    maxtime = 30           # how long you want the model to run
    record_itv = 0.1        # how often to record data.
    sim_time = 1            # repeat model to reduce randomness
    boundary = True         # boundary condition.

    # initial population for the N x M patches. 
    I = [[[44, 22] for _ in range(M)] for _ in range(N)]
    
    # flattened payoff matrices, total resource is 0.4, cost of fighting is 0.1
    X = [[[-1, 4, 0, 2] for _ in range(M)] for _ in range(N)]
    
    # patch variables
    P = [[[0.5, 0.5, 1, 1, 0.001, 0.001] for _ in range(M)] for _ in range(N)]

    print_pct = 25           # print progress
    seed = 36               # seed for random number generation

    # create a model object
    mod = model(N, M, maxtime, record_itv, sim_time, boundary, I, X, P, 
                            print_pct = print_pct, seed = seed)
    
    return mod



def UV_expected_val(mod):
    '''
    Calculate expected U & V population and payoff based on matrices, assume no migration and any stochastic process.
    To differentiate from UV_expected in figures.py: this one return arrays (values).
    '''
    
    U_expected = np.zeros((mod.N, mod.M))  # expected U population
    V_expected = np.zeros((mod.N, mod.M))  # expected V population
    pi_expected = np.zeros((mod.N, mod.M)) # expected payoff, which are equal for U and V
    
    for i in range(mod.N):
        for j in range(mod.M):
            # say matrix = [a, b, c, d]
            # U_proportion = (d - b) / (a - b - c + d)
            U_prop = (mod.X[i][j][3] - mod.X[i][j][1]) / (mod.X[i][j][0] - mod.X[i][j][1] - mod.X[i][j][2] + mod.X[i][j][3])
            # equilibrium payoff, U_payoff = V_payoff
            eq_payoff = U_prop * mod.X[i][j][0] + (1 - U_prop) * mod.X[i][j][1]
            
            # payoff / kappa * proportion
            U_expected[i][j] = eq_payoff / mod.P[i][j][4] * U_prop
            V_expected[i][j] = eq_payoff / mod.P[i][j][5] * (1 - U_prop)
            pi_expected[i][j] = eq_payoff
                
    return U_expected, V_expected, pi_expected



def check_overflow_func(mod):
    _, _, pi_expected = UV_expected_val(mod)
    for i in range(mod.N):
        for j in range(mod.M):
            w1_pi = pi_expected[i][j] * mod.P[i][j][2]  # w1 * U_pi
            w2_pi = pi_expected[i][j] * mod.P[i][j][3]  # w2 * V_pi
            if ((w1_pi > EXP_OVERFLOW_BOUND) or (w2_pi > EXP_OVERFLOW_BOUND)):
                print("Warning: might cause overflow in simulation. w1, w2, or payoff matrix values too large")
                return
            if ((w1_pi > EXP_TOO_LARGE_BOUND) or (w2_pi > EXP_TOO_LARGE_BOUND)):
                print("Warning: might have low accuracy in simulation. w1, w2, or payoff matrix values too large")
                return

