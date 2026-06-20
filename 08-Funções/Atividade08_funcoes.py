# Autor: Matheus Sena

nome = input("Digite o nome do aluno: ")
nota = float(input("Digite a nota do aluno: "))


# Função status do aluno
def status(nota):
    if nota >= 7:
        print("Aluno aprovado! ")
    elif nota >= 4:
        print("Aluno em recuperação! ")
    else:
      print("Aluno reprovado! ")

# Chamada da função
status(nota)