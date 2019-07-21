class Instance:
    def __init__(self, id, size, userCount):
        self.size = size
        self.id = userCount
        self.originalId = id
        
        """
        if self.size == 2:
            self.price = self.size + 0.125
        elif self.size == 4:
            self.price = self.size + 0.25
        elif self.size == 8:
            self.price = self.size + 0.5
        else:
            self.price = self.size
        """
        self.price = 1.0 / userCount * size
        #self.price = 1
        self.begins = []
                