# -*- coding: utf-8 -*-
"""
@author: batek
"""

import pandas as pd

class Sensor(object):
       
    
    def __init__(self, name):
        self._sensorName = name
        self._battery = Battery(100, 1)
        print ("Sensor " + name + " created")
        
    def SetDictOfData(self, data):
        self._sensorData = data
    
    def GetOutputBasedOnTimestamp(self, timestamp):
        hasBattery = self._battery.dischargePower(timestamp)
        return self._sensorData[timestamp] if hasBattery else "Battery discharged!"
    
    def batteryLeft(self):
        return self._battery.capacityLeft()
    

class ExcelFileImporter(object):
    
    def __init__(self, fileName):
        self._fileName = fileName
        
    '''
    Rturns DataFrame object,
    which is first sheet in given excel file
    '''
    def loadFile(self):
        file = pd.ExcelFile(self._fileName)
        return file.parse(file.sheet_names[0])
    
    
'''

Class for carrying global data.
variables intended to use as static
'''
class DTO(object):
    _times = None
    
    
    
class DataInitializer(object):
        
    def __init__(self, excelFileName):
        self._excelFileName = excelFileName
        print ("Data initialization begins!")
        
    def LOadDataAndReturnSensors(self):
        
        sensors = []
        excelFile = ExcelFileImporter(self._excelFileName)
        importer = excelFile.loadFile()
        
        '''
        0 column - index
        1 column - TimeStamp
        
        2 ... N  - Sensor
        '''
        
        timestamps = importer[importer.columns[1]]
        timestamps = timestamps[1:]
        
        # store defined times for later use
        DTO._times = timestamps
        
        for i in range(2, len(importer.columns)):
            
            nSensor = Sensor(importer.columns[i])
            sensorData = importer[importer.columns[i]]
            
            sensorDict = dict(zip(timestamps, sensorData[1:]))
            
            nSensor.SetDictOfData(sensorDict)
            
            sensors.append(nSensor)
        
        return sensors
            
class Battery(object):
    
    def __init__(self, capacity= 100, energyStep= 1):
        self._capacity = capacity
        self._energyStep = energyStep
        self._lastTime = -1
        self._firstTimeCheck = True
    
    # returns true, if there is power left
    def dischargePower(self, time):
        if self._firstTimeCheck:
            self._capacity -= self._energyStep
            self._lastTime = time
            self._firstTimeCheck = False
        else:
            timeDiff = time - self._lastTime
            self._capacity -= self._energyStep
            self._lastTime = time
        return self._capacity > 0
    
    def capacityLeft(self):
        return self._capacity
            

class RunSimulation(object):
    
    def __init__(self,excelDataPath,  verbose = False, toFile=False, fileName=""):
        self._excelDataPath = excelDataPath
        self._verbose = verbose
        self._printToFile = toFile
        self._fileName = fileName
        if self._printToFile:
            if self._fileName is "":
                self._fileName = "sensorOutput.txt"
            self._file = open(self._fileName, "w")
        print("simulatin initalized!")
        
    def printV(self, text):
        if self._verbose:
            if self._printToFile:
                self._file.write(text  + "\n")        
            else:
                print(text)
    
    def closeFileOutput(self):
        if self._printToFile:
            self._file.close()
        
        
    def runSimulation(self):
        dataIOnitializer = DataInitializer(self._excelDataPath)
        sensorList = dataIOnitializer.LOadDataAndReturnSensors()
        
        for time in DTO._times:
            
            for sensor in sensorList:
                
                self.printV(sensor._sensorName + ";CO2_level:" + ";battery_left:" + str(sensor.batteryLeft()))
        
        self.closeFileOutput()
        

##########################################################################################################
xslPath = r"C:\Users\batiha\Downloads\Data for UNI Ostrava\0010 CO-Sensorvalues on event base.xlsx"

simulation = RunSimulation(xslPath, True, True)                    

simulation.runSimulation()
            
        
        
        
        







