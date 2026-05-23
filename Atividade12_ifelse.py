#Autor: Matheus Sena

nome = input("Digite seu nome: ")
telefone = float(input("Digite seu telefone: "))
cidade = input("Digite a sua cidade: ")
salario = float(input("Digite seu salario: "))

if salario >= 1000:
    print ("Você possui uma renda boa")
elif salario >= 700:
    print ("Você pssui uma renda razoável")
elif salario >= 500:
    print ("Você possui uma renda baixa")
else:
    print ("Você possui uma renda muito baixa")