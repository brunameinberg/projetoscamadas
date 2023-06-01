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
        com1.enable()

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)


           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        #LISTA DE COMANDOS QUE SERÃO SELECIONADOS 
        listadecomandos = [b'\x00\x00\x00\x00', b'\x00\x00\xAA\x00',b'\xAA\x00\x00', b'\x00\xAA\x00', b'\x00\x00\xAA', b'\x00\xAA', b'\xAA\x00', b'\x00', b'\xFF']

        #SELECIONANDO OS COMANDOS
        quantidadedecomandos = random.randrange(10, 30)
        print(f"quantidade de comandos enviados: {quantidadedecomandos}")

        comandosusados = []
        for i in range(0, quantidadedecomandos):
            c = random.choice(listadecomandos)
            comandosusados.append(c + b'\x2d')

        print(f"lista de comandos utilizados{comandosusados}")

        #transformando no formato certo
        arraydebytes = b''
        for elemento in comandosusados:
            #print(elemento)
            arraydebytes += ((elemento))

        #separador do tempo e dos comandos (~)

        print(arraydebytes )

        print(f"array de bytes enviados: {arraydebytes}")
        stringdearray = (str(arraydebytes))

        contador = 0
        for letra in stringdearray:
            if letra == "x":
                contador = contador + 1

        contador = contador + quantidadedecomandos

        print(f"quantidade de bytes {contador}")
        #tamanhocomoarray = bytearray(contador)
        tamanhocomoarray = contador.to_bytes(1, byteorder='big')
        #print(qtd_bytes_hx)
        #tamanhocomoarray = bytearray.fromhex(qtd_bytes_hx)
        print(f"contador como array {tamanhocomoarray}")


        arraydedevolucao = tamanhocomoarray + arraydebytes
        

        print(f"array que será enviado completo {arraydedevolucao}")
        
        #txBuffer = imagem em bytes!
        retornacomandos = "files/devolve.txt"

        print("Carregando imagem para transmissão")
        print(" - {}". format(arraydedevolucao))
        print("------------------------")

        txBuffer = arraydedevolucao 
       
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)-1))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        print(f"com1 = {com1}")
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        txSize = com1.tx.getStatus()
        print(f"txSize: {txSize}")
        print('enviou = {}' .format(txBuffer))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos

        print("esperando 1 byte com tamanho recebido")

        
        while com1.rx.getBufferLen() < 1:
            time.sleep(3)
            break

        if com1.rx.getBufferLen() < 1: 
            print("-------------------------")
            print("NAO TEVE RESPOSTA")
            print("-------------------------")
            com1.disable()
        
        else:

            rxBuffer, nRx = com1.getData(1)
    
            print("recebeu {} byte" .format(len(rxBuffer)))
                

            for i in range(len(rxBuffer)):
                print("recebeu {}" .format(rxBuffer[i]))
        

        #print("salvando dados no arquivo:")
        #print("- {}".format(retornacomandos))
        f = open(retornacomandos, 'wb')
        f.write(rxBuffer)

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
