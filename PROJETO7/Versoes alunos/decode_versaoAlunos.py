
#Importe todas as bibliotecas
from suaBibSignal import *
import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    fs = 44100
    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels =2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  1 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = fs*duration
    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao
    n = 5 
    print(f"**** CAPTÇÃO COMEÇA EM {n} SEGUNDOS ****")
    
    #use um time.sleep para a espera
    time.sleep(n)
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("----------------------------------")
    print("GRAVAÇÃO INICIALIZADA")
    print("----------------------------------")
    #para gravar, utilize
    audio = sd.rec(int(numAmostras), fs, channels=2)
    sd.wait()
    print("...     FIM")
    
    
    sd.playrec(audio,fs,channels=2)


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    dados =audio[:,1]
    

    
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    y = audio[:,1]
    print(y)
    T = len(y)
    print(f"O PERÍODO É {T}")
    t = np.linspace(0,1,fs)
    print(t)
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
    plt.plot(t,dados)
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    #xf, yf = signal.calcFFT(y, fs)
    xf,yf = signal.calcFFT(dados,fs)
    signal.plotFFT(dados,fs)
    tecla = 0
    xf = list(xf)
    yf = list(yf)
    lista_filtro = []
    for i in range(0,10):
        for car in yf:
            ind = yf.index(max(yf))
            lista_filtro.append(xf[ind])
            del xf[ind]
            del yf[ind]

  

    #tecla 1 = 697 e 1209
    #tecla 2 = 697 e 1336
    #tecla 3 = 697 e 1477
    #tecla 4 = 770 e 1209
    #tecla 5 = 770 e 1336
    #tecla 6 = 770 e 1477
    #tecla 7 = 852 e 1209
    #tecla 8 = 852 e 1336
    #tecla 9 = 852 e 1477

    freq1 = False
    freq2 = False
    freq3 = False
    freq4 = False
    freq5 = False
    freq6 = False
    freq7 = False
    freq8 = False
    freq9 = False


    for frequencia in lista_filtro[0:10]:
        for i in np.arange(850,855,0.01):
            if round(i,2)==round(frequencia,2):
                freq3 = True
        for i in np.arange(768,773,0.01):
            if round(i,2)==round(frequencia,2):
                freq2 = True
        for i in np.arange(695,700,0.01):
            if round(i,2)==round(frequencia,2):
                freq1 = True     
        for i in np.arange(1207,1212,0.01):
            if round(i,2)==round(frequencia,2):
                freq4 = True
        for i in np.arange(1334,1339,0.01):
            if round(i,2)==round(frequencia,2):
                freq5 = True
        for i in np.arange(1475,1480,0.01):
            if round(i,2)==round(frequencia,2):
                freq6 = True

    if freq1 == True and freq4 == True:
        print("TECLA 1")
    if freq1 == True and freq5 == True:
        print("TECLA 2")
    if freq1 == True and freq6 == True:
        print("TECLA 3")
    if freq2 == True and freq4 == True:
        print("TECLA 4")
    if freq2 == True and freq5 == True:
        print("TECLA 5")
    if freq2 == True and freq6 == True:
        print("TECLA 6")
    if freq3 == True and freq4 == True:
        print("TECLA 7")
    if freq3 == True and freq5 == True:
        print("TECLA 8")
    if freq3 == True and freq6 == True:
        print("TECLA 9")
       
        


    



   
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    #index = peakutils.indexes(yf, thres=0.4, min_dist=50)
    #print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
