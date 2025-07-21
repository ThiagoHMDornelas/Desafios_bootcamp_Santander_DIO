from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print(" Transações permitidas por dia excedido.")
            return

        transacao.registrar(conta)

    def adicionar_Conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        super().__init__(endereco)


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, rlValor):
        rlSaldo = self._saldo
        boSaldoExcedido = rlValor > rlSaldo

        if boSaldoExcedido:
            print("\nERRO! Saldo insuficiente para sacar o vlr. informado!")
        elif rlValor > 0:
            self._saldo -= rlValor
#            stExtrato += f"Saque:\t\tR$ {rlValor:.2f}\n"
#            itQtdSaque += 1
            print("\nSaque realizado com sucesso!")
            return True
        else:
            print("\nERRO! O valor de saque informado deve ser maior do que 0(zero).")

        return False

    def depositar(self, rlVlrDeposito):    
        if rlVlrDeposito > 0:
            self._saldo += rlVlrDeposito
#            stExtrato += f"Depósito:\tR$ {rlVlrDeposito:.2f}\n"
            print("\nDepósito realizado com sucesso!")
            return True
        else:
            print("\nERRO! O valor de depósito deve ser maior do que 0(zero).")
            return False

    def saldo():
        pass


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, VlrLimite=500, QtdLimiteSaques=3):
        self._limite = VlrLimite
        self._limite_saques = QtdLimiteSaques
        super().__init__ (numero, cliente)   

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\nErro! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\nErro! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False
        
    def info_conta(self):
        print(f"""\
            Agência: {self._agencia}
            C/C    : {self._numero}
            Titular: {self._cliente}
        """)
        print("*************************")        


# Classe igual a do Professor Felipe (DIO). 
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strftime(transacao["data"], "%d-%m-%Y %H:%M:%s").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)

        return transacoes


# Classe igual a do Professor Felipe (DIO). 
class Transacao(ABC):
    @property
    @abstractmethod    
    def valor(self):
        pass
    
    @classmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {func.__name__.upper()}")
        return resultado

    return envelope


menu = """

[d]  Depositar
[s]  Sacar
[e]  Extrato
[cc] Criar Conta
[ec] Exibir Contas
[nu] Novo Usuário
[q]  Sair

=> """

@log_transacao
def depositar(rlSaldo, rlVlrDeposito, stExtrato, /):    
    if rlVlrDeposito > 0:
        rlSaldo += rlVlrDeposito
        stExtrato += f"Depósito:\tR$ {rlVlrDeposito:.2f}\n"
        print("\nDepósito realizado com sucesso!")
    else:
        print("\nERRO! O valor de depósito deve ser maior do que 0(zero).")

    return rlSaldo, stExtrato

@log_transacao
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

@log_transacao
def exibir_extrato(rlSaldo, /, *, stExtrato):
        print("\n================ Extrato ================")
        print("Não foram realizadas movimentações." if not stExtrato else stExtrato)
        print(f"\nSaldo: R$ {rlSaldo:.2f}")
        print("==========================================")

@log_transacao
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

@log_transacao
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
