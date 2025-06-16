from typing import List
from pyloco import Task

class Greetings(Task):

    def __init__(self, parent):

        self.add_data_argument("data", type=str, nargs="+", required=True,
                               help="input data to print")

        self.register_forward("data", type=List[str], help="printed texts")

    def perform(self, targs):
        
        output = []

        for data in targs.data:
            outtext = "Hello %s Bye~" % data
            output.append(outtext)
            print(outtext)

        self.add_forward(data=output)
