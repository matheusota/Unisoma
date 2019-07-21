"""
dias:
seg -> 0, ter -> 1, ..., sexta -> 4

horas:
7:30 -> 0, 8:00 -> 1, ... 17:00 -> 17

Manhã: horas de 0 a 8
Tarde: horas de 9 a 17
"""
def getDayNumber(day):
    dayMap = {
        "Segunda" : 0,
        "Terça" : 1,
        "Quarta" : 2,
        "Quinta" : 3,
        "Sexta" : 4
    }

    return dayMap[day]

def getHourNumber(hours):
    h, m = [int(x) for x in hours.split(":")]
    
    x = 2 * (h - 7) + (1 if m > 30 else 0) - 1

    if h >= 13:
        x -= 2
    
    return x

