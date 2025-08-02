'''
Stores and reads a model object.

Functions:
- save:    save a model object.
- load:    load a model object.
'''


from . import simulation

import json
import gzip
import os
import numpy as np


def save(mod, dirs = '', print_msg = True):
    '''
    Saves a model object. Data will be stored at dirs/data.json.gz

    Inputs:
    - mod:        Your model object.
    - dirs:       Where to save it.
    - print_msg:  Whether to print message after saving.
    '''

    try:
        _ = mod.N
    except AttributeError:
        raise ValueError('mod is not a model object')

    if not os.path.exists(dirs):
        os.makedirs(dirs)
        
    data = []
    
    inputs = []
    inputs.append(mod.N)
    inputs.append(mod.M)
    inputs.append(mod.maxtime)
    inputs.append(mod.record_itv)
    inputs.append(mod.sim_time)
    inputs.append(mod.boundary)
    inputs.append(mod.I.tolist())
    inputs.append(mod.X.tolist())
    inputs.append(mod.P.tolist())
    inputs.append(mod.print_pct)
    inputs.append(mod.seed)
    data.append(inputs)

    # skipped rng
    
    outputs = []
    outputs.append(mod.max_record)
    outputs.append(mod.compress_itv)
    if not mod.data_empty:
        outputs.append(mod.U.tolist())
        outputs.append(mod.V.tolist())
        outputs.append(mod.Upi.tolist())
        outputs.append(mod.Vpi.tolist())
    else:
        outputs.append(None)
        outputs.append(None)
        outputs.append(None)
        outputs.append(None)

    data.append(outputs)

    data_dirs = os.path.join(dirs, 'data.json.gz')
    with gzip.open(data_dirs, 'wb') as f:
        f.write(json.dumps(data).encode('utf-8'))

    if print_msg:
        print('data saved: ' + data_dirs)



def load(dirs):
    '''
    Reads and returns a model object.

    Inputs:
    - dirs:       where to read from, just provide the folder-subfolder names. Don't include 'data.json.gz'
    - print_msg:  this function prints a message when the mod.compress_itv != None. Setting print_msg = False will skip ignore this message.

    Returns:
    - mod: a piegy.model.model object read from the data.
    '''
    
    if not os.path.exists(dirs):
        raise FileNotFoundError('dirs not found: ' + dirs)
    
    data_dirs = os.path.join(dirs, 'data.json.gz')
    if not os.path.isfile(data_dirs):
        raise FileNotFoundError('data not found in ' + dirs)
    
    with gzip.open(data_dirs, 'rb') as f:
        data = json.loads(f.read().decode('utf-8'))

        # inputs
        try:
            mod = simulation.model(N = data[0][0], M = data[0][1], maxtime = data[0][2], record_itv = data[0][3],
                                sim_time = data[0][4], boundary = data[0][5], I = data[0][6], X = data[0][7], P = data[0][8], 
                                print_pct = data[0][9], seed = data[0][10], check_overflow = False)
        except:
            raise ValueError('Invalid input parameters stored in data')

        # outputs
        try:
            mod.set_data(data_empty = False, max_record = data[1][0], compress_itv = data[1][1], 
                        U = data[1][2], V = data[1][3], Upi = data[1][4], Vpi = data[1][5])
            if (mod.U is None) or (isinstance(mod.U, np.ndarray) and mod.U.shape == () and mod.U.item() is None):
                # if data is None
                mod.data_empty = True
        except:
            raise ValueError('Invalid simulation results stored in data')
    
    return mod





