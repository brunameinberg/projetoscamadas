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
serialName = "COM5"                  # Windows(variacao de)


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
        
        #txBuffer = imagem em bytes!
        
        comando_f = []
        rxBuffer, nRx = com1.getData(1)
        print(f"ESTOU AQUI {rxBuffer}")
        num_total = int.from_bytes(rxBuffer)
        print(num_total)
        rxBuffer, nRx = com1.getData(num_total)
        print(rxBuffer)

        

        comandos_prontos = ['AA','00 00 00 00','00 00 AA 00','AA 00 00','00 AA 00','00 00 AA','00 AA','AA 00','00','FF']
        ultimoi = 0
        contador = 0
        for i in range(len(rxBuffer)):
            if rxBuffer[i]== 45:
                nao_passou = False
                comando = rxBuffer[ultimoi:i]
                ultimoi = i+1
                for com in comandos_prontos:      
                    if comando == bytearray.fromhex(com):
                        comando_f.append(comandos_prontos.index(com))
                        if comandos_prontos.index(com)==0:
                            nao_passou=False
                        nao_passou = True
                       
                if nao_passou == False:
                    if contador > 0:
                        print("ALGO QUE NÃO É UM COMANDO FOI ENVIADO") 
                    contador+=1    
                    
        num = len(comando_f)        
        time.sleep(.5)
        com1.sendData(num.to_bytes(1, byteorder='big'))
        for n in comando_f:
            print (f"Comando {n}")
    
            
    
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
