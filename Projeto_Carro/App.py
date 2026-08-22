# Autor: Matheus Sena

import streamlit as st

st.sidebar.image("img/Logo.jpg")  # Logo da empresa
st.sidebar.markdown("*Sena Locações*")  # Nome da empresa

lista_carros = [
    "McLaren MP4-4",
    "Porsche 917-30",
    "Ferrari 330 P4",
    "Audi Sport Quattro S1",
    "BMW E30 M3",
    "Fusca AZUL",
    "Lamborghini Miura",
    "Mercedes-Benz 300SL",
]

detalhes_carros = {
    "McLaren MP4-4": {
        "preco": "R$ 200.000",
        "portas": "0 (Monoposto)",
        "Cor": "Branco e Vermelho",
    },
    "Porsche 917-30": {
        "preco": "R$ 150.000",
        "portas": "0 (Cockpit aberto)",
        "Cor": "Azul e Amarelo",
    },
    "Ferrari 330 P4": {
        "preco": "R$ 15.000",
        "portas": "2 portas",
        "Cor": "Vermelho",
    },
    "Audi Sport Quattro S1": {
        "preco": "R$ 40.000",
        "portas": "2 portas",
        "Cor": "Branco, Amarelo e Preto",
    },
    "BMW E30 M3": {
        "preco": "R$ 4.500",
        "portas": "2 portas",
        "Cor": "Preto",
    },
    "Fusca AZUL": {
        "preco": "R$ 800",
        "portas": "2 portas",
        "Cor": "Azul",
    },
    "Lamborghini Miura": {
        "preco": "R$ 50.000",
        "portas": "2 portas",
        "Cor": "Cinza",
    },
    "Mercedes-Benz 300SL": {
        "preco": "R$ 35.000",
        "portas": "2 portas",
        "Cor": "Cinza",
    },
}

carro_selecionado = st.sidebar.selectbox(
    "Selecione o carro que você deseja: ", lista_carros
)
detalhes_selecionado = detalhes_carros[carro_selecionado]

st.title(carro_selecionado)
st.image(f"img/{carro_selecionado}.jpg")

st.subheader("🚗 Detalhes do Veículo")

col1, col2, col3 = st.columns(3)

# Display formatted price metric
col1.metric("Preço Diária", detalhes_selecionado["preco"])
col2.metric("Portas", detalhes_selecionado["portas"])
col3.metric("Cor", detalhes_selecionado["Cor"])

st.divider()

qtd_dias = st.number_input("Quantos dias quer ficar com o carro?", min_value=1, value=1)


preco_numerico = int(
    detalhes_selecionado["preco"]
    .replace("R$", "")
    .replace(".", "")
    .strip()
)
total = qtd_dias * preco_numerico

if st.button("Alugar", type="primary"):
    st.success(f"O aluguel do carro vai custar: **R$ {total:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))