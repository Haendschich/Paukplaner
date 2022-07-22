# -*- coding: utf-8 -*-

import copy

daylist = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
daylistGerman = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
timelist = [h+m 
            for h in ['08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
            for m in ['00','15','30','45']]
onlyhour = ['08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

def Day(fill):
    return {x: copy.copy(fill) for x in timelist}

def Week(declaration):
    return {x: Day(declaration) for x in daylist}

class Paukant:
    
    def __init__(self, name):
        self.name = name
        self.days = Week(False)
        self.load()
            
    def load(self):
        with open(f'stundenplaene/{self.name}.txt', 'r') as file:
            file = file.readlines()

            self.lessons = file[1].split()[1]
            self.type = file[2].split()[1]
            
            for i, day in enumerate(file[5:12]):
                for time in day.split()[1:]:
                    time = time.replace(':','')
                    stamp = time.split('-')[0]
                    end = time.split('-')[1][:-1]
                    while(stamp != end):
                        self.days[day.split(':')[0]][stamp] = True
                        stamp = incTime(stamp)
                    self.days[day.split(':')[0]][stamp] = True

def incTime(time):
    if time == '2345':
        return time
    if time[2:] == '45':
        return f'{"0" if time[:2]=="08" else ""}{str(int(time[:2])+1)}00'
    else:
        return f'{time[:2]}{str(int(time[2:])+15)}'



class Paukplan:
    
    def __init__(self, listOfPaukanten):
        self.listOfPaukanten = listOfPaukanten
        self.possibility = createPossibility(listOfPaukanten)
        self.plan = self.loadPaukplan()
    
    def getNames(self):
        return list(map(lambda p: p.name, self.listOfPaukanten))
    
    def getHourlistNames(self):
        return list(map(lambda p: p.name, [p for p in self.listOfPaukanten if p.type not in ['Tiefleiter', 'Inaktiv', 'Fechtmeister']]))
    
    def getLeiter(self):
        return [p.name for p in self.listOfPaukanten if not p.type == 'Hoch']
    
    def getTypeByName(self, name):
        for p in self.listOfPaukanten:
            if p.name == name:
                return p.type
    
    def savePaukplan(self):
        open("save.txt",'w').write(str(self.plan))
        
    def loadPaukplan(self):
        plan = Week('')
        try:
            with open('save.txt', 'r') as file:
                data = list(map(lambda x: x.split('{')[-1], file.read().split('}')))[:7]
        except:
            return plan
        
        for i,day in enumerate(daylist):
            data[i] = list(map(lambda x: x.strip(), data[i].split(',')))
            for time in data[i]:
                plan[day][time[1:5]] = time[9:-1]
        
        return plan

def createPossibility(stundenplaene):
    possibility = Week([])
        
    for paukant in stundenplaene:
        if paukant.type not in ['Inaktiv', 'Tiefleiter', 'Fechtmeister']:
            for day in paukant.days:
                for time in paukant.days[day]:
                    if paukant.days[day][time]:
                        continue
                    if paukant.days[day][incTime(time)]:
                        continue
                    if paukant.days[day][incTime(incTime(time))]:
                        continue
                    if paukant.days[day][incTime(incTime(incTime(time)))]:
                        continue
                    possibility[day][time].append(paukant.name)
    
    return possibility

def getColor(t):
    def add(l1, l2, l3):
        return tuple(map(lambda x1, x2, x3: x1+x2+x3, l1, l2, l3))
    def mul(f, l):
        return tuple(map(lambda x: int(x*f), l))
    def hexa(n):
        return hex(n)[2:] if len(hex(n))>3 else f'0{hex(n)[2:]}'
    
    tup = add(mul((1-t)**2, (255,0,0)),mul(2*(1-t)*t, (255,255,0)),mul(t**2, (0,255,0)))
    return f'#{hexa(tup[0])}{hexa(tup[1])}{hexa(tup[2])}'