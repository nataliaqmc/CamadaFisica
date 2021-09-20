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
serialName = "COM5"                  # Windows(variacao de)

def main():
    try:

        com1 = enlace('COM5')
        
        com1.enable()

        print("Comunicação aberta com sucesso")
        '''txBuffer = open(imageR, 'rb').read()
        
        print(colored("txBuffer",'yellow'),txBuffer)
          
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        nRx = len(txBuffer)
        print(colored(('Quantos bytes serão enviados: ',nRx),'cyan'))
       
        print(colored("A comunicação irá começar!",'red'))
        
        com1.sendData(np.asarray(txBuffer))
       
        
        txSize = com1.tx.getStatus()
        print("txSize = ",txSize)'''
        
        print('A recepção vai começar')
        ganhei = False
        while not ganhei:
            rxBuffer, nRx = com1.getData(1)
            #print('aqui')
            time.sleep(0.1)
            if rxBuffer:
                ganhei = True
        #txLen = int.from_bytes(rxBuffer[0],byteorder='little')
        
        #print(rxBuffer)
        #Recebendo o tamanho dos dados:
        print('txLen = ', rxBuffer[0])

        #Recebendo os dados:
        rxBuffer, nRx = com1.getData(rxBuffer[0]-1)
        print(rxBuffer)
        print('nrx',nRx)

        listaBytesRx = str(rxBuffer)
        listaBytesRx = listaBytesRx.split('x')
        #print(listaBytesRx)
        
        c = 0
        resultado_final = []
        while c<len(listaBytesRx):
            if listaBytesRx[c]=='f0\\':
                resultado_final.append('F0')
            elif listaBytesRx[c]=='ff\\':
                resultado_final.append('FF')
            elif listaBytesRx[c]=='00\\':
                resultado_final.append('00')
            elif listaBytesRx[c]=='0f\\':
                resultado_final.append('0F')
            elif listaBytesRx[c]=='bb\\':
                resultado_final[-1]+=listaBytesRx[c+1].upper()[:2]
                c+=1
            else:
                if listaBytesRx[c] != "b'\\":
                    resultado_final.append(listaBytesRx[c].upper()[:2])
            c+=1
        print('resultado final',resultado_final)

        #f = open(imageW,'wb')
        #f.write(rxBuffer)
        #f.close()

        print(rxBuffer)
        print("recebeu {}" .format(rxBuffer))
            
    
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
