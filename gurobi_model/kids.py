from dayblockhelper import *

class Kid:
    def __init__(self, name):
        self.name = name
        self.available = [[False for _ in range(18)] for _ in range(5)]
        self.attendances = {}

    # set a whole day availability to a given status
    def setDayAvailability(self, day, status):
        for i in range(18):
            self.available[day][i] = status
    
    # set availability of a kid
    def setAvailability(self, day, period, start, end):
        # set day availability
        if day != "Todos":
            j = getDayNumber(day)
            self.setDayAvailability(j, True)
        else:
            for i in range(5):
                self.setDayAvailability(i, True)
        
        # set period availability
        if period == "Manhã":
            for i in range(5):
                for j in range(9, 18):
                    self.available[i][j] = False

        elif period == "Tarde":
            for i in range(5):
                for j in range(9):
                    self.available[i][j] = False

        elif period == "Horário":
            start = getHourNumber(start)
            end = getHourNumber(end)

            for i in range(5):
                for j in range(18):
                    if j < start or j > end:
                        self.available[i][j] = False

    # add an attendance
    def addAttendance(self, type, number):
        self.attendances[type] = number
    
    # get number of attendances
    def getAttendanceNumber(self, type):
        return self.attendances.get(type, 0)
    
    def __str__(self):
        s = "----------------------------------------\n"
        s += "Kid Name: " + self.name + "\n"
        s += "Availability:\n"
        for i in range(5):
            s += str(self.available[i]) + "\n"
        s += "Attendances:\n"
        for t in self.attendances:
            s += "\t" + t + ", " + str(self.attendances[t]) + "\n"

        if len(self.attendances) == 0: 
            s += "\n"
        
        return s

class Kids:
    def __init__(self):
        self.kids = {}
        self.kids_names = []
    
    # get kids ids from the registers file
    def readKidsRegisters(self, filepath):
        with open(filepath) as file:
            i = 0

            for line in file:
                line = line.split(",")
                
                if i > 0:
                    name = line[0]
                    type = line[-1].replace("\n", "")

                    if type == "Regular":
                        self.kids[name] = Kid(name)
                        self.kids_names.append(name)
                
                i += 1
    
    # get kids availability
    def readKidsAvailability(self, filepath):
        with open(filepath) as file:
            i = 0

            for line in file:
                line = line.split(",")
                
                if i > 0:
                    name = line[0]
                    day = line[1]
                    period = line[2]
                    start = line[3]
                    end = line[4]

                    if name in self.kids:
                        self.kids[name].setAvailability(day, period, start, end)
                
                i += 1
    
    # get kids attendaces needs
    def readKidsAttendances(self, filepath):
        with open(filepath) as file:
            i = 0

            for line in file:
                line = line.split(",")
                
                if i > 0:
                    name = line[0]
                    type = line[1]
                    number = line[2]
                    frequency = line[3]
                    reeschedule = line[4]

                    # ONLY DEALING WITH WEAKLY SCHEDULINGS FIRST
                    if frequency == "Semanal":
                        self.kids[name].addAttendance(type, number)
                
                i += 1
    
    # rewrite [] operator
    def __getitem__(self, key):
        if type(key) == str:
            return self.kids[key]
        elif type(key == int):
            return self.kids[self.kids_names[key]]
        else:
            return None
    
    def __len__(self):
        return len(self.kids)
        
    def __str__(self):
        s = ""
        for kid in self.kids.values():
            s += str(kid)
        
        return s