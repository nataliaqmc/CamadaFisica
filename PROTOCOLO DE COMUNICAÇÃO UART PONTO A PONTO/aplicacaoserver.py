#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from enlaceserver import *
import time
import numpy as np
from termcolor import colored
import random
#serialName = "COM6"
serialName = "/dev/cu.usbmodem141401"                  # Windows(variacao de)

def main():
    try:

        com1 = enlace(serialName)
        
        com1.enable()


        print("Comunicação aberta com sucesso")
        print('A recepção vai começar')
        vivo,n = com1.getData(14)

        tipo=2
        tipoDeMensagem = tipo.to_bytes(1, byteorder='big')
        idSensor = vivo[1]
        idServidor = vivo[2]
        total_pacotes  = vivo[3]
        n_pacote = vivo[4]
        h5 = vivo[5]
        pacoteErroRecomeco = vivo[6]
        ultimoPacoteRecebido = vivo[7]
        h8 = vivo[8]
        h9 = vivo[9]

        head = (tipoDeMensagem
                + idSensor
                + idServidor
                + total_pacotes
                + n_pacote
                + h5
                + pacoteErroRecomeco
                + ultimoPacoteRecebido
                + h8
                + h9)

        eop = (b'\xFF' b'\xAA' b'\xFF' b'\xAA')

        vivo = head+eop
        print('Recebeu os dados d confirmação!')
        #quantPacotes = int.from_bytes(vivo[6:9], 'big')
        com1.sendData(vivo)
        
        print('Pronto para receber os pacotes!')

        numero = 1
        
        """while numero <= quantPacotes:
            pacote, tPacote = com1.getData(10)
            pacote2, tPacote2 = com1.getData(int.from_bytes(pacote[0:3], 'big') + 4)
            print('Tamanho do pacote atual: ', int.from_bytes(pacote[0:3], 'big'))
            print('Número do pacote atual: ', int.from_bytes(pacote[3:6], 'big'))
            print('Quantidades de pacotes a serem recebidos: ', int.from_bytes(pacote[6:9], 'big'))
            print('Datagrama recebido: ', pacote2)
            if numero == int.from_bytes(pacote[3:6], 'big') and pacote2[-4:] == (b'\x66' b'\x69' b'\x6d' b'\x21') and (len(pacote2)-4) == (int.from_bytes(pacote[0:3], 'big')):
                com1.sendData(pacote)
                numero += 1
                print('Pacote recebido com sucesso!')
            else:
                com1.sendData(b'/x00')
                print('Erro ao receber o pacote!')"""
        
    
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
