#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from enlace import *
import time
import numpy as np
from termcolor import colored
import random

#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM6"                  # Windows(variacao de)

def sorteio():
    qnt_comandos = random.randint(10,30)
    print(qnt_comandos)
    comandos = ['00FF','00','0F','F0','FF00','FF']
    listaBytes = [b'\x00',b'\x0F', b'\xF0', b'\xFF', b'\xBB']
    i = 0
    resposta = []
    while i < qnt_comandos:
        j = random.randint(0,5)
        resposta.append(comandos[j])
        i +=1
    nova_resposta = [b'\00']
    for dado in resposta:
        if dado == comandos[0]:
            nova_resposta.append(listaBytes[0])
            nova_resposta.append(listaBytes[4])
            nova_resposta.append(listaBytes[3])
        elif dado == comandos[4]:
            nova_resposta.append(listaBytes[3])
            nova_resposta.append(listaBytes[4])
            nova_resposta.append(listaBytes[0])
        elif dado == comandos[1]:
            nova_resposta.append(listaBytes[0])
        elif dado == comandos[2]:
            nova_resposta.append(listaBytes[1])
        elif dado == comandos[3]:
            nova_resposta.append(listaBytes[2])  
        elif dado == comandos[5]:
            nova_resposta.append(listaBytes[3])
    print('Bytes enviados',nova_resposta[1:])

    tamanho = len(nova_resposta)
    nova_resposta[0] = (tamanho).to_bytes(1,'little')
    
    return np.asarray(nova_resposta)


def main():
    try:
        
        com1 = enlace('COM6')
        
        com1.enable()
        cronometro_inicio = time.perf_counter()
        cronometro_inicio
        print(cronometro_inicio)
        print("Comunicação aberta com sucesso")
        
        txBuffer = sorteio()
        print(colored("txBuffer",'yellow'),txBuffer)
          
       
        print(colored("A comunicação irá começar!",'red'))
        #bytes_send = t + txBuffer
        #print(bytes_send)
        #Mandando a quantidade de dados e os dados:  
        com1.sendData(txBuffer)

        print('A recepção vai começar')
      
        '''#acesso aos bytes recebidos
        txLen = len(txBuffer)
        print(colored('txLen','magenta'),txLen)

        rxBuffer, nRx = com1.getData(txLen)
        print(rxBuffer)
        f = open(imageW,'wb')
        f.write(rxBuffer)
        f.close()

        print(rxBuffer)
        print("recebeu {}" .format(rxBuffer))'''
            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
