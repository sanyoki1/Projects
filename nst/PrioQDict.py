class PrioQ:
    def __init__(self): self.q = {}
    def __len__(self) -> int: return len(self.q)
    def get_list(self) -> dict: return self.q

    def enqueue(self, item, val: int):
        if item not in self.q.keys():
            self.q[item] = [val]
        else:
            self.q[item].append(val)
        return

    def dequeue(self):
        if len(self.q) == 0:
            print("cant dequeue")
            exit()
        mn = 99999
        minKey = None
        for key in self.q.keys():
            for val in self.q[key]:
                if val < mn:
                    mn = val
                    minKey = key
        self.q[minKey].remove(mn)
        if len(self.q[minKey]) == 0:
            self.q.pop(minKey)
        return minKey

    def remove(self, item):
        if item not in self.q.keys():
            print("item not in queue")
        else:
            for i in range(len(self.q[item])):
                if self.q[item][i] == item.getFScore():
                    self.q[item].pop(i)
            if len(self.q[item]) == 0:
                self.q.pop(item)

    def get_items(self):
        return self.q.keys()