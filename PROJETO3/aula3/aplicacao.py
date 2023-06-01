#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("esperando 1 byte de sacrifício")
        
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
    
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        

        #Inicio do recebimento de pacotes
        time.sleep(1)
        rxBuffer, nRx = com1.getData(65)
        print("HANDSHAKE")
        print(rxBuffer)

        if rxBuffer[0]==1:
            print("RESPOSTA PARA O CLIENT")
            string_handshake = "01"+64*"00"
            com1.sendData(bytearray.fromhex(string_handshake))

        #PRIMEIRO PACOTE
        eof_r = bytearray.fromhex("AA AA AA")
        rx_write = bytearray.fromhex("")
        ind_a=-1

        rxBuffer, nRx = com1.getData(12)


        for i in range(0,rxBuffer[0]-1):
           time.sleep(1)
           if ind_a == -1:
            ind_a_r = rxBuffer[1]
            pyload, nRx = com1.getData(rxBuffer[2] )
            eop, nRx = com1.getData(3)
            print("ENTREI AQUI")
            if ind_a_r==ind_a+1:
                    if eop==eof_r:
                        rx_write+=pyload
                        string_resposta = "AA"+64*"00"
                        com1.sendData(bytearray.fromhex(string_resposta))
                        ind_a=ind_a_r
                        print(ind_a_r)
                    else:
                        print("O TAMANHO DO PAYLOAD INFORMADO NÃO CORRESPONDE AO TAMNAHO REAL")
                        break
            elif ind_a_r != ind_a+1:
                print(f"O PACOTE {ind_a_r} veio fora da ordem")   
                break             

           if ind_a != -1:
            rxBuffer,nRx = com1.getData(12)
            ind_a_r = rxBuffer[1]
            pyload, nRx = com1.getData(rxBuffer[2])
            eop, nRx = com1.getData(3)
            if ind_a_r==ind_a+1:
                if eop==eof_r:
                    rx_write+=pyload
                    string_resposta = "AA"+64*"00"
                    com1.sendData(bytearray.fromhex(string_resposta))
                    ind_a=ind_a_r
                    print(ind_a_r)
                    print(len(rx_write))
                else:
                   print( "O TAMANHO DO PAYLOAD NÃO CORRESPONDE AO INFORMADO NA HEAD")
            elif ind_a_r != ind_a+1:
                print(f"O PACOTE {ind_a_r} veio fora da ordem")
        imageW = "./img/recebida.jpg"
        f = open(imageW,'wb')
        f.write(rx_write)
        f.close()

                
               




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
