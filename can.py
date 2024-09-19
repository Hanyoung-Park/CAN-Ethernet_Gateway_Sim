class CAN_Nodes:
    def __init__(self, period, datasize, startpoint):
        self.period = period
        self.datasize = datasize # bit
        self.startpoint = startpoint

class CAN_Link:
    def __init__(self, datarate):
        self.datarate = datarate # kbps
        self.idle = True
        self.q = []
        self.holdingTime = 0 # microseconds
        self.headersize = 11 + 4
        self.txnode = None

    def checkIdle(self):
        if self.holdingTime <= 0:
            self.idle = True
        else:
            self.idle = False        
        return self.idle

    def enqueue(self, CAN_Nodes):
        self.q.append(CAN_Nodes)

    def dequeue(self):
        del self.q[0]

    def transmit(self, CAN_Nodes):
        Ltransmission = (CAN_Nodes.datasize + self.headersize) / self.datarate
        self.holdingTime = Ltransmission * 1e6
        self.txnode = CAN_Nodes

    def updateLink(self, gateway, t):
        if self.holdingTime > 1:
            self.holdingTime -= 1
        elif self.holdingTime > 0:
            self.holdingTime = 0
            gateway.enqueue(self.txnode, t)
        else:
            self.holdingTime = 0
        if self.checkIdle() and len(self.q) != 0:
            self.transmit(self.q[0])
            self.dequeue()
        

    
    