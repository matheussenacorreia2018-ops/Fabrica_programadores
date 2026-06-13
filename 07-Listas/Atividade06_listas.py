# Autor: Matheus Sena
# Projeto: Listas em Python

  #         0        1          2         3          4       5    
nomes = ["Pelé", "Maradona", "Messi", "Ronaldo",]# Neymar # Raí (Mbappe)
print(nomes)

# Adicionando um nome na lista
# Para retirar as aspas e os colchetes, use *
nomes.append("Raí")
print(*nomes)

# Adicionando um nome em uma posição específica
nomes.insert(4, "Neymar")
print(*nomes)

# Modificar uma pessoa da lista
nomes [5] = "Mbappe"
print(*nomes)

# Removendo um nome da lista
del nomes [1]
print(*nomes)

# Removendo um nome por texto
# Buscar o nome e apagar o primeiro que aparecer
nomes.remove("Mbappe")
print(*nomes)

# Usando o pop para mostrar o nome removido.
#   0    1      2      3
# Pelé Messi Ronaldo Neymar
removido = nomes.pop(2)
print(f"Após o pop foi removido o nome: {removido}", nomes)

# Limpar a lista
nomes.clear()
print(f" Após o clear a lista é: {nomes}")