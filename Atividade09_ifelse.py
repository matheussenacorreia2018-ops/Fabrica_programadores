#Autor: Matheus Sena
#Adesivo condicionais

#variáveis
temperatura=float(input("Olá me diga como esta a temperatura em Graus Celsius: "))
#Adesivo condicionais
if temperatura >= 30:
    print("O clima está quente")
elif temperatura >=20:
    print("O clima hoje está agradável")    
elif temperatura >= 10:
    print("O clima está frio")
else:
    print("CUIDADO está muito frio, agasalhe-se")