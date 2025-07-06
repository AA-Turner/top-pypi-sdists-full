import GPUtil
import psutil

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            gpus = GPUtil.getGPUs()
            if not gpus:
                self.process = 'cpu'
                self.bestGPU = None
            else:
                self.process = 'gpu'
                self.bestGPU = self.select_best_gpu()
                self.numGPUs = len(gpus)
                self.numCPUs = psutil.cpu_count(logical=False)
            self.availableMemory = 100-self.get_memory_usage()
            self.batchSize = self.calculate_batch_size()
            self.initialized = True

    def set_process(self, process):
        if process not in ['cpu', 'gpu']:
            raise ValueError("process must be 'cpu' or 'gpu'")
        self.process = process

    def get_process(self):
        return self.process
    
    def select_best_gpu(self):
        gpus = GPUtil.getGPUs()

        best_gpu = 0
        max_memory = 0

        for i, gpu in enumerate(gpus):
            # Obtenez la mémoire totale et utilisée pour chaque GPU
            total_memory = gpu.memoryTotal
            used_memory = gpu.memoryUsed
            available_memory = total_memory - used_memory

            # Sélectionnez le GPU avec le plus de mémoire disponible
            if available_memory > max_memory:
                max_memory = available_memory
                best_gpu = i
        return best_gpu
    

    def get_memory_usage(self):
        """Returns the current memory usage in percentage."""
        return psutil.virtual_memory().percent

    def calculate_batch_size(self,max_memory_usage=90, min_batch_size=1, max_batch_size=20):
        """Calculate dynamic batch size based on available memory."""

        # Adjust batch size based on available memory
        if self.availableMemory > max_memory_usage:
            return max_batch_size
        else:
            # Scale batch size linearly with available memory
            return max(min_batch_size, int((self.availableMemory / max_memory_usage) * max_batch_size))

config = Config()