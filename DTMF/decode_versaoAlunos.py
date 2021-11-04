#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import sys
import time
from suaBibSignal import *
import peakutils

#funcao para transformar intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    signal = signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    freqDeAmostragem = 44100
    fs = freqDeAmostragem
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = freqDeAmostragem #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 5 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera

    n = 3
    print("A captação irá começar em {} segundos.".format(str(n)))
    time.sleep(n)
    
    #faca um print informando que a gravacao foi inicializada
    print("A gravação foi inicializada.")
    
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = freqDeAmostragem*duration
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")

    y = audio[:,0]
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    print(audio)
    #grave uma variavel com apenas a parte que interessa (dados)
    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    inicio  = 0
    fim = 5
    numPontos = duration*fs
    t = np.linspace(inicio,fim,numPontos)

    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(y, fs)

    index = peakutils.indexes(yf,0.3,100)
    print("-----------index:", index)

    freq_l = []
    freq_l_y = []
    for i in index:
        freq_pico = xf[i]
        print('yfi',yf[i])
        freq_l.append(freq_pico)
        freq_l_y.append(yf[i])
    tecla_obtida = None
    for f in freq_l:
        if 1200 <=f<=1220:
            for i in freq_l:
                if 687<=i<=707:
                    tecla_obtida = 1
        elif 1326 <= f <= 1346:
            for i in freq_l:
                if 687<=i<=707:
                    tecla_obtida = 2
        elif 1467 <= f <= 1487:
            for i in freq_l:
                if 687<=i<=707:
                    tecla_obtida = 3
        elif 1200 <=f<=1220:
            for i in freq_l:
                if 760<=i<=780:
                    tecla_obtida = 4
        elif 1326 <= f <= 1346:
            for i in freq_l:
                if 760<=i<=780:
                    tecla_obtida = 5
        elif 1467 <= f <= 1487:
            for i in freq_l:
                if 760<=i<=780:
                    tecla_obtida = 6
        elif 1200 <=f<=1220:
            for i in freq_l:
                if 842<=i<=862:
                    tecla_obtida = 7
        elif 1326 <= f <= 1346:
            for i in freq_l:
                if 842<=i<=862:
                    tecla_obtida = 8
        elif 1467 <= f <= 1487:
            for i in freq_l:
                if 842<=i<=862:
                    tecla_obtida = 9
        elif 1326 <= f <= 1346:
            for i in freq_l:
                if 931<=i<=951:
                    tecla_obtida = 0
    print('Tecla obtida: ', tecla_obtida)

    # plot do gráfico áudio vs tempo!
    plt.figure("Audio X Tempo")
    plt.plot(y,t)
    plt.grid()
    plt.title('Áudio por tempo')

    # plot do gráfico Fourier!
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    
    print("-----------frequências de pico:", freq_l)

    
   
    
    
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
