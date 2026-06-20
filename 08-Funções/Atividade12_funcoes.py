# Autor: Matheus Sena

# Função Loop For
numero = int(input("Digite o numero: "))

def tabuada(numero):
  for i in range (1,101):
    print(f"{numero} x {i} = {i * numero}")

tabuada(numero)