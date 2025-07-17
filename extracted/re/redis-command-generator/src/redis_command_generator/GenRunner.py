import threading
import copy
import sys
from simple_parsing import parse
from dataclasses import dataclass
from time import sleep
from multiprocessing import cpu_count
from redis_command_generator.BaseGen import KeyedLimitedRandomQueue
from redis_command_generator.AllGen import *

def create_tg(base_classes):
    return type('TypeGen', base_classes, {})

def cast_to_tg(obj_with_args, class_type):
    class_obj = copy.deepcopy(obj_with_args)
    class_obj.__class__ = class_type
    return class_obj

def strings_to_classes(classnames):
    classes = []
    for name in classnames:
        classes.append(getattr(sys.modules[__name__], name))
    
    return classes

# Append thread number to logfile name
def rename_log(logfile, thread_num):
    if logfile is None:
        return None
    
    logfile = logfile.split(".")
    return f"{logfile[0]}_t{thread_num}.{logfile[1]}"

# You may also run `python -m redis_command_generator.GenRunner -h` to see all available args
@dataclass
class GenRunner(AllGen):
    num_threads: int = cpu_count() - 1  # Number of threads to run, default is number of CPU cores - 1
    include_gens: tuple = ("SetGen", "ZSetGen", "StringGen", "StreamGen", "ListGen", "HyperLogLogGen", "HashGen", "GeoGen", "BitmapGen", "TimeSeriesGen", "BloomGen", "CuckooGen", "CmsGen", "TopKGen", "TDigestGen", "JsonGen")
    exclude_gens: tuple = ()
    
    def __post_init__(self):
        self.threads = []
        self.events = []
        self.logfiles = []
    
    def __enter__(self):
        self.start()
        return self
    
    def start(self, args=None):
        if args is None:
            args = copy.deepcopy(self)
        
        gen_names = [gen for gen in args.include_gens if gen not in args.exclude_gens]
        gen_types = strings_to_classes(gen_names)
        TypeGen = create_tg(tuple(gen_types))  # Create a new class from all the selected generators
        keyed_limited_random_queue = KeyedLimitedRandomQueue(max_size_per_key=100)

        
        for i in range(args.num_threads):
            # Can't simply use i as more threads may be added by running start multiple times
            t_num = len(self.threads)
            
            generator = cast_to_tg(args, TypeGen)
            
            generator.logfile = rename_log(args.logfile, t_num)
            self.logfiles.append(generator.logfile)
            
            self.events.append(threading.Event())
            self.threads.append(threading.Thread(target=(generator._run), args=(self.events[t_num],keyed_limited_random_queue)))
            self.threads[t_num].start() 

    def join(self):
        for t in self.threads:
            t.join()
        return self.logfiles

    def __exit__(self, exc_type, exc_value, traceback):
        for e in self.events:
            e.set()
        return self.join()

if __name__ == "__main__":
    args = parse(GenRunner)

    # # For your convienience, a list of all available params is shown below
    runner = GenRunner(verbose=args.verbose,
                       hosts=args.hosts,
                       flush=args.flush,
                       max_cmd_cnt=args.max_cmd_cnt,
                       mem_cap=args.mem_cap,
                       pipe_every_x=args.pipe_every_x,
                       def_key_size=args.def_key_size,
                       def_key_pref=args.def_key_pref,
                       distributions=args.distributions,
                       expire_precentage=args.expire_precentage,
                       logfile=args.logfile,
                       maxmemory_bytes=args.maxmemory_bytes,
                       print_prefix=args.print_prefix,
                       ttl_low=args.ttl_low,
                       ttl_high=args.ttl_high,
                       max_subelements=args.max_subelements,
                       subval_size=args.subval_size,
                       subkey_size=args.subkey_size,
                       incrby_min=args.incrby_min,
                       incrby_max=args.incrby_max,
                       num_threads=args.num_threads,
                       include_gens=args.include_gens,
                       identical_values_across_hosts=args.identical_values_across_hosts,
                       exclude_gens=args.exclude_gens)

    runner.start()
    runner.join()