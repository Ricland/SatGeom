import sys
from PyQt5 import QtWidgets, QtGui
import design
import math

class SatGeom(QtWidgets.QMainWindow, design.Ui_Form) :
    def __init__(self): 
        super().__init__()
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.solve) #нажатие на кнопку
    
    def solve (self) :
        self.textEdit.clear()
        
        latRec = self.lineEdit.text()
        lngRec = self.lineEdit_2.text()
        latSat_1 = self.lineEdit_3.text()
        lngSat_1 = self.lineEdit_4.text()
        h = self.lineEdit_7.text()

        if validation_of_data_1 (latRec, lngRec, latSat_1, lngSat_1, h) :
            latRec = float(self.lineEdit.text())
            lngRec = float(self.lineEdit_2.text())
            latSat_1 = float(self.lineEdit_3.text())
            lngSat_1 = float(self.lineEdit_4.text())
            h = float(self.lineEdit_7.text())

            azimS_1, elevS_1, latP_1, lngP_1, dRecP_1, dPSat_1 = calc(latRec, lngRec, latSat_1, lngSat_1, h)

            self.textEdit.insertPlainText("НИСЗ №1: \n\n")
            self.textEdit.insertPlainText("Азимут: " + '{:.2f}'.format(azimS_1) + "°\n")
            self.textEdit.insertPlainText("Угол места: " + '{:.2f}'.format(elevS_1) + "°\n")
            self.textEdit.insertPlainText("Координаты подионосферной точки: " + '{:.2f}'.format(latP_1) + "° " + '{:.2f}'.format(lngP_1) + "°\n")
            self.textEdit.insertPlainText("Расстояние от приёмника до подионосферной точки: " + '{:.2f}'.format(dRecP_1) + " км\n")
            self.textEdit.insertPlainText("Расстояние от подионосферной точки до точки проекции НИСЗ: " + '{:.2f}'.format(dPSat_1) + " км\n\n")
            self.textEdit.insertPlainText("----------------------------------------------------------------------------------------------\n\n")
            
            if self.lineEdit_5.text() and self.lineEdit_6.text() != "" :
                latSat_2 = self.lineEdit_5.text()
                lngSat_2 = self.lineEdit_6.text()

                if validation_of_data_2 (latSat_2, lngSat_2) :
                    latSat_2 = float(self.lineEdit_5.text())
                    lngSat_2 = float(self.lineEdit_6.text())

                    azimS_2, elevS_2, latP_2, lngP_2, dRecP_2, dPSat_2 = calc(latRec, lngRec, latSat_2, lngSat_2, h)
                    dPtoP = 12742 * math.asin(math.sqrt((math.sin((degToRad(latP_1) - degToRad(latP_2)) / 2)) ** 2 + math.cos(degToRad(latP_1)) * math.cos(degToRad(latP_2)) * math.sin((degToRad(lngP_1) - degToRad(lngP_2)) / 2) ** 2))

                    self.textEdit.insertPlainText("НИСЗ №2: \n\n")
                    self.textEdit.insertPlainText("Азимут: " + '{:.2f}'.format(azimS_2) + "°\n")
                    self.textEdit.insertPlainText("Угол места: " + '{:.2f}'.format(elevS_2) + "°\n")
                    self.textEdit.insertPlainText("Координаты подионосферной точки: " + '{:.2f}'.format(latP_2) + "° " + '{:.2f}'.format(lngP_2) + "°\n")
                    self.textEdit.insertPlainText("Расстояние от приёмника до подионосферной точки: " + '{:.2f}'.format(dRecP_2) + " км\n")
                    self.textEdit.insertPlainText("Расстояние от подионосферной точки до точки проекции НИСЗ: " + '{:.2f}'.format(dPSat_2) + " км\n\n")
                    self.textEdit.insertPlainText("----------------------------------------------------------------------------------------------\n")
                    self.textEdit.insertPlainText("Расстояние между подионосферными точками: " + '{:.2f}'.format(dPtoP) + " км") 
                else :
                    self.textEdit.insertPlainText("Ошибка ввода!")
        else :
            self.textEdit.insertPlainText("Ошибка ввода!")
        
def degToRad (a) : 
    return a * math.pi / 180.

def radToDeg (a) :  
    return a * 180. / math.pi

def calc (latRec, lngRec, latSat, lngSat, h) : 
    rE = 6371 #радиус Земли
    rS = 26571 #радиус орбиты НИСЗ
    
    latRec = degToRad(latRec)
    lngRec = degToRad(lngRec)
    latSat = degToRad(latSat)
    lngSat = degToRad(lngSat) 
    
    psyS = math.acos(math.sin(latRec) * math.sin(latSat) + math.cos(latRec) * math.cos(latSat) * math.cos(lngSat - lngRec)) #центральный угол между точкой наблюдения и НИСЗ
    azimS = math.atan2((math.sin(lngSat - lngRec) * math.cos(latSat)), (math.cos(latRec) * math.sin(latSat) - math.sin(latRec) * math.cos(latSat) * math.cos(lngSat - lngRec))) #азимут на НИСЗ
    if azimS < 0 :  
        azimS = 2 * math.pi + azimS
    elevS = math.atan((math.cos(psyS) - rE / rS) / math.sin(psyS)) #угол места 
    
    psyP = math.pi / 2 - elevS - math.asin(rE / (rE + h) * math.cos(elevS)) #центральный угол между точкой наблюдения и ионосферной точкой
    latP = math.asin(math.sin(latRec) * math.cos(psyP) + math.cos(latRec) * math.sin(psyP) * math.cos(azimS)) #широта подионосферной точки
    lngP = lngRec + math.asin(math.sin(psyP) * math.sin(azimS) / math.cos(latP)) #долгота подионосферной точки

    dRecP = 2 * rE * math.asin(math.sqrt((math.sin((latRec - latP) / 2)) ** 2 + math.cos(latRec) * math.cos(latP) * math.sin((lngRec - lngP) / 2) ** 2)) #расстояние от приёмника до подионосферной точки
    dPSat = 2 * rE * math.asin(math.sqrt((math.sin((latP - latSat) / 2)) ** 2 + math.cos(latP) * math.cos(latSat) * math.sin((lngP - lngSat) / 2) ** 2)) #расстояние от подионосферной точки до проекции НИСЗ на Землю
    
    return radToDeg(azimS), radToDeg(elevS), radToDeg(latP), radToDeg(lngP), dRecP, dPSat

def validation_of_data_1 (latRec, lngRec, latSat, lngSat, h) :
    try :
        float(latRec)
        float(lngRec)
        float(latSat)
        float(lngSat)
        float(h)
        return True
    except Exception :
        return False

def validation_of_data_2 (latSat, lngSat) :
    try :
        float(latSat)
        float(lngSat)
        return True
    except Exception :
        return False
            
def main() :
    app = QtWidgets.QApplication(sys.argv)
    window = SatGeom()
    window.show()
    app.exec_()

if __name__ == '__main__' :
    main()
