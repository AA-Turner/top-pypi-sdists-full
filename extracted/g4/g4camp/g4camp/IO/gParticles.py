import numpy as np

from geant4_pybind import G4ThreeVector

from g4camp.IO.gQuant import gQuant

class gParticles():
    
    def __init__(self, label: str = ''):
        
        self._label   = label
        self._counter = 0
    
        self.uid           = gQuant('uid',int)
        self.parent_uid    = gQuant('parent_uid',int)
        self.pdgid         = gQuant('pdgid',int)
        self.x_m           = gQuant('x_m',float)
        self.y_m           = gQuant('y_m',float)
        self.z_m           = gQuant('z_m',float)
        self.t_ns          = gQuant('t_ns',float)
        self.dir_x         = gQuant('dir_x',float)
        self.dir_y         = gQuant('dir_y',float)
        self.dir_z         = gQuant('dir_z',float)
        self.Etot_GeV      = gQuant('Etot_GeV',float)
        self.process_name  = gQuant('process_name','|S10')
        
        self.quantities = (self.uid,self.parent_uid,self.pdgid,
                    self.x_m,self.y_m,self.z_m,self.t_ns,
                    self.dir_x,self.dir_y,self.dir_z,self.Etot_GeV,
                    self.process_name)
    
    @property
    def label(self):
        return self._label
    
    @property
    def counter(self):
        return self._counter
    
    @counter.setter
    def counter(self, new_count):
        self._counter = new_count
    
    @property
    def pos_m(self):
        return np.column_stack((self.x_m,
                                self.y_m,
                                self.z_m))
    
    @property
    def dir(self):
        return np.column_stack((self.dir_x,
                                self.dir_y,
                                self.dir_z))
    
    @property
    def unique_data(self):
        return len(set(self.uid.value))
    
    def set_data(self, new_uid: int, new_parent_uid: int, new_pdgid: int, \
                 new_pos_m: G4ThreeVector, new_t_ns: float,
                 new_dir: G4ThreeVector, new_Etot_GeV: float, \
                 new_process_name: bytes = None) -> None:
        
        self.uid.value           = new_uid
        self.parent_uid.value    = new_parent_uid
        self.pdgid.value         = new_pdgid
        
        self.x_m.value           = new_pos_m.x
        self.y_m.value           = new_pos_m.y
        self.z_m.value           = new_pos_m.z
        self.t_ns.value          = new_t_ns
        
        self.dir_x.value         = new_dir.x
        self.dir_y.value         = new_dir.y
        self.dir_z.value         = new_dir.z
        self.Etot_GeV.value      = new_Etot_GeV
        
        if new_process_name:
            self.process_name.value = new_process_name
        
        self.counter += 1
    
    def get_named_data(self) -> np.ndarray:
        
        quantities = tuple(q for q in self.quantities if q.has_value())
        if not quantities:
            return np.empty(shape=(0),dtype=None)
        data_type  = list((q.label,q.dtype) for q in quantities)
        data_list  = np.column_stack([q.value for q in quantities])
        named_data = np.array([tuple(_) for _ in data_list], dtype=data_type)
        named_data = named_data[np.lexsort((named_data['t_ns'], named_data['uid']))]
        
        return named_data