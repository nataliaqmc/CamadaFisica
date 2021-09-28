#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


from enlace import *
import time
import numpy as np
from termcolor import colored
import random

serialName = "COM5"
#serialName = "/dev/cu.usbmodem141201"                  # Windows(variacao de)

arquivo = 'PROTOCOLO DE COMUNICAÇÃO UART PONTO A PONTO/imgrecebida.png'

def readArquivo(arquivo):
    txBuffer = open(arquivo, 'rb').read()
    n = 114
    split_txBuffer = [txBuffer[i:i+n] for i in range(0, len(txBuffer), n)]
    return split_txBuffer



def datagrama(idSensor, idServidor, split_txBuffer,crc):

    eop = (b'\xFF' b'\xAA' b'\xFF' b'\xAA')
    total_pacotes = len(split_txBuffer)
    n_pacote = 1
    tipoDeMensagem = 3
    pacoteErroRecomeco = 1
    ultimoPacoteRecebido = 0
    h8 = crc
    h9 = crc

    lista_pacotes_a_serem_enviados = []
    for payload in split_txBuffer:
        h5 = len(payload)
        head = (tipoDeMensagem.to_bytes(1, byteorder='big')
            + idSensor.to_bytes(1, byteorder='big')
            + idServidor.to_bytes(1, byteorder='big')
            + total_pacotes.to_bytes(1, byteorder='big')
            + n_pacote.to_bytes(1, byteorder='big')
            + h5.to_bytes(1, byteorder='big')
            + pacoteErroRecomeco.to_bytes(1, byteorder='big')
            + ultimoPacoteRecebido.to_bytes(1, byteorder='big')
            + h8.to_bytes(1, byteorder='big')
            + h9.to_bytes(1, byteorder='big'))
        n_pacote += 1
        pacoteErroRecomeco = n_pacote
        ultimoPacoteRecebido += 1
        pacote = head + payload + eop
        lista_pacotes_a_serem_enviados.append(pacote)
    print('LISTA DOS PACOTES A SEREM ENVIADOS: ',
          lista_pacotes_a_serem_enviados)
    return lista_pacotes_a_serem_enviados


def main():
    try:

        com1 = enlace(serialName)
        com1.enable()
        print("Comunicação aberta com sucesso")

        # INICIANDO O HANDSHAKE:
        split_txBuffer = readArquivo(arquivo)
        n_pacote = 0
        total_pacotes = len(split_txBuffer)
        crc = random.randint(1,100)
        tipoDeMensagem = 1 #Handshake
        idSensor = random.randint(1,100)  # ID arbitrário
        idServidor = random.randint(1,100)  # ID arbitrário
        idArquivo = random.randint(1,100)
        h5 = idArquivo
        pacoteErroRecomeco = 2
        ultimoPacoteRecebido = 0
        h8 = crc
        h9 = crc

        head = (tipoDeMensagem.to_bytes(1, byteorder='big') + idSensor.to_bytes(1, byteorder='big')
                + idServidor.to_bytes(1, byteorder='big') + total_pacotes.to_bytes(1, byteorder='big')
                + n_pacote.to_bytes(1, byteorder='big') + h5.to_bytes(1, byteorder='big')
                + pacoteErroRecomeco.to_bytes(1, byteorder='big') + ultimoPacoteRecebido.to_bytes(1, byteorder='big')
                + h8.to_bytes(1, byteorder='big') + h9.to_bytes(1, byteorder='big'))
        eop = (b'\xFF' b'\xAA' b'\xFF' b'\xAA')
        
        pacoteHandshake = head+eop

        print('Pacote Handshake: ', pacoteHandshake)
        print('Enviando um datagrama para conferir se o servidor está ligado!')
        com1.sendData(pacoteHandshake)
        pergunta, tamanho = com1.getData(14)

        # Conferindo se o servidor está rodando:
        print('Resposta recebida: ', pergunta)
        while pergunta == 'Não rodou':
            resposta = input('Servidor inativo. Tentar novamente? S/N: ')
            if resposta == 'S':
                com1.sendData(pacoteHandshake)
                pergunta, tamanho = com1.getData(14)
            else:
                break

        if pergunta != 'Não rodou':
            lista_pacotes_a_serem_enviados = datagrama(idSensor,idServidor,split_txBuffer,crc)
            for pacote in lista_pacotes_a_serem_enviados:
                print('Sending Pacote')
                com1.sendData(pacote)
                com1.sendData(pacote)
                confirmacao, t = com1.getData(14)
                while (confirmacao[1:10] != pacote[1:10]):
                    print('Repetindo o envio do pacote!')
                    print(confirmacao[1:10], ' != ', pacote[1:10])
                    com1.sendData(pacote)
                    com1.sendData(pacote)
                    confirmacao, t = com1.getData(14)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
