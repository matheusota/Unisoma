class Worker:
    def __init__(self):
        self.name = ""
        self.available = [[True for _ in range(18)] for _ in range(5)]
        self.type = ""

    # read a worker file and put it in a worker class
    def readWorker(self, filepath):
        filename = filepath.split("/")[-1]
        self.name = filename.split(".")[0]

        with open(filepath) as file:
            i = 0

            for line in file:
                line = line.split(",")

                if i == 0:
                    self.type = line[0]
                
                else:
                    for j in range(5):
                        if line[j + 1] != "" and line[j + 1] != "\n":
                            self.available[j][i - 1] = False
                
                i += 1
    
    def __str__(self):
        s = "----------------------------------------\n"
        s += "Worker Name: " + self.name + "\n"
        s += "Availability:\n"
        for i in range(5):
            s += str(self.available[i]) + "\n"
        
        return s
        
        