menu = """

[d] Depositar
[s] Sacar
[e] rlExtrato
[q] Sair

=> """

rlSaldo = 0
rlVlrLimitePorSaque = 500
rlExtrato = ""
itQtdSaque = 0
itQtdLimiteSaque = 3

while True:
    stOpcao = input(menu)
    # Deposito
    if stOpcao == "d":
        rlValor = float(input("Qual o Vlr. que deseja Depositar? "))
        if rlValor > 0:
            rlSaldo += rlValor
            rlExtrato += f"Depósito: R$ {rlValor:.2f}\n"
        else:
            print("ERRO! O valor de depósito deve ser maior do que 0(zero).")
    # Saque        
    elif stOpcao == "s":
        rlValor = float(input("Qual o Vlr deseja sacar? "))

        boSaldoExcedido          = (rlValor > rlSaldo)
        boLimiteSaqueExcedido    = (rlValor > rlVlrLimitePorSaque)
        boQtdLimiteSaqueExcedido = (itQtdSaque >= itQtdLimiteSaque)

        if boSaldoExcedido:
            print("ERRO! Saldo insuficiente para sacar o vlr. informado!")
        elif boLimiteSaqueExcedido:
            print(f"ERRO! Valor limite por saque excedido. Saque deve ser de no máximo R$ {rlVlrLimitePorSaque:.2f}!")
        elif boQtdLimiteSaqueExcedido:
            print(f"ERRO! Número máximo de saques por dia excedido. Qtd. maxima de {itQtdLimiteSaque}!")
        elif rlValor > 0:
            rlSaldo -= rlValor
            rlExtrato += f"Saque: R$ {rlValor:.2f}\n"
            itQtdSaque += 1
        else:
            print("ERRO! O valor de saque informado deve ser maior do que 0(zero).")
    elif stOpcao == "e":
        print("\n================ Extrato ================")
        print("Não foram realizadas movimentações." if not rlExtrato else rlExtrato)
        print(f"\nSaldo: R$ {rlSaldo:.2f}")
        print("==========================================")
    elif stOpcao == "q":
        break
    else:
        print("ERRO! Opção informada não é válida.")
