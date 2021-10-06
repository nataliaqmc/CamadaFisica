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
from datetime import datetime
serialName = "COM6"
#serialName = "/dev/cu.usbmodem141401"                  # Windows(variacao de)

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
    logs = open(f'PROTOCOLO DE COMUNICAÇÃO UART PONTO A PONTO/logs/Server{n_situacao}.txt', 'w')
    for log in lista_logs:
      logs.write('%s\n' % log)
    logs.close()

def main():
    try:
        com1 = enlace(serialName)
        com1.enable()

        print("Comunicação aberta com sucesso")
        print('A recepção vai começar')
        
        vivo,n = com1.getData(14)
        lista_logs.append(cria_log(vivo, 'recebimento'))

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
        vivo = head + eop
        print('Recebeu os dados para confirmação!')
        #com1.sendData(vivo)
        #lista_logs.append(cria_log(vivo, 'envio'))
            
        print('Pronto para receber os pacotes!')
        numero = 1
        timer_inicio = time.time()
        while numero <= vivo[3]:
            pacote, tPacote = com1.getData(10)
            lista_logs.append(cria_log(pacote, 'recebimento'))
            pacote2, tPacote2 = com1.getData(pacote[5] + 4)
            lista_logs.append(cria_log(pacote2, 'recebimento'))
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
            time.sleep(1)
            if (numero == pacote[4]) and (pacote2[-4:] == eop) and ((len(pacote2)-4) == pacote[5]) and (pacote[7]==numero-1) and (time.time() - timer_inicio < 20):
                envioConfirmacao =( b'\x04' + pacote[1:] + eop)
                print('Dados sendo enviados: ', envioConfirmacao)
                #com1.sendData(envioConfirmacao)
                lista_logs.append(cria_log(envioConfirmacao, 'envio'))
                numero += 1
                print('Pacote recebido com sucesso!')
                print('-----------------------------------------------')
                print(' ')
                timer_inicio = time.time()
            elif time.time() - timer_inicio > 20 or pacote == b'\x00':
                envioErro = ( b'\x05'+pacote[1:] + eop)
                com1.sendData(envioErro)
                lista_logs.append(cria_log(envioErro, 'envio'))
                cria_arquivo_logs(lista_logs, 3)
                print("-------------------------")
                print("Comunicação encerrada por time out")
                print("-------------------------")
                com1.disable()
                break
            else:
                envioErro = ( b'\x06'+pacote[1:] + eop)
                com1.sendData(envioErro)
                lista_logs.append(cria_log(envioErro, 'envio'))
                print('Erro ao receber o pacote ',numero,': ', envioErro)
        
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        cria_arquivo_logs(lista_logs, 3)
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
