from kids import *
from worker import *

class Instance:
    def __init__(self):
        self.kids = []
        self.workers = []
    
    # read the kids and the workers in order to compose the instance structure
    def readInstance(self, path):
        # read the kids
        self.kids = Kids()
        self.kids.readKidsRegisters(path + "/CadastroDaCrianca.csv")
        self.kids.readKidsAvailability(path + "/DisponibilidadeDaCrianca.csv")
        self.kids.readKidsAttendances(path + "/AtendimentoRegular.csv")

        # read the workers
        workers_files = [
            "Funcionario1.csv", 
            "Funcionario2.csv", 
            "Funcionario3.csv",
            "Funcionario4.csv",
            "Funcionario6.csv",
            "AnaCecilia.csv",
            "Dayana.csv"
        ]

        for worker_file in workers_files:
            w = Worker()
            w.readWorker(path + "/" + worker_file)
            self.workers.append(w)
    
    def __str__(self):
        s = "Kids:\n"
        s += str(self.kids)
        s += "\nWorkers:\n"
        for worker in self.workers:
            s += str(worker)
        
        return s