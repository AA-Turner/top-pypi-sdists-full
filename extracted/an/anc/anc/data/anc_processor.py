from abc import ABC, abstractmethod


class Processor(ABC):
    r'''
    function to handle a single data
    return None if no data needs to return. Otherwise, return a list of transformed data
    It is useful when certain filtering logic is needed
    '''
    @abstractmethod
    def transform(self, item, is_last_sample=False):
        pass

    r'''
    function to handle a batch of data
    input:
        list_of_items -- data to be batch processed
        is_last_batch -- whether current batch is the last batch might be useful if the last batch's 
                         tranform logic is different from the normal batches.
    return:
        the transformed batch data. None if no data needs to return, otherwise, it should be a list of batch data
        since buffer gathering logic might exist, and it is possible to return multiple of batch data.
    '''
    @abstractmethod
    def batch_transform(self, list_of_items, is_last_batch=False):
        pass


class AncProcessor(Processor):
    r'''
    A processor that does nothing but return the input as is for both transform and batch transform function
    '''
    def transform(self, item, is_last_sample=False):
        return [item]

    # we wrap out data to a list to follow the return pattern in the base class
    def batch_transform(self, list_of_items, is_last_batch=False):
        return [list_of_items]
