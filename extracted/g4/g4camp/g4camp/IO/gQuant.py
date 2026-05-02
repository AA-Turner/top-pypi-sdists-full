import numpy as np

class gQuant():
    
    def __init__(self, label: str, dtype: np.dtype):
        
        self._label = label
        self._dtype = dtype
        
        self.__capacity = 100_000
        self.__size     = 0
        
        self._value = np.empty(shape=self.__capacity, dtype=self._dtype)
    
    @property
    def label(self) -> str:
        return self._label
    
    @property
    def dtype(self) -> type:
        return self._dtype
    
    @property
    def value(self) -> dtype:
        if self._value is None:
            raise ValueError('Value has not been initialized!')
        if np.size(self._value) != self.__size:
            self._value = self._value[:self.__size]
        return self._value
    
    @value.setter
    def value(self, new_value: dtype) -> None:
        if self.__size == self.__capacity:
            self.__capacity *= 2
            data_reshape = np.empty(shape=self.__capacity, dtype=self._dtype)
            data_reshape[:self.__size] = self._value
            self._value = data_reshape
        
        self._value[self.__size] = new_value
        
        self.__size += 1
    
    def has_value(self) -> bool:
        return self.__size > 0