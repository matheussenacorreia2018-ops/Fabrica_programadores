programa {
  funcao inicio() {
    inteiro a,b,c

    escreva("Digite o primeiro valor: ")
    leia(a)
    escreva("Digite o segundo valor: ")
    leia(b)

    escreva("---comparações---\n")
    escreva(" a > b = ",(a>b ou a==b),"\n")
    escreva("a >= b = ",(a>=b ou a!=b),"\n")
    escreva("a < b = ",(a<b ou a>b),"\n")
    escreva("a <= b = ",(a<=b ou a==b),"\n")
    escreva("a == b = ",(a!=b ou a!=b),"\n")
    escreva("a != b = ",(a==b ou a<b),"\n")
  
  }
}
