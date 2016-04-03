#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
import numpy as np
import PyQt4.Qwt5 as Qwt
import wave
import pyaudio
import thread
import time
import pylab
import matplotlib
import scipy
#Dołączenie Interfejsu graficzneo do kodu uruchomiania aplikacji
import ui_metoda
def FFT(x):
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    #ilość etapów  rosnie Log2(N)
    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    #N_min = min(N,32)
    #ustawia ile blok będzie przyjmować danych
    N_min = 2
    
    # Perform an O[N^2] DFT on all length-N_min sub-problems at once
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    #obliczenie pierwszej etapu
    #dot - mnożenie
    # reshape - tworzenie macierzy wiersz parzystych elementów , nieprzystych elementów
    # shape[0] - wierszowo , shape[1] - kolumnowo
    X = np.dot(M, x.reshape((N_min, -1)))
   	#wykonanie N etapów
    while X.shape[0] < N:
    	#parzysty X(k) gdzie k = 0,1,2,3,4, .... , N/2 -1
        X_even = X[:, :X.shape[1] / 2]
        #nieparzysty X(k + N/2) gdzie k = 0,1,2,3,4, .... , N/2 -1
        X_odd = X[:, X.shape[1] / 2:]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        #mnożenie macierzowe
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])
    #łączenie wierszy jedną całość
    return X.ravel()
def DFT(x):
    #Zwykła dyskretna transformata fouriera
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    #print np.dot(M,x)
    #mnożenie macierzowe
    return np.dot(M, x)
np.set_printoptions(precision=4)
class AudioIO():
	def __init__(self):
		#częstotliwośc próbkowania
		self.RATE = 44100
		#Buffor
		self.BUFFER = 1024
		#Format Dźwieku
		self.FORMAT = pyaudio.paInt32
		#kanały
		self.channels = 2
		#Konstruktor portu audio
		self.p = pyaudio.PyAudio()
		self.data = 0
		self.startFFT = False

	def setup(self,wf):
		self.wf = wf
		#Utworzenie strumienia
		self.stream = self.p.open(format=self.p.get_format_from_width(self.FORMAT),
            channels=self.channels,rate=self.RATE,output=True,start=False,stream_callback=self.callback,frames_per_buffer=self.BUFFER)
	def Play(self):
		self.stream.start_stream()
		self.startFFT = True
	def stop(self):
		self.p.close(self.stream)
        time.sleep(0.1)
        #self.startFFT = False
	def callback(self,in_data, frame_count, time_info, status):    
		self.data = self.wf.readframes(frame_count)
		#Przekonwertowanie Stringa na int typu int16 czyli 2**32
		#self.fft(dateInt)
		return (self.data, pyaudio.paContinue)
	#Transformata Fouriera
	def fft(self):
		if self.data == 0:
	 		data = np.zeros((2048,),dtype=float)
	 	else:
			data = np.fromstring(self.data,dtype=np.int16)
		#zakres częstotliwości 0 do 25 Khz
		x = np.arange(self.BUFFER/2,dtype=int)
		# od 0 do 512 elementów self.RATE = MAX częstotliwość pasma , self.BUFFER - max buffer ilość elementów 
		x = x*(self.RATE/self.BUFFER)
		left,right = np.split(np.abs(FFT(data)),2)
		#Dodawania liczby rzeczywistej i liczby urujonej y = R+Zj
		y=np.add(left,right[::-1])
		#20log10(y) = decybel gdzie a,b > 0 loga(b)
		if self.data != 0:
			y=np.multiply(20,np.log10(y))
		#określenie którą częstotliwość wyświetlać na wykresie	
		x = x[0:len(x):10]
		y = y[0:len(y):10]
		#ustawienie danych do wykresu
		plot.qwtPlot.setAxisTitle(Qwt.QwtPlot.xBottom, 'Hz')
		plot.qwtPlot.setAxisTitle(Qwt.QwtPlot.yLeft, 'dB')
		type_plot.setData(x, y)
		#Odświerzanie wykresu kasowanie ponowne rysowanie
		plot.qwtPlot.replot() 
		#print self.y

#Funkcje do przycisków		
def file_open():
    #Wyświetlenie okiena do wyboru pliku
    fd = QtGui.QFileDialog()
    #pobranie scieżki do pliku
    filename = fd.getOpenFileName()
    from os.path import isfile
    #Sprawdzenie czy plik istenieje
    if isfile(filename):
        #zapisanie scieżki do stringa
        print str(filename)
        wf = wave.open(str(filename),"rb")
        audio.setup(wf)

def Play_music():
	audio.Play()
def Stop_music():
	audio.stop()




#bezporśredni moduł ma wartość __main__
if __name__ == "__main__":
	#Stworzenie obiektu aplikacji oraz odwoływanie od argumentów
	app = QtGui.QApplication(sys.argv)
    #Tworzymy Okno po prze inicjację
	win_plot = ui_metoda.QtGui.QMainWindow()
    #odwołanie do klasy skrót main_ui.Ui_Form()
	plot =  ui_metoda.Ui_MainWindow()
    #odwołanie do funkcji
	plot.setupUi(win_plot)
    #tutaj dajemy włane połączenie slotów połączenie przycisków
	plot.openFile.clicked.connect(file_open)
	plot.play.clicked.connect(Play_music)
	plot.stop.clicked.connect(Stop_music)
	audio = AudioIO()
	#Ustawiamy QWtPlot (konstruktor funkcji - typ Funkcji)
	type_plot=Qwt.QwtPlotCurve()
	#Ustawienie Stylu wykresu
	type_plot.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,QtGui.QBrush(),QtGui.QPen(QtGui.QColor(255,0,0)),QtCore.QSize(7, 7)))
	plot.qwtPlot.setAxisScale(Qwt.QwtPlot.yLeft,0,160)
	#dołączenie obiektu do qwtPlot
	type_plot.attach(plot.qwtPlot)
    #Licznik czasu 
	plot.timer = QtCore.QTimer()
	#Prędkość przesuwania funkcji , licznik , czas odświeżania obrazu lub dźwięku
	plot.timer.start(10.0)
	#Połączenie Licznika z daną funkcja
	win_plot.connect(plot.timer,QtCore.SIGNAL('timeout()'),audio.fft)
	#win_plot.connect(plot.timer,QtCore.SIGNAL('timeout()'),fft)
	#Wyświetlenie obiektu
	win_plot.show()
	#Czyste Zamknięcie aplikacji
	sys.exit(app.exec_())
    

