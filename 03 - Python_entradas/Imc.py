# Autor: Matheus Sena
# Projeto: Variável (float)

peso = float(input('Digite seu peso: '))
altura = float(input('Digite sua altura'))

imc = peso / (altura * altura)
print(f'Seu imc é: {imc}')