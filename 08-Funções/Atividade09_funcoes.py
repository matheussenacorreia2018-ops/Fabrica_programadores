# Autor: Matheus Sena
# Função imc

peso = float(input("Digite seu peso: "))
altura = float(input("Digite sua altura: "))

#Calculo IMC
imc = peso / (altura ** 2)

#exibindo resultado
print(f"\nSeu IMC é: {imc: 2f}")

# Função imc
def calcular (peso, altura):
    if imc < 18.5:
        print("Abaixo do peso")
    elif imc <= 25:
        print("Peso normal")
    elif imc <=30:
        print("Sobrepeso")
    else:
        print("Obesidade")

calcular(peso, altura)