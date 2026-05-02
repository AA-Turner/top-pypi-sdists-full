class query_data:
    # def __init__(self, subGraph, edgeTypes, nodeTypes, edgeConditions, nodeConditions):
    #     self.subGraph = subGraph
    #     self.edgeTypes = edgeTypes
    #     self.nodeTypes = nodeTypes
    #     self.edgeConditions = edgeConditions
    #     self.nodeConditions = nodeConditions

    def __init__(self):
        self.subGraph = "subGraph"
        self.edgeTypes = "edgeTypes"

    def keys(self):
        # return 'subGraph', 'edgeTypes', 'nodeTypes', 'edgeConditions', 'nodeConditions'
        return 'subGraph', 'edgeTypes'

    def __getitem__(self, item):
        #return getattr(self, item)
        return "test"
import datetime
start = datetime.datetime.now()
import time
time.sleep(3)
end = datetime.datetime.now()
#print((end -start).seconds)

# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def get_pack_time():
    with open("./../env/pack_time.txt") as f:
        for line in f.readlines():
            print(line.strip())

pass
get_pack_time()