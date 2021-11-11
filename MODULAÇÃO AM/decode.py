#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import sys
import time
from suaBibSignal import *
import peakutils
from funcoes_LPF import *

#funcao para transformar intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
 
    sinal = signalMeu()

    data, fs = sf.read('oie_modulado.wav')
    print("fs:",fs)

    x,y = sinal.generateSin(14000, 1, 5, fs)
    x = x[0:len(data)]
    y = y[0:len(data)]

    data_demodulada = data*y
    sinal.plotFFT(data_demodulada, fs)

    #sd.play(data_demodulada, fs)
    #sd.wait()

    data_filtrada = filtro(data_demodulada, fs, 4000)

    sinal.plotFFT(data_filtrada, fs)
    sd.play(data_filtrada, fs)
    sd.wait()


    
    plt.show()

if __name__ == "__main__":
    main()
