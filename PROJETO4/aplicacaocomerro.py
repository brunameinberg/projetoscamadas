#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
from time import *
import numpy as np
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        print("-------------------------")
        print("enviando byte de sacrificio")
        print("-------------------------")
        com1.enable()
        sleep(.2)
        com1.sendData(b'00')
        sleep(1)

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        #PACOTE HANDSHAKE
        #o primeiro pacote a ser enviado é somente o handshake, para considerar somente o primeiro byte como 1

        inicia = False

        #lendo a imagem
        imageR = 'img/cararetoironman.jpg'
        txBuffer = open(imageR, 'rb').read()
        numerodepacotes = int((len(txBuffer)) // 114) #quantidade de pacotes
        numerorestantedepacotes = int((len(txBuffer)) % 114)
        numerodepacotesembytes = (numerodepacotes + 1).to_bytes(1, byteorder = 'big')
        eop = bytearray.fromhex('AA'+'BB'+'CC'+'DD')
        print(f"quantidade de pacotes {numerodepacotes}")
        print(f"numero final de bytes pacote final {numerorestantedepacotes}")
        print(f"tamanho da imagem: {len(txBuffer)}")
        handshake = '01' + '13' + '00' +  '5C'  + '00' + '2d' + '00' + '00' +  '00' + '00' + 'AA'+'BB'+'CC'+'DD'
        handshake = (bytearray.fromhex(handshake))
        print(f"handshake: {handshake}")
        tentativadeerro = False

        #abrindo arquivos para escrita
        f1 = open("f1.txt",  "a")
        f2 = open("f2.txt",  "a")
        f3 = open("f3.txt",  "a")
        f4 = open("f4.txt",  "a")


        #envia handshake
        com1.sendData(handshake) 
        linhaarquivo = str(ctime(time())) + '/' + 'envio' + '/' + '1' +  '/' + '14' + '\n'
        print(linhaarquivo)
        f1.write(linhaarquivo)
        


        while com1.rx.getBufferLen() < 1:
            sleep(5)
            break

        while com1.rx.getIsEmpty():
             sleep(1)
             timerhandshake = time()
        
             if (timerhandshake - time()) > 5:
                mensagemtimeout = b'x/05' + b'/x00'*9 + eop
                com1.sendData(mensagemtimeout)   
                com1.disable()
                break
                
        rxBuffer, nRx = com1.getData(14)
        print(f"resposta do servidor: {rxBuffer}")
        linhaarquivo = str(ctime(time())) + '/' + 'receb' + '/' + '1' +  '/' + '14' + '\n'
        f1.write(linhaarquivo)

        


        if len(rxBuffer) == 14: 

            print("recebeu {} bytes" .format(len(rxBuffer)))
            print("-------------------------")

            if rxBuffer[0]== 2:
                print("HANDSHAKE")
                inicia = True
            
            if rxBuffer[0]== 4:
                print("nao é o handshake")
                inicia = True
        

        maiscentoequatorze = 0   
        timer1 =  time()
        timeout = False

        j = 1
        while j <= numerodepacotes:
            print(f"j : {j}")

            if j == 90:
                 qualpacoteembytes = (90).to_bytes(1, byteorder='big')
                 tamanhopayloadpacote = (83).to_bytes(1, byteorder = 'big')
                 head = bytearray.fromhex('03' + '13' + '00') + qualpacoteembytes + qualpacoteembytes + tamanhopayloadpacote + bytearray.fromhex('00' + '00') + bytearray.fromhex('00' + '00')
                 payload = txBuffer[(10259) : (10342)] #porção da imagem que será enviada
                 eop = bytearray.fromhex('AA'+'BB'+'CC'+'DD')
                 com1.sendData(head+ payload + eop)
                 print("enviando pacote final")
                 print(f"pacote sendo enviado: {head + payload + eop}")
                 print(f"tamanho do pacote sendo enviado {len(head + payload + eop)}")
                 rxBuffer, nRx = com1.getData(14)
                 print(f"resposta do servidor: {rxBuffer}")
                 linhaarquivo = str(ctime(time())) + '/' + 'envio' + '/' + '3' +  '/' + '83' +  '/' + "90" + '\n'
                 j = j + 1
                 f1.write(linhaarquivo)
                 f2.write(linhaarquivo)
                 f3.write(linhaarquivo)
                 f4.write(linhaarquivo)
            
            #forçando o erro
            
            if j == 2 and tentativadeerro is False:
                qualpacoteembytes = (3).to_bytes(1, byteorder='big')
                tamanhopayloadpacote = (len(txBuffer[(maiscentoequatorze) : (maiscentoequatorze) + 114])).to_bytes(1, byteorder = 'big')
                head = bytearray.fromhex('03' + '13' + '00') + numerodepacotesembytes + qualpacoteembytes + tamanhopayloadpacote + bytearray.fromhex('00' + '00') + bytearray.fromhex('00' + '00')
                payload = txBuffer[(maiscentoequatorze) : (maiscentoequatorze) + 114] #porção da imagem que será enviada
                eop = bytearray.fromhex('AA'+'BB'+'BB'+'DD')
                com1.sendData(head + payload + eop)
                print(f"enviando pacote : {3} PACOTE ERRADO!!!!!")
                print(f"pacote sendo enviado: {head + payload + eop}")
                print(f"tamanho do pacote sendo enviado {len(head + payload + eop)}")
                linhaarquivo = str(ctime(time())) + '/' + 'envio' + '/' + '3' +  '/' + '83' +  '/' + "90" + '\n'
                f2.write(linhaarquivo)
                tentativadeerro = True
                timer2 = time()
    
                while com1.rx.getIsEmpty():
                    sleep(0.5)
        
                    if (time() - timer2) > 20:
                            mensagemtimeout = b'x/05' + b'/x00'*9 + eop
                            com1.sendData(mensagemtimeout)   
                            com1.disable()
                            break
                
                if timeout == True:
                    print("----------------------------")
                    print("TIMEOUT!!!!")
                    print("----------------------------")
                    break
                
                rxBuffer, nRx = com1.getData(14)
                print(f"resposta do servidor: {rxBuffer}")
                linhaarquivo = str(ctime(time())) + '/' + 'receb' + '/' + '6' +  '/' + '14' + 'ORDEM ERRADA DE PACOTE' + '\n'
                f2.write(linhaarquivo)
            
            
            else:
            
                qualpacoteembytes = (j).to_bytes(1, byteorder='big')
                tamanhopayloadpacote = (len(txBuffer[(maiscentoequatorze) : (maiscentoequatorze) + 114])).to_bytes(1, byteorder = 'big')
                head = bytearray.fromhex('03' + '13' + '00') + numerodepacotesembytes + qualpacoteembytes + tamanhopayloadpacote + bytearray.fromhex('00' + '00') + bytearray.fromhex('00' + '00')
                payload = txBuffer[(maiscentoequatorze) : (maiscentoequatorze) + 114] #porção da imagem que será enviada
                eop = bytearray.fromhex('AA'+'BB'+'CC'+'DD')
                com1.sendData(head + payload + eop)
                print(f"enviando pacote : {j}")
                print(f"pacote sendo enviado: {head + payload + eop}")
                print(f"tamanho do pacote sendo enviado {len(head + payload + eop)}")
                maiscentoequatorze = maiscentoequatorze + 114
                
                #escrevendo no arquivo:
                linhaarquivo = str(ctime(time())) + '/' + 'envio' + '/' + '3' +  '/' + '128' +  '/' + str(j) + '\n'
                f1.write(linhaarquivo)
                f2.write(linhaarquivo)
                f3.write(linhaarquivo)
                f4.write(linhaarquivo)

                j = j + 1
        
                timer2 = time()

                print(com1.rx.getIsEmpty())
                

                while com1.rx.getIsEmpty():
                    sleep(0.5)
                    com1.sendData(head + payload + eop)
                    print(f"enviando pacote : {j}")
                    print(f"pacote sendo enviado: {head + payload + eop}")
                    print(f"tamanho do pacote sendo enviado {len(head + payload + eop)}")
                    print((time() - timer2))
                    linhaarquivo = str(ctime(time())) + '/' + 'envio' + '/' + '3' +  '/' + '128' +  '/' + str(j) + '\n' + "ESPERANDO MENSAGEM TIPO 4"
                    f3.write(linhaarquivo)
                
    
                    if (time() - timer2) > 20:
                        mensagemtimeout = b'x/05' + b'/x00'*9 + eop
                        com1.sendData(mensagemtimeout)   
                        com1.disable()
                        timeout = True
                        linhaarquivo = 'TIMEOUT'
                        f3.write(linhaarquivo)
                        break
        
            
                if timeout == True:
                    print("----------------------------")
                    print("TIMEOUT!!!!")
                    print("----------------------------")
                    break

                rxBuffer, nRx = com1.getData(14)
                print(f"resposta do servidor: {rxBuffer}")
                linhaarquivo = str(ctime(time())) + '/' + 'receb' + '/' + '4' +  '/' + '14' + '\n'
                f1.write(linhaarquivo)
                f2.write(linhaarquivo)
                f3.write(linhaarquivo)
                f4.write(linhaarquivo)
            
        
    
               
                
            
            if rxBuffer[0] != 4 and com1.rx.getIsEmpty() is False:
                print("--------------------------------------------------")
                print("NÃO RECEBEU RESPOSTA TIPO 4")
                print("--------------------------------------------------")
            
            if rxBuffer[6] != 0:
                j = rxBuffer[6]
                maiscentoequatorze = maiscentoequatorze - 114

                

            if len(rxBuffer) < 1:
                print("--------------------------------------------------")
                print("NÃO RECEBEU RESPOSTA")
                print("--------------------------------------------------")
                break
                 
            
            if (time()-timer1) > 20:
                print("--------------------------------------------------")
                print("NÃO RECEBEU RESPOSTA NO TEMPO CORRETO")
                print("--------------------------------------------------")
                mensagemtimeout = b'x/05' + b'/x00'*9 + eop
                com1.sendData(mensagemtimeout)   
                com1.disable()
                break
                
                 
            
            if rxBuffer[0] == 6 and tentativadeerro is True:
                print(f"rxBuffer: {rxBuffer[6]}")
                j = (rxBuffer[6])
                timer1 = time()
                print(tentativadeerro)
                print("--------------------------------------------------")
                print("SERVER NÃO RECEBEU O PACOTE CORRETO")
                print("--------------------------------------------------")
            
            else:
                 timer1 = time()
        

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
