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
import random

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
        print("-------------------------")
        print("enviando byte de sacrificio")
        print("-------------------------")
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        #PACOTE HANDSHAKE
        #o primeiro pacote a ser enviado é somente o handshake, para considerar somente o primeiro byte como 1

        handshake = '01'+64*'00'
        handshake = bytearray.fromhex(handshake)
        print(handshake)

        #envia handshake
        com1.sendData((handshake)) 

        #caso seja recebido o handshake com o primeiro byte sendo 1, esperar retorno de 1 também



        while com1.rx.getBufferLen() < 1:
            time.sleep(3)
            break

        if  com1.rx.getBufferLen() < 1:
            print("-------------------------")
            testeservidor = input("Servidor inativo. Tentar novamente? S/N" )
            print(testeservidor)
            print("-------------------------")
                
            while testeservidor == "S":
                print("tentando novamente")
                time.sleep(5)
                com1.sendData(np.asarray(handshake)) 
                

                if com1.rx.getBufferLen() < 1: 
                    print('tentou de novo e nao foi')
                    com1.disable()
                    break

            if testeservidor == "N":
                com1.disable()
            
        else:        
        
            rxBuffer, nRx = com1.getData(65)

        if len(rxBuffer) == 65: 

            print("recebeu {} bytes" .format(len(rxBuffer)))
            print("-------------------------")
            print("HANDSHAKE")

            if rxBuffer[0] == 1:
                print("-------------------------")
                print("O SERVIDOR ESTÁ PRONTO")
                print("-------------------------")
                
                print("enviando informações")

                #montando o head que será enviado
                #a primeira informação do head é sempre o númedo total de pacotes

                imageR = "img/cararetokingo.jpg" #imagem que será enviada
                txBuffer = open(imageR, 'rb').read()
                print("meu array de bytes tem tamanho {}" .format(len(txBuffer))) #tamanho da imagem
                numerodepacotes2 = int((len(txBuffer)) // 50) #quantidade de pacotes
                numerorestantedepacotes = int((len(txBuffer)) % 50)
                numerodepacotes = (numerodepacotes2 + 1).to_bytes(1, byteorder = 'big')
                print(f"quantidade de pacotes {numerodepacotes2}")
                print(f"numero final de bytes pacote final {numerorestantedepacotes}")

                maiscinquenta = 0
                for i in range(0, numerodepacotes2 + 1):

                    j = i.to_bytes(1, byteorder = 'big')
                    payload = txBuffer[(maiscinquenta) : (maiscinquenta) + 50] #porção da imagem que será enviada
                    

                    if i == 81:
                        com1.sendData(numerodepacotes + j + (len(txBuffer[4049 : 4092])).to_bytes(1, byteorder = 'big') + (9* b'\x00') + txBuffer[4049 : 4092] + (b'\xAA')*3)
                        print("enviando pacote final")
                    
                    else:
                        tamanhopayloadembytes = (len(txBuffer[(maiscinquenta) : (maiscinquenta) + 50])).to_bytes(1, byteorder = 'big')
                        com1.sendData(numerodepacotes + j + tamanhopayloadembytes + (9* b'\x00') + payload + (b'\xAA')*3)
                        print(f"enviando pacote : {i}")
                        maiscinquenta = maiscinquenta + 50
                        rxBuffer, nRx = com1.getData(65)
                        print(f"confimação que recebeu o pacote!")

                    


                    if rxBuffer[0] != 170 or len(rxBuffer) < 1:
                        print("--------------------------------------------------")
                        print("NÃO RECEBEU RESPOSTA PRA ENVIAR MAIS COMANDO")
                        print("--------------------------------------------------")
                        break
                        
                

        
           


        
        #txBuffer = imagem em bytes!
        '''retornacomandos = "files/devolve.txt"
 
       
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)-1))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos'''


        #print("salvando dados no arquivo:")
        #print("- {}".format(retornacomandos))
        #f = open(retornacomandos, 'wb')
        #f.write(rxBuffer)

        #f.close()
            

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
