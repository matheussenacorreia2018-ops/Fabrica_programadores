# Autor: Matheus Sena
# Projeto: Função imc

peso = float(input("Digite seu peso: "))
altura = float(input("Digite sua altura: "))

# Função imc
def calcular_imc(peso,altura):
    imc = peso / (altura * altura)
    print(f"Seu imc é: {imc:.2f}")

calcular_imc(peso,altura)