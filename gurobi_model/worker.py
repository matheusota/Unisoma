class Worker:
    def __init__(self):
        self.available = [[True for _ in range(18)] for _ in range(5)]
        self.type = ""

    # read a worker file and put it in a worker class
    def readWorker(self, filepath):
        with open(filepath) as file:
            i = 0

            for line in file:
                line = line.split(",")

                if i == 0:
                    self.type = line[0]
                
                else:
                    for j in range(5):
                        if line[j + 1] != "":
                            self.available[j][i - 1] = False
                
                i += 1