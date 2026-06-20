# Autor: Matheus Sena

# Função Loop While


numero = int(input("Digite a tabuada desejada: "))

def tabuada(numero):
  i = 1
  while i <= 10:
    print(f"valor de i antes da interação {i}")
    print(f"{numero} x {i} = {numero * i}")
    i = i + 1
    print(f"valor do i depois da iteração {i}")

tabuada(numero)