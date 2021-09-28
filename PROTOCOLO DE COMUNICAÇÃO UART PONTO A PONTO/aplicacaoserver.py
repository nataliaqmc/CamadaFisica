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
serialName = "COM6"
#serialName = "/dev/cu.usbmodem141401"                  # Windows(variacao de)

def main():
    try:

        com1 = enlace(serialName)
        com1.enable()

        print("Comunicação aberta com sucesso")
        print('A recepção vai começar')

        vivo,n = com1.getData(14)

        head = ((2).to_bytes(1, byteorder='big')
            + vivo[1].to_bytes(1, byteorder='big')
            + vivo[2].to_bytes(1, byteorder='big')
            + vivo[3].to_bytes(1, byteorder='big')
            + vivo[4].to_bytes(1, byteorder='big')
            + vivo[5].to_bytes(1, byteorder='big')
            + vivo[6].to_bytes(1, byteorder='big')
            + vivo[7].to_bytes(1, byteorder='big')
            + vivo[8].to_bytes(1, byteorder='big')
            + vivo[9].to_bytes(1, byteorder='big'))

        eop = (b'\xff' b'\xaa' b'\xff' b'\xaa')
        vivo = head+eop

        print('Recebeu os dados para confirmação!')
        com1.sendData(vivo)

        print('Pronto para receber os pacotes!')
        numero = 1
        
        while numero <= vivo[3]:
            pacote, tPacote = com1.getData(10)
            pacote2, tPacote2 = com1.getData(pacote[5] + 4)
            print('Head do pacote atual: ', pacote)
            print('Tipo de mensagem recebida: ', pacote[0])
            print('Id do sensor: ', pacote[1])
            print('Id do servidor: ', pacote[2])
            print('Número total de pacotes do arquivo: ', pacote[3])
            print('Número do pacote sendo recebido: ', pacote[4])
            print('Tamanho do payload: ', pacote[5])
            print('Pacote solicitado para recomeço quando a erro no envio: ',pacote[6])
            print('Ultimo pacote recebido com sucesso: ', pacote[7])
            print('CRC h8: ', pacote[8])
            print('CRC h9: ', pacote[9])
            if (numero == pacote[4]) and (pacote2[-4:] == eop) and ((len(pacote2)-4) == pacote[5]) and (pacote[7]==numero-1):
                envioConfirmacao =( b'\x04' + pacote[1:] + eop)
                print('Dados sendo enviados: ', envioConfirmacao)
                com1.sendData(envioConfirmacao)
                numero += 1
                print('Pacote recebido com sucesso!')
                print('-----------------------------------------------')
                print(' ')
            else:
                envioErro = ( b'\x06'+pacote[1:] + eop)
                com1.sendData(envioErro)
                print('Erro ao receber o pacote ',numero,': ', envioErro)
        
    
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
