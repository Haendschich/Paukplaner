# -*- coding: utf-8 -*-

import tkinter as tk
import os
import plan

def windowStundenplan(self):
    window = tk.Toplevel()
    window.title("Stundenpläne")
    
    topWindow = tk.Frame(window)
    topWindow.pack(side='top')
    
    createAuswahl(self, topWindow)
    createTable(self, topWindow)    
    
    def saveAndExit():
        saveStatus(self)
        self.fillPaukantHoursFrame()
        self.aktNumberOfHours()
        window.destroy()
        
    window.protocol("WM_DELETE_WINDOW", saveAndExit)
    
def createAuswahl(self, window):
    auswahlFrame = tk.Frame(window, width="100")
    auswahlFrame.pack(padx=5, side='left', anchor='n')
        
    newFrame = tk.LabelFrame(auswahlFrame, text="Neuer Paukant", width=30)
    newFrame.pack(anchor='w')
    
    subAuswahl = tk.Frame(auswahlFrame)
    subAuswahl.pack()
    self.paukantAuswahl = tk.Listbox(subAuswahl,
                                    width=30, height=12,
                                    selectmode='single')
    self.paukantAuswahl.pack(side='left')
    
    scrollbarAuswahl = tk.Scrollbar(subAuswahl)
    scrollbarAuswahl.pack(side='left', fill='y')
    self.paukantAuswahl['yscrollcommand'] = scrollbarAuswahl.set
    scrollbarAuswahl['command'] = self.paukantAuswahl.yview
    
    def loadPaukanten(event=None):
        paukanten = os.listdir('stundenplaene')
        
        self.paukantAuswahl.delete(0,'end')
        for p in paukanten:
            self.paukantAuswahl.insert('end', p[:-4])
            
    def deletePaukant(event=None):
        try:
            os.remove(f'stundenplaene/{self.paukantAuswahl.get(self.paukantAuswahl.curselection())}.txt')
            loadPaukanten()
        except:
            return
    
    def save(event=None):
        saveStatus(self)
    
    def load(event=None):
        loadStatus(self)
    
    self.paukantAuswahl.bind('<KeyPress-Delete>', deletePaukant)
    self.paukantAuswahl.bind('<ButtonPress-1>', save)
    self.paukantAuswahl.bind('<space>', save)
    self.paukantAuswahl.bind('<<ListboxSelect>>', load)

    loadPaukanten()
        
    self.newVar = tk.StringVar()
    newText = tk.Entry(newFrame, textvariable=self.newVar, width=25)
    newText.pack(side='left')
        
    def addPaukant(event=None):
        if not self.newVar.get()+'.txt' in os.listdir('stundenplaene') and self.newVar.get() != "":
            with open('stundenplaene/'+self.newVar.get()+'.txt','w') as file:
                file.write(f"name: {self.newVar.get()}\nlessons: 10\ntype: Hoch\n\nmonday:\ntuesday:\nwednesday:\nthursday:\nfriday:\nsaturday:\nsunday:")
            self.newVar.set("")
            loadPaukanten()
    
    newText.bind('<Return>',addPaukant)
    tk.Button(newFrame, text="+", command=addPaukant, width=2).pack(side='left', padx=3)
    
    paukantOptionsFrame = tk.Frame(auswahlFrame)
    paukantOptionsFrame.pack(side='top', anchor='w')
    
    sollFrame = tk.Frame(paukantOptionsFrame, pady=2)
    sollFrame.pack(side='top', anchor='w')
    tk.Label(sollFrame, text='Soll: ').pack(side='left')
    self.paukantSoll = tk.StringVar()
    paukantSoll = tk.Spinbox(sollFrame, from_=0, to=99,  width=3, textvariable=self.paukantSoll)
    paukantSoll.pack(side='left')
    
    self.paukantArt = tk.StringVar()
    paukantArt = tk.OptionMenu(paukantOptionsFrame, self.paukantArt, 'Hoch', 'Tief', 'Inaktiv', 'Tiefleiter', 'Fechtmeister')
    paukantArt.pack(side='top', anchor='w')
    
def createTable(self, window):
    tableFrame = tk.Frame(window)
    tableFrame.pack(side='left', anchor='n')
    
    daysFrame = tk.Frame(tableFrame)
    daysFrame.pack(side='top', anchor='n')
        
    for d in [""] + plan.daylistGerman:
        tk.Label(daysFrame, width=20, height=1, text=d).pack(side='left', anchor='w', padx=2)
    
    gridFrame = tk.Frame(tableFrame)
    gridFrame.pack(side='top')
    
    timeFrame = tk.Frame(gridFrame)
    timeFrame.pack(side='left', anchor='n')
        
    for t in range(8,24,2):
        tk.Label(timeFrame, 
                 width=10, height=2, 
                 text=str(t)+":00 Uhr").pack(side='top', pady=3)
        
    def changeStatus(event):
        if event.widget['bg'] == 'green':
            event.widget['bg'] = 'white'
        else:
            event.widget['bg'] = 'green'
    
    dayFrames = [tk.Frame(gridFrame) for i in range(7)]
    for d in dayFrames:
        d.pack(side='left')
    
    self.timeButtons = [[],[],[],[],[],[],[]]
    for d, day in enumerate(dayFrames):
        for time in range(8):
            self.timeButtons[d].append(tk.Button(day, width=20, height=2, bg='white'))
            self.timeButtons[d][time].pack(side='top')
            self.timeButtons[d][time].bind('<ButtonPress-1>', changeStatus)
            
def saveStatus(self):
    try: 
        self.paukantAuswahl.curselection()[0]
    except:
        self.loadPaukplan()
        return
    
    with open(f'stundenplaene/{self.paukantAuswahl.get(self.paukantAuswahl.curselection()[0])}.txt', 'w') as file:
        file.write(f"name: {self.paukantAuswahl.get(self.paukantAuswahl.curselection()[0])}\n")
        file.write(f"lessons: {self.paukantSoll.get()}\n")
        file.write(f"type: {self.paukantArt.get()}\n\n")
            
        for i, d in enumerate(plan.daylist):
            file.write(f"{d}: ")
            for j, button in enumerate(self.timeButtons[i]):
                if button['bg'] == 'green':
                    file.write(f"{j if j==0 else ''}{8+2*j}:15-{j if j==0 else ''}{9+2*j}:45; ")
            file.write("\n")
            
    self.loadPaukplan()

def loadStatus(self):
    try:
        self.paukantAuswahl.get(self.paukantAuswahl.curselection()[0])
    except:
        return
    
    try:
        file = open(f'stundenplaene/{self.paukantAuswahl.get(self.paukantAuswahl.curselection()[0])}.txt', 'r')
        file.readlines()[2]
    except:
        self.paukantSoll.set('10')
        self.paukantArt.set('Hoch')
        return
    
    with open(f'stundenplaene/{self.paukantAuswahl.get(self.paukantAuswahl.curselection()[0])}.txt', 'r') as file:
        file = file.readlines()
        self.paukantSoll.set(file[1].split()[1])
        self.paukantArt.set(file[2].split()[1])
        
        for day in range(7):
            times = file[day+4].split()[1:]
            for b in self.timeButtons[day]:
                b['bg'] = 'white'
            for t in times:
                self.timeButtons[day][int((int(t[:2] if not ':' in t[:2] else t[:1])-8)/2)]['bg'] = 'green'
                
                