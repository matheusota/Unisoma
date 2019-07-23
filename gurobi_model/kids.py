from dayblockhelper import *

class Attendance:
    def __init__(self, type, number):
        self.type = type
        self.number = number

    def __str__(self):
        return "(" + self.type + ", " + str(self.number) + ")"

class Kid:
    def __init__(self, name):
        self.name = name
        self.available = [[False for _ in range(18)] for _ in range(5)]
        self.attendances = []

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
        self.attendances.append(Attendance(type, number))
    
    def __str__(self):
        s = "----------------------------------------\n"
        s += "Kid Name: " + self.name + "\n"
        s += "Availability:\n"
        for i in range(5):
            s += str(self.available[i]) + "\n"
        s += "Attendances:\n"
        for attendance in self.attendances:
            s += str(attendance) + ", "
        s += "\n"
        
        return s

class Kids:
    def __init__(self):
        self.kids = {}
    
    # get kids ids from the registers file
    def readKidsRegisters(self, filepath):
        with open(filepath) as file:
            i = 0

            for line in file:
                line = line.split(",")
                
                if i > 0:
                    for j in range(5):
                        self.kids[line[0]] = Kid(line[0])
                
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
        return self.kids[key]
    
    def __len__(self):
        return len(self.kids)
        
    def __str__(self):
        s = ""
        for kid in self.kids.values():
            s += str(kid)
        
        return s