# Autor: Matheus Sena

# Função listas


  #         0        1          2         3      
nomes = ["Rayssa", "Sena", "Humberto", "Pietro",]

# Chamada listas
def name(nomes):
    nomes.append(input("Digite o nome do contato a ser adicionado: "))
    nomes.remove(input("Digite o contato a ser removido: "))
    print(nomes)
        
name(nomes)