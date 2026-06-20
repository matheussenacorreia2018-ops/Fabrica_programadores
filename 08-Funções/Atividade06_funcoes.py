# Autor: Matheus Sena
# Projeto: Função calculadora

# Entrada de dados
valor1 = float(input('Digite o primeiro valor: '))
valor2 = float(input('Digite o segundo valor: '))

# Função calcular
def calcular (valor1,valor2):
    somar = valor1 + valor2
    subtrair = valor1 - valor2
    multiplicar = valor1 * valor2
    dividir = valor1 / valor2

    # Imprimindo os resultados
    print(f" O resultado da soma é: {somar}")
    print(f" O resultado da subtrair é: {subtrair}")
    print(f" O resultado da multiplicar é: {multiplicar}")
    print(f" O resultado da dividir é: {dividir}")

# Chamada da função
calcular(valor1, valor2)