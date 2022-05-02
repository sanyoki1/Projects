class PrioQ:

    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def get_items(self):
        l = []
        for i in self.queue:
            l.append(i[0])
        return l

    def enqueue(self, item, val):
        self.queue.append((item,val))

    def dequeue(self):
        currM = 99999
        select = None
        # select minimum
        for i in self.queue:
            if i[1] < currM:
                currM = i[1]
                select = i
        self.queue.remove(select)
        return select[0]

    def remove(self, item):
        match = None
        for i in range(len(self.queue)):
            if self.queue[i][0] == item and self.queue[i][1] == item.getFScore():
                self.queue.pop(i)
                return
        return