# -*- coding: utf-8 -*-
"""
@author: batek
"""

import pandas as pd

class Sensor(object):
    
    _sensorData = {}
    _sensorName = ""
    _battery = None
    
    
    def __init__(self, name):
        self._sensorName = name
        self._battery = Battery(100, 1)
        print ("Sensor " + name + " created")
        
    def SetDictOfData(self, data):
        self._sensorData = data
    
    def GetOutputBasedOnTimestamp(self, timestamp):
        hasBattery = _battery.dischargePower(timestamp)
        return self._sensorData[timestamp] if hasBattery else "Battery discharged!"
    
    def batteryLeft(self):
        return self._battery.capacityLeft()
    

class ExcelFileImporter(object):

    _fileName = ""
    
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
    
    _excelFileName = ""
    
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
    
    _capacity = 0
    _energyStep = 0
    _lastTime = -1
    _firstTimeCheck = True
    
    def __init__(self, capacity= 100, energyStep= 1):
        _capacity = capacity
        _energyStep = energyStep
    
    # returns true, if there is power left
    def dischargePower(self, time):
        if _firstTimeCheck:
            _capacity -= _energyStep
            _lastTime = time
            _firstTimeCheck = False
        else:
            timeDiff = time - _lastTime
            _capacity -= _energyStep
            _lastTime = time
        return _capacity > 0
    
    def capacityLeft(self):
        return _capacity
            

class RunSimulation(object):
    
    _sensorsList = []
    _verbose = False
    _excelDataPath = r""
    
    def __init__(self,excelDataPath,  verbose = False):
        _excelDataPath = excelDataPath
        _verbose = verbose
        print("simulatin initalized!")
        
    def printV(self, text):
        if _verbose:
            print(text)
        
        
    def runSimulation(self):
        dataIOnitializer = DataInitializer(self._excelDataPath)
        _sensorList = dataIOnitializer.LOadDataAndReturnSensors()
        
        for time in DTO._times:
            
            for sensor in _sensorList:
                
                printV(sensor._sensorName + ";CO2_level:" + ";battery_left:" + sensor.batteryLeft())


##########################################################################################################
xslPath = r"C:\Users\batiha\Downloads\Data for UNI Ostrava\0010 CO-Sensorvalues on event base.xlsx"

simulation = RunSimulation(xslPath, True)                    

simulation.runSimulation()
            
        
        
        
        







