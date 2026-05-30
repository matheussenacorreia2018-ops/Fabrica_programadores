#Autor: Matheus Sena
#Projeto : Loop FOR - Variavéis de início e fim

numero = int(input("Digite a tabuada desejada: "))
numero_inicio = int(input("Digite o inicio da tabuada: "))
numero_fim = int(input("Digite o fim da tabuada: "))


# loop FOR

for i in range (numero_inicio,numero_fim):
    print(f"{numero} x {i} = {i * numero}")