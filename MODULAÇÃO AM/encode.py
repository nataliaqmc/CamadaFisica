#importe as bibliotecas
import numpy as np
from scipy.signal.filter_design import freqs_zpk
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import sys
from suaBibSignal import *
from funcoes_LPF import *
import wave

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():

    # 1) Fazer leitura do arquivo .wav
    data, fs = sf.read('oie.wav')

    # 2) Normalização do sinal
    data_filtrada = data/max(data)

    # 3) Filtro das frequências acima de 4kHz
    data_filtrada = LPF(data_filtrada, 4000, fs)

    # 4) Reprodução do sinal
    sd.play(data_filtrada, fs)
    sd.wait()

    # 5) Mudulação do cinal com portadora de 14kHz
    sinal = signalMeu()
    seno = sinal.generateSin(14000, 0.3, 5, fs)
    data_modularizada = data_filtrada*seno


    # 6) Ouvindo o áudio modularizado
    sd.play(data_modularizada, fs)
    sd.wait()


if __name__ == "__main__":
    main()
