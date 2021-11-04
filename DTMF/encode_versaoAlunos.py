#importe as bibliotecas
import numpy as np
from scipy.signal.filter_design import freqs_zpk
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import sys
from suaBibSignal import *


"""elif resposta == "#":
    x = 1477 #Hz
    y = 941 #Hz
elif resposta == "A":
    x = 1633 #Hz
    y = 697 #Hz
elif resposta == "B":
    x = 1633 #Hz
    y = 770 #Hz
elif resposta == "C":
    x = 1633 #Hz
    y = 852 #Hz
elif resposta == "D":
    x = 1209 #Hz
    y = 941 #Hz
elif resposta == "X":
    x = 1209 #Hz
    y = 941 #Hz"""



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


    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array
    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    NUM = input("Escolha um número entre 0 e 9:")

    if NUM == "1":
        freq_x = 1209 #Hz
        freq_y = 697 #Hz
    elif NUM == "2":
        freq_x = 1336 #Hz
        freq_y = 697 #Hz
    elif NUM == "3":
        freq_x = 1477 #Hz
        freq_y = 697 #Hz
    elif NUM == "4":
        freq_x = 1209 #Hz
        freq_y = 770 #Hz
    elif NUM == "5":
        freq_x = 1336 #Hz
        freq_y = 770 #Hz
    elif NUM == "6":
        freq_x = 1477 #Hz
        freq_y = 770 #Hz
    elif NUM == "7":
        freq_x = 1209 #Hz
        freq_y = 852 #Hz
    elif NUM == "8":
        freq_x = 1336 #Hz
        freq_y = 852 #Hz
    elif NUM == "9":
        freq_x = 1477 #Hz
        freq_y = 852 #Hz
    elif NUM == "0":
        freq_x = 1336 #Hz
        freq_y = 941 #Hz

    tb, x = sinal.generateSin(freq_x, gainX, duration, fs)
    tb, y = sinal.generateSin(freq_y, gainY, duration, fs)

    #nao aceite outro valor de entrada.
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    tone = x+y

    
    #printe o grafico no tempo do sinal a ser reproduzido
    sinal.plotFFT(tone, fs)

    # reproduz o som
    sd.play(tone, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
