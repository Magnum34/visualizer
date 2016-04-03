#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import timeit
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
		
if __name__ == "__main__":
	x = np.random.random(1024)
	dft = DFT(x)
	setup = ''
	time_dft = timeit.Timer(lambda: DFT(x)).timeit(number=1)
	#print "DFT = ", dft
	fft =FFT(x)
	time_fft = timeit.Timer(lambda: FFT(x)).timeit(number=1)
	time_fft_lib = timeit.Timer(lambda: np.fft.fft(x)).timeit(number=1)
	print " DFT = ",time_dft, " us \n fft = ",time_fft," us \n fft lib = ", time_fft_lib," us "
	#print "fft = ", fft