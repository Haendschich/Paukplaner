# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import os
import stundenplaeneGUI
import plan

class GUI(tk.Frame):
    
    def __init__(self, master):
        super().__init__(master)
        self.pack(ipadx=10, ipady=10)
        
        self.paukplan = plan.Paukplan([plan.Paukant(name[:-4]) for name in os.listdir('stundenplaene/')])
        
        self.createWidgets()
        self.colorize()
        self.aktNumberOfHours()
        
        self.menuBar = tk.Menu(master)
        master.config(menu=self.menuBar)
        self.fillMenuBar()
        
    def createWidgets(self):
        mainFrame = tk.Frame(self, width=300, height=200)
        mainFrame.pack()
        
        tableFrame = tk.Frame(mainFrame)
        tableFrame.pack(side='top')
        
        dayFrames = [tk.LabelFrame(tableFrame, text=plan.daylistGerman[i]) for i in range(7)]
        for f in dayFrames:
            f.pack(side='left', anchor='w')
        
        self.timeFrames = plan.Week(None)
        self.timeLeiter = plan.Week(None)
        self.timeFraction = plan.Week(None)
        
        for d, day in enumerate(plan.daylist):
            for time in plan.onlyhour:
                self.timeFrames[day][f'{time}00'] = tk.Frame(dayFrames[d], height=1)
                self.timeFrames[day][f'{time}00'].pack(side='top')
                self.timeFrames[day][f'{time}00'].bind('<Enter>',lambda event, day=day, time=time: self.enterHover(day, time))
                self.timeFrames[day][f'{time}00'].bind('<Leave>',lambda event, day=day, time=time: self.leaveHover(day, time))                
                
                self.createTimeFractionSpinbox(day, time)
                
                self.createTimeLeiterOptionMenu(day, time)
                
        self.paukantHoursFrame = tk.Frame(mainFrame)
        self.paukantHoursFrame.pack(side='top', anchor='w')
        
        self.fillPaukantHoursFrame()

    def createTimeFractionSpinbox(self, day, time):
        tk.Label(self.timeFrames[day][f'{time}00'], text=f"{time}:").pack(side='left')
        
        for fraction in ['00','15','30','45']:
            if self.paukplan.plan[day][time+fraction]:
                value = fraction
                break
            else:
                value = '00'
                
        self.timeFraction[day][f'{time}00'] = tk.StringVar()
        tk.Spinbox(self.timeFrames[day][f'{time}00'], values=['00','15','30','45'], 
                   textvariable=self.timeFraction[day][f'{time}00'],
                   command=lambda day=day, time=f'{time}00': self.aktPaukplan(day, time),
                   width=2).pack(side='left')
        self.timeFraction[day][f'{time}00'].set(value)
        
    def createTimeLeiterOptionMenu(self, day, time):
        for fraction in ['00','15','30','45']:
            if self.paukplan.plan[day][time+fraction]:
                value = self.paukplan.plan[day][time+fraction]
                break
            else:
                value = ''
        
        self.timeLeiter[day][f'{time}00'] = tk.StringVar(value=value)
        timeLeiter = tk.OptionMenu(self.timeFrames[day][f'{time}00'],
                                   self.timeLeiter[day][f'{time}00'],
                                   "", *[p for p in self.paukplan.getLeiter()],
                                   command=lambda event, day=day, time=f'{time}00': self.aktPaukplan(day, time))
        timeLeiter.config(width=12, height=1)
        timeLeiter.pack(side='left')
        
    def fillMenuBar(self):
        self.menuFile = tk.Menu(self.menuBar,tearoff=False)
        self.menuFile.add_command(label="Speichern", command=self.paukplan.savePaukplan)
        #self.menuFile.add_command(label="Exportieren")
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Beenden", command=on_closing)
        self.menuBar.add_cascade(label="Datei", menu=self.menuFile)
        
        self.menuSettings = tk.Menu(self.menuBar,tearoff= False)
        self.menuSettings.add_command(label="Stundenpläne", command=self.openStundenplan)
        #self.menuSettings.add_command(label="Fechtmeister")
        self.menuBar.add_cascade(label="Einstellungen", menu=self.menuSettings)
        
    def loadPaukplan(self):
        self.paukplan.listOfPaukanten = [plan.Paukant(name[:-4]) for name in os.listdir('stundenplaene/')]
        self.paukplan.possibility = plan.createPossibility(self.paukplan.listOfPaukanten)
        try:
            self.colorize()
        except:
            pass
        
    def colorize(self):
        if not self.paukplan.listOfPaukanten:
            return
        for day in plan.daylist:
            for time in plan.onlyhour:
                self.timeFrames[day][f'{time}00']['background'] = plan.getColor(len(self.paukplan.possibility[day][f'{time}{self.timeFraction[day][time+"00"].get()}'])/len([p for p in self.paukplan.listOfPaukanten if p.type not in ['Tiefleiter', 'Fechtmeister', 'Inaktiv']])) 
                for child in self.timeFrames[day][f'{time}00'].winfo_children():
                    if not child.winfo_class() == 'Menubutton':
                        child['background'] =  plan.getColor(len(self.paukplan.possibility[day][f'{time}{self.timeFraction[day][time+"00"].get()}'])/len([p for p in self.paukplan.listOfPaukanten if p.type not in ['Tiefleiter', 'Fechtmeister', 'Inaktiv']]))
        
    def openStundenplan(self):
        stundenplaeneGUI.windowStundenplan(self)
        
    def aktPaukplan(self, day, time):
        for t in ['00','15','30','45']:
            self.paukplan.plan[day][f'{time[:2]}{t}'] = ''
        
        self.paukplan.plan[day][f'{time[:2]}{self.timeFraction[day][time].get()}'] = self.timeLeiter[day][time].get()
        
        self.aktNumberOfHours()
    
    def fillPaukantHoursFrame(self):
        for w in self.paukantHoursFrame.winfo_children():
            w.destroy()
        
        lineFrames = [tk.Frame(self.paukantHoursFrame) for i in range(int(len(self.paukplan.getHourlistNames())/10)+1)]
        for f in lineFrames:
            f.pack(side='top', anchor='w')
        
        self.numberOfHours = {x: tk.StringVar(value='0') for x in self.paukplan.getHourlistNames()}
        
        self.paukantLabelList = []
        for i, p in enumerate(self.paukplan.getHourlistNames()):
            frame = tk.LabelFrame(lineFrames[int(i/10)], padx=3)
            frame.pack(side='left')
            self.paukantLabelList.append(tk.Label(frame, text=p, width=12, font=('Helvetica', 9, 'normal')))
            self.paukantLabelList[-1].pack(side='left', anchor='w')
            tk.Entry(frame, width=2, textvariable=self.numberOfHours[p], state='disabled').pack(side='left')
        
    def enterHover(self, day, time):
        for i, paukant in enumerate(self.paukantLabelList):
            if paukant.cget('text') in self.paukplan.possibility[day][f'{time[:2]}{self.timeFraction[day][time+"00"].get()}']:
                self.paukantLabelList[i]['fg'] = 'blue'
                self.paukantLabelList[i]['font'] = ('Helvetica', 9, 'bold')
    
    def leaveHover(self, day, time):
        for p in self.paukantLabelList:
            p['fg'] = 'black'
            p['font'] = ('Helvetica', 9, 'normal')
            
    def aktNumberOfHours(self):
        for paukant in self.paukplan.getHourlistNames():
            summe = 0
            for day in plan.daylist:
                for time in plan.timelist:
                    if paukant in self.paukplan.possibility[day][time] and self.paukplan.plan[day][time]:
                        if not (self.paukplan.getTypeByName(paukant) == 'Hoch' and self.paukplan.getTypeByName(self.paukplan.plan[day][time]) == 'Tiefleiter'):
                            summe += 1
            self.numberOfHours[paukant].set(summe)
    
def on_closing(gui):
    save = messagebox.askyesnocancel("Schließen", "Vor dem Beenden speichern?")
    if save:
        gui.paukplan.savePaukplan()
    if save is None:
        return
    
    root.destroy()
        
root = tk.Tk(className=" Paukplaner")
gui = GUI(root)

root.protocol("WM_DELETE_WINDOW", lambda: on_closing(gui))
gui.mainloop()