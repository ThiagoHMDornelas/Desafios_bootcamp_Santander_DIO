menu = """

[d]  Depositar
[s]  Sacar
[e]  Extrato
[cc] Criar Conta
[ec] Exibir Contas
[nu] Novo Usuário
[q]  Sair

=> """
def depositar(rlSaldo, rlVlrDeposito, stExtrato, /):    
    if rlVlrDeposito > 0:
        rlSaldo += rlVlrDeposito
        stExtrato += f"Depósito:\tR$ {rlVlrDeposito:.2f}\n"
        print("\nDepósito realizado com sucesso!")
    else:
        print("\nERRO! O valor de depósito deve ser maior do que 0(zero).")

    return rlSaldo, stExtrato

def sacar(*, rlSaldo, rlValor, stExtrato, rlVlrLimitePorSaque, itQtdSaque, itQtdLimiteSaque):
    boSaldoExcedido = rlValor > rlSaldo
    boLimiteSaqueExcedido = rlValor > rlVlrLimitePorSaque
    boQtdLimiteSaqueExcedido = itQtdSaque >= itQtdLimiteSaque

    if boSaldoExcedido:
        print("\nERRO! Saldo insuficiente para sacar o vlr. informado!")
    elif boLimiteSaqueExcedido:
        print("\nERRO! Valor limite por saque excedido. Saque deve ser de no máximo R$ {rlVlrLimitePorSaque:.2f}!")
    elif boQtdLimiteSaqueExcedido:
        print("\nERRO! Número máximo de saques por dia excedido. Qtd. maxima de {itQtdLimiteSaque}!")
    elif rlValor > 0:
        rlSaldo -= rlValor
        stExtrato += f"Saque:\t\tR$ {rlValor:.2f}\n"
        itQtdSaque += 1
        print("\nSaque realizado com sucesso!")
    else:
        print("\nERRO! O valor de saque informado deve ser maior do que 0(zero).")

    return rlSaldo, stExtrato

def exibir_extrato(rlSaldo, /, *, stExtrato):
        print("\n================ Extrato ================")
        print("Não foram realizadas movimentações." if not stExtrato else stExtrato)
        print(f"\nSaldo: R$ {rlSaldo:.2f}")
        print("==========================================")

def novo_usuario(usuarios):
    stCpf = input("Informe o CPF (apenas números): ")
    usuario = localizar_usuario(stCpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    stNome = input("Informe o nome completo: ")
    stDataNascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    stEndereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": stNome, "data_nascimento": stDataNascimento, "cpf": stCpf, "endereco": stEndereco})

    print("Usuário criado com sucesso!")

def nova_conta(stAgencia, stNroConta, usuarios, contas):
    stCpf = input("Informe o CPF do usuário: ")
    usuario = localizar_usuario(stCpf, usuarios)

    if usuario:
        contas.append({"agencia": stAgencia, "nro_conta": stNroConta, "usuario": usuario})
        print("\nConta criada com sucesso!")
    else:
        print("\nUsuário não encontrado!")

    return

def localizar_usuario(stCpf, usuarios):
    usuarios_encontrado = []
    for usuario in usuarios:
        if usuario["cpf"] == stCpf:
           usuarios_encontrado = usuario 
    
    if len(usuarios_encontrado) > 0:
        return usuarios_encontrado
    else:
        return None

def exibir_contas(contas):
    for conta in contas:
        print(f"""\
            Agência: {conta['agencia']}
            C/C    : {conta['nro_conta']}
            Titular: {conta['usuario']['nome']}
        """)
        print("*************************")



stAgencia = "0001"
rlSaldo = 0
rlVlrLimitePorSaque = 500
stExtrato = ""
itQtdSaque = 0
itQtdLimiteSaque = 3
usuarios = []
contas = []

while True:
    stOpcao = input(menu)

    # Deposito
    if stOpcao == "d":
        rlValor = float(input("Qual o Vlr. que deseja Depositar? "))
        rlSaldo, stExtrato = depositar(rlSaldo, rlValor, stExtrato)
    # Saque        
    elif stOpcao == "s":
        rlValor = float(input("Qual o Vlr deseja sacar? "))

        rlSaldo, stExtrato = sacar(rlSaldo = rlSaldo, rlValor = rlValor, stExtrato = stExtrato,                             
                               rlVlrLimitePorSaque = rlVlrLimitePorSaque, itQtdSaque = itQtdSaque,
                               itQtdLimiteSaque = itQtdLimiteSaque,)
    elif stOpcao == "e":
        exibir_extrato(rlSaldo, stExtrato = stExtrato)
    elif stOpcao == "nu":
        novo_usuario(usuarios)
    elif stOpcao == "cc":
        stNroConta = len(contas) + 1
        nova_conta(stAgencia, stNroConta, usuarios, contas)
    elif stOpcao == "ec":
        exibir_contas(contas)
    elif stOpcao == "q":
        break
    else:
        print("ERRO! Opção informada não é válida.")
