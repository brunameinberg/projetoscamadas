import random
import numpy as np

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

print(f"quantidade de bytes {contador}")
#tamanhocomoarray = bytearray(contador)
tamanhocomoarray = contador.to_bytes(1, byteorder='big')
#print(qtd_bytes_hx)
#tamanhocomoarray = bytearray.fromhex(qtd_bytes_hx)
print(f"contador como array {tamanhocomoarray}")



arraydedevolucao = tamanhocomoarray + arraydebytes
print(f"array que será enviado completo {arraydedevolucao}")
        


    




