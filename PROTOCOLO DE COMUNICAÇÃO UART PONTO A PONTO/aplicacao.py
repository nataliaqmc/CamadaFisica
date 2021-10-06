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
from crc import CrcCalculator, Crc8
from datetime import datetime

#serialName = "COM5"
serialName = "/dev/cu.usbmodem141201"                  # Windows(variacao de)

arquivo = 'imgrecebida.png'
eop = (b'\xff' b'\xaa' b'\xff' b'\xaa')
def readArquivo(arquivo):
    txBuffer = open(arquivo, 'rb').read()
    n = 114
    split_txBuffer = [txBuffer[i:i+n] for i in range(0, len(txBuffer), n)]
    return split_txBuffer


lista_logs = []

def cria_log(mensagem, envio_ou_recebimento):
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
    envio_ou_recebimento = envio_ou_recebimento
    tipo_msg = mensagem[0]
    tamanho_total = len(mensagem)
    if tipo_msg == 3:
        id_pacote_enviado = mensagem[4]
        total_pacotes_arquivo = mensagem[3]
        crc = str(mensagem[8:10]).upper()
        crc = crc[4:6] + crc[8:10]
        log = f'{time} / {envio_ou_recebimento} / {tipo_msg} / {tamanho_total} / {id_pacote_enviado} / {total_pacotes_arquivo} / {crc}'
    else:
        id_pacote_enviado = ''
        total_pacotes_arquivo = ''
        crc = ''
        log = f'{time} / {envio_ou_recebimento} / {tipo_msg} / {tamanho_total}'
    return log

def cria_arquivo_logs(lista_logs: list, n_situacao: int):
    logs = open(f'logs/Client{n_situacao}.txt', 'w')
    for log in lista_logs:
      logs.write('%s\n' % log)
    logs.close()

def datagrama(idSensor, idServidor, split_txBuffer,crc):
    global eop

    total_pacotes = len(split_txBuffer)
    n_pacote = 1
    tipoDeMensagem = 3
    pacoteErroRecomeco = 1
    ultimoPacoteRecebido = 0

    lista_pacotes_a_serem_enviados = []
    for payload in split_txBuffer:
        checksum = int.to_bytes(crc.calculate_checksum(payload), 2, byteorder="big")
        h5 = len(payload)
        h8 = int.to_bytes(checksum[0], 1, byteorder="big")
        h9 = int.to_bytes(checksum[0], 1, byteorder="big")
        head = (tipoDeMensagem.to_bytes(1, byteorder='big')
            + idSensor.to_bytes(1, byteorder='big')
            + idServidor.to_bytes(1, byteorder='big')
            + total_pacotes.to_bytes(1, byteorder='big')
            + n_pacote.to_bytes(1, byteorder='big')
            + h5.to_bytes(1, byteorder='big')
            + pacoteErroRecomeco.to_bytes(1, byteorder='big')
            + ultimoPacoteRecebido.to_bytes(1, byteorder='big')
            + h8
            + h9)
        n_pacote += 1
        pacoteErroRecomeco = n_pacote
        ultimoPacoteRecebido += 1
        pacote = head + payload + eop
        lista_pacotes_a_serem_enviados.append(pacote)
        
    print(colored(('LISTA DOS PACOTES A SEREM ENVIADOS: ',
          lista_pacotes_a_serem_enviados),'yellow'))

    
    
    return lista_pacotes_a_serem_enviados


def main():
    try:

        com1 = enlace(serialName)
        com1.enable()
        print("Comunicação aberta com sucesso")

        # INICIANDO O HANDSHAKE:
        global eop
        split_txBuffer = readArquivo(arquivo)
        n_pacote = 0
        total_pacotes = len(split_txBuffer)
        #crc = random.randint(1,100)
        tipoDeMensagem = 1 #Handshake
        idSensor = random.randint(1,100)  # ID arbitrário
        idServidor = random.randint(1,100)  # ID arbitrário
        idArquivo = random.randint(1,100)
        pacoteErroRecomeco = 0
        ultimoPacoteRecebido = 0
        payload_vazio = b'\x00'

        crc_calculator = CrcCalculator(Crc8.CCITT)
        checksum = int.to_bytes(crc_calculator.calculate_checksum(payload_vazio), 2, byteorder="big")
        print('-----CRC Calculator',crc_calculator)
        print('-----Checksum',checksum[0])
        h8 = int.to_bytes(checksum[0], 1, byteorder="big")
        h9 = int.to_bytes(checksum[0], 1, byteorder="big")
        print('-----h8,h9',h8,',',h9)
        head = (tipoDeMensagem.to_bytes(1, byteorder='big') + idSensor.to_bytes(1, byteorder='big')
                + idServidor.to_bytes(1, byteorder='big') + total_pacotes.to_bytes(1, byteorder='big')
                + n_pacote.to_bytes(1, byteorder='big') + idArquivo.to_bytes(1, byteorder='big')
                + pacoteErroRecomeco.to_bytes(1, byteorder='big') + ultimoPacoteRecebido.to_bytes(1, byteorder='big')
                + h8 + h9)

        pacoteHandshake = head + eop

        # ENVIANDO O HANDSHAKE:
        print(colored(('Pacote Handshake: ', pacoteHandshake),'magenta'))
        print('Enviando um datagrama para conferir se o servidor está ligado!')
        com1.sendData(pacoteHandshake)
        lista_logs.append(cria_log(pacoteHandshake, 'envio'))
        pergunta, tamanho = com1.getData(14)
        lista_logs.append(cria_log(pergunta, 'recebimento'))
        

        # Conferindo se o servidor está rodando:
        print('Resposta recebida: ', pergunta)
        while pergunta == 'Não rodou':
            resposta = input('Servidor inativo. Tentar novamente? S/N: ')
            if resposta == 'S':
                com1.sendData(pacoteHandshake)
                lista_logs.append(cria_log(pacoteHandshake, 'envio'))
                pergunta, tamanho = com1.getData(14)
                lista_logs.append(cria_log(pergunta, 'recebimento'))
            else:
                break

        if pergunta != 'Não rodou':
            lista_pacotes_a_serem_enviados = datagrama(idSensor,idServidor,split_txBuffer,crc_calculator)
            for pacote in lista_pacotes_a_serem_enviados:
                print('Sending Pacote')
                com1.sendData(pacote)
                lista_logs.append(cria_log(pacote, 'envio'))
                com1.sendData(pacote)
                lista_logs.append(cria_log(pacote, 'envio'))
                confirmacao, t = com1.getData(14)
                lista_logs.append(cria_log(confirmacao, 'recebimento'))
                timer_inicio = time.time()

                while (confirmacao[1:10] != pacote[1:10]):
                    if time.time() - timer_inicio > 20:
                        envioErro = ( b'\x05'+confirmacao[1:] + eop)
                        com1.sendData(envioErro)
                        lista_logs.append(cria_log(envioErro, 'envio'))
                        # Encerra comunicação
                        print("-------------------------")
                        print("Comunicação encerrada por time out")
                        print("-------------------------")
                        com1.disable()
                        cria_arquivo_logs(lista_logs, 1)
                    print('Repetindo o envio do pacote!')
                    print(confirmacao[1:10], ' != ', pacote[1:10])
                    com1.sendData(pacote)
                    com1.sendData(pacote)
                    lista_logs.append(cria_log(pacote, 'envio'))
                    confirmacao, t = com1.getData(14)
                    lista_logs.append(cria_log(confirmacao, 'recebimento'))
            
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

        cria_arquivo_logs(lista_logs, 1)

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
