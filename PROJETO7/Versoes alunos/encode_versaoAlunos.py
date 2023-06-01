
#importe as bibliotecas
from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import math

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)




def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")
    print("Aguardando usuário")
    print("Gerando Tons base")

    f1 = 697
    f2 = 770
    f3 = 852
    fa = 1209
    fb = 1336
    fc = 1477
    

    tecla = input("Digite uma tecla de 1-9: ")
    if tecla == '1':
        freq1 = f1
        freq2 = fa
    
    if tecla == '2':
        freq1 = f1
        freq2 = fb
    
    if tecla == '3':
        freq1 = f1
        freq2 = fc
    
    if tecla == '4':
        freq1 = f2
        freq2 = fa
    
    if tecla == '5':
        freq1 = f2
        freq2 = fb
    
    if tecla == '6':
        freq1 = f2
        freq2 = fc
    
    if tecla == '7':
        freq1 = f3
        freq2 = fa
    
    if tecla == '8':
        freq1 = f3
        freq2 = fb
    
    if tecla == '9':
        freq1 = f3
        freq2 = fc
    
    #fazendo as senoides A*sin(2*pi*f*t)
    fs = 44100
    t = np.linspace(0, 3, fs*3)
    tone1 = np.sin(2*np.pi*freq1*t)
    tone2 = np.sin(2*np.pi*freq2*t)
    tone = tone1 + tone2

    #plotando o grafico
    tempo_plot = np.linspace(0,0.01,441)
    tone1_plot = np.sin(2*np.pi*freq1*tempo_plot)
    tone2_plot = np.sin(2*np.pi*freq2*tempo_plot)
    tone_plot = tone1_plot + tone2_plot
    
    plt.plot(tempo_plot, tone_plot)
    plt.title('Senoide')
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    plt.show()

    #transfromada de fourier
    meusignal = signalMeu()
    x,y = signalMeu.calcFFT(meusignal, tone, fs)
    grafico = signalMeu.plotFFT(meusignal, tone, fs)


    
    

    


    print("Executando as senoides (emitindo o som)")
    #print("Gerando Tom referente ao símbolo : {}".format(NUM))
    sd.play(tone, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()
    #plotFFT(self, signal, fs)
    

if __name__ == "__main__":
    main()
