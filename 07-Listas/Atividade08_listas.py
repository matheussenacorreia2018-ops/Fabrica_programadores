# Autor: Matheus Sena
# Projeto: Listas em Python

  #         0        1          2         3      
nomes = ["Rayssa", "Sena", "Humberto", "Pietro",]
print(nomes)

nomes.append(input("Digite o nome do contato a ser adicionado: "))
print(*nomes)

nomes.remove(input("Digite o contato a ser removido: "))
print(*nomes)