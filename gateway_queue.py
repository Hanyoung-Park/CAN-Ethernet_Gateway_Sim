from can import CAN_Nodes

class Gateway:
    def __init__(self, n_ids):
        self.n_ids = n_ids
        self.queue_data = 0
        self.q = []
        self.toc = []
        self.latency_array = []

    def enqueue(self, CAN_Nodes, t):
        self.queue_data += CAN_Nodes.datasize
        self.q.append(CAN_Nodes)
        self.toc.append(t)

    def dequeue(self, t):
        self.queue_data -= self.n_ids * 64
        for _ in range(self.n_ids):
            del self.q[0]
        for i in range(len(self.toc)):
            self.latency_array.append(t - self.toc[i])
        return self.latency_array
        
    def updateGateway(self, t):
        if self.queue_data >= self.n_ids * 64:
            result = self.dequeue(t)
            self.toc = []
            self.latency_array = []
            return result
        return None

