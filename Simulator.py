# -*- coding: utf-8 -*-
"""
@author: batek
"""

import pandas as pd

class Sensor(object):
    
    sensorData = {}
    sensorName = ""
    
    def __init__(self, name):
        self.sensorName = name
        print ("Sensor " + name + " created")
        
    def SetDictOfData(self, data):
        self.sensorData = data
    
    def GetOutputBasedOnTimestamp(self, timestamp):
        return self.sensorData[timestamp]
    

class ExcelFileImporter(object):

    fileName = ""
    
    def __init__(self, fileName):
        self.fileName = fileName
        
    '''
    Rturns DataFrame object,
    which is firs sheet in given excel file
    '''
    def loadFile(self):
        file = pd.ExcelFile(self.fileName)
        return file.parse(file.sheet_names[0])
    

class DataInitializer(object):
    
    excelFileName = ""
    
    def __init__(self, excelFileName):
        self.excelFileName = excelFileName
        print ("Data initialization begins!")
        
    def LOadDataAndReturnSensors(self):
        
        sensors = []
        excelFile = ExcelFileImporter(self.excelFileName)
        importer = excelFile.loadFile()
        
        '''
        0 column - index
        1 column - TimeStamp
        
        2 ... N  - Sensor
        '''
        
        timestamps = importer[importer.columns[1]]
        timestamps = timestamps[1:]
        
        for i in range(2, len(importer.columns)):
            
            nSensor = Sensor(importer.columns[i])
            sensorData = importer[importer.columns[i]]
            
            sensorDict = dict(zip(timestamps, sensorData[1:]))
            
            nSensor.SetDictOfData(sensorDict)
            
            sensors.append(nSensor)
        
        return sensors
            
            
            
            
        
        



var = DataInitializer(r"C:\Users\batek\Downloads\Data for UNI Ostrava\0010 CO-Sensorvalues on event base.xlsx")


print(var.LOadDataAndReturnSensors()[3].sensorData)

    
    
            
    
    
    
        