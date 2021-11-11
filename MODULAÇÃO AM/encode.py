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

    sinal = signalMeu()

    # 1) Fazer leitura do arquivo .wav
    data, fs = sf.read('oie.wav')

    # 2) Normalização do sinal
    data_normalizada = data/max(data)
    time = np.linspace(0,3,len(data_normalizada))
    plt.figure("Figure 1")
    plt.plot(time,data_normalizada)
    plt.title("Sinal de áudio original normalizado")
    
    # 3) Filtro das frequências acima de 4kHz
    data_filtrada = LPF(data_normalizada, 4000, fs)

    time = np.linspace(0,3,len(data_filtrada))
    plt.figure("Figure 2")
    plt.plot(time,data_filtrada)
    plt.title("Sinal de áudio filtrado pelo tempo")

    sinal.plotFFT(data_filtrada, fs)

    # 4) Reprodução do sinal
    sd.play(data_filtrada, fs)
    sd.wait()

    # 5) Mudulação do sinal com portadora de 14kHz
    x,y = sinal.generateSin(14000, 1, 3, fs)
    x = x[0:len(data_filtrada)]
    y = y[0:len(data_filtrada)]

    data_modulada = y*data_filtrada
    time = np.linspace(0,3,len(data_modulada))
    plt.figure("Figure 4")
    plt.plot(time,data_modulada)
    plt.title("Áudio Modulado pelo Tempo")

    sinal.plotFFT(data_modulada, fs)

    sf.write("oie_modulado.wav", data_modulada, fs)

    #6) Ouvindo o áudio modularizado
    sd.play(data_modulada, fs)
    sd.wait()

    plt.show()


if __name__ == "__main__":
    main()
