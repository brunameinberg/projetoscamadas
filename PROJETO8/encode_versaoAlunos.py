
#importe as bibliotecas
from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import math
from pydub import AudioSegment
import time
from funcoes_LPF import *
import soundfile as sf
import numpy as np

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

    signalmeu = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    fs = 44100
    data, samplerate = sf.read('audio.wav')
    tempo_plot = np.linspace(0, 3, 133121)

    dados = data[:,1]
    paranormalizar = abs(max(dados))
    dados2 = dados/paranormalizar

    plt.plot(tempo_plot, dados2)
    plt.title("Sinal no tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()

    signal = filtro(dados, samplerate, 4000)
    paranormalizar = abs(max(signal))
    signal2 = signal/paranormalizar

    
    sd.playrec(signal2,fs,channels=2)


    plt.plot(tempo_plot, signal2)
    plt.title("Sinal no tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()

    signalmeu.plotFFT(signal2, fs)
    plt.show()

    seno = math.sin(2*math.pi*14000)

    S_t = signal2*np.sin(2*math.pi*14000*tempo_plot)
    
    paranormalizar2 = abs(max(S_t))
    S_t2 = S_t/paranormalizar2

    sd.playrec(S_t2,fs,channels=2)
    print("Tocando")

    plt.plot(tempo_plot, S_t2)
    plt.title("Sinal no tempo MODULADO")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()

    signalmeu.plotFFT(S_t2, fs)
    plt.show()

    
    # aguarda fim do audio
    sd.wait()
    #plotFFT(self, signal, fs)
    

if __name__ == "__main__":
    main()
