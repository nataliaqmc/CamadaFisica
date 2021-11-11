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


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    sinal = signalMeu()

    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    duration = 5 #tempo em segundos que ira emitir o sinal acustico 
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3

    
    freq_x = 20000 #Hz
    freq_y = 4000 #Hz

    tb, x = sinal.generateSin(freq_x, gainX, duration, fs)
    tb, y = sinal.generateSin(freq_y, gainY, duration, fs)


    #nao aceite outro valor de entrada.
    print("Gerando Tom")
    
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    tone = x+y

    sf.write("input.wav", tone, fs)

if __name__ == "__main__":
    main()