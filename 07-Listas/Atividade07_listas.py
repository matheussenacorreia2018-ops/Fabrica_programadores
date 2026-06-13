# Autor: Matheus Sena
# Projeto: Listas em Python

  #         0        1          2         3          4    
nomes = ["Pelé", "Maradona", "Messi", "Ronaldo",] # Raí 
print(nomes)

# Adicionando um nome na lista
# Para retirar as aspas e os colchetes, use *
nomes.append("Raí")
print(*nomes)


# Removendo um nome por texto
# Buscar o nome e apagar o primeiro que aparecer
nomes.remove("Maradona")
print(*nomes)
