programa {
  funcao inicio() {
    real valor_produto, valor_desconto, valor_porcentagem
    // valor do produto = 500
    // valor da porcentagem = 25%
    // valor do desconto = 125

    escreva("Digite o valor do produto: ")
    leia(valor_produto)
    escreva("Digite o valor do desconto: ")
    leia(valor_desconto)

    valor_desconto = valor_produto * (valor_porcentagem/100)
    escreva("\no valor total do produto é: ",valor_desconto)
  }
}
