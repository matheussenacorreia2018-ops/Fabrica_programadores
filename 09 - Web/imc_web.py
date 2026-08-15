#Autor: Matheus Sena
#Projeto: IMC com streamlit

# Importanto a biblioteca
import streamlit as st


st.title("Calculadora IMC")
peso = st.number_input("Digite seu peso (kg): ")
altura = st.number_input("Digite sua altura (m): ")

#Ação do botão
if st.button("Calcular IMC", type = "primary"):
    #Verifica se o usuário digitou o valor > que zero
    if peso > 0 and altura > 0:
        imc = peso /(altura ** 2)
        st.success(f"Seu IMC é: {imc:.2f}")
        if imc <= 18.5:
            st.warning("Abaixo do peso", icon="⚠️")
        elif imc <= 24.9:
            st.success("Peso normal!", icon="✅")
        elif imc <= 29.9:
            st.warning("Sobrepeso", icon="⚠️")
        elif imc <= 34.9:
            st.warning("Obesidade Grau I", icon="⚠️")
        elif imc <= 39.9:
            st.warning("Obesidade Grau II", icon="⚠️")
        else:
            st.error("Obesidade Grau III", icon="🚨")
    else:
        st.warning("Digite um valor válido", icon="⚠️")
