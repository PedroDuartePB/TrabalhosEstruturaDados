from Arvores import ArvoreBusca, Heap
from ClassesAux import TipoAtendimento, Paciente

_ubs_cadastro = ArvoreBusca()
_agenda = Heap()

# A parte visual foi feita só para auxiliar na entrega com ajuda de IA
def exibir_menu() -> str:
    print("\n" + "=" * 35)
    print(" 🏥 SISTEMA DE GESTÃO DA UBS")
    print("=" * 35)
    print("1. Cadastrar paciente no sistema")
    print("2. Remover paciente do sistema")
    print("3. Registrar chegada na recepção")
    print("4. Chamar próximo paciente (Atendimento)")
    print("5. Visualizar fila de espera")
    print("6. Sair do sistema")
    return input("Escolha uma opção: ")

def setup():
    pacientes = [(230, "jonas", 67, "sus", TipoAtendimento.CONSULTA),
                 (137, "marcia", 42, "sus", TipoAtendimento.CONSULTA),
                 (112, "lucas", 16, "sus", TipoAtendimento.CONSULTA),
                 (504, "fulano", 83, "sus", TipoAtendimento.CONSULTA),
                 (207, "jessica", 17, "sus", TipoAtendimento.CONSULTA),
                 (150, "cassio", 39, "sus", TipoAtendimento.CONSULTA),
                 (101, "Lucas Mendes", 28, "sus", TipoAtendimento.CONSULTA),
                 (202, "Mariana Silva", 77, "sus", TipoAtendimento.CONSULTA),
                 (303, "Roberto Carlos", 100, "sus", TipoAtendimento.CONSULTA),
                 (404, "Fernanda Lima", 28, "sus", TipoAtendimento.CONSULTA),
                 (505, "João Pedro", 3, "sus", TipoAtendimento.CONSULTA),
                 (606, "Camila Alves", 51, "sus", TipoAtendimento.CONSULTA)]

    for i in pacientes:
        p = Paciente(*i)
        _ubs_cadastro.inserir(p, p.cpf)

    p2 = Paciente(*pacientes[2])
    _agenda.inserir(p2, p2.idade)
    p5 = Paciente(*pacientes[5])
    _agenda.inserir(p5, p5.idade)
    pn = Paciente(*pacientes[-1])
    _agenda.inserir(pn, pn.idade)

    # agenda final Camila(51), cassio(39), lucas(16)


def main():
    while True:
        opcao = exibir_menu()
        print("")

        if opcao == '1':
            try:
                cpf = int(input("Digite o CPF (apenas números): "))
                nome = input("Digite o nome do paciente: ")
                idade = int(input("Digite a idade do paciente: "))
                tipo_atendimento = TipoAtendimento.VACINACAO
                paciente = Paciente(cpf, nome, idade, "sus", tipo_atendimento)
                _ubs_cadastro.inserir(paciente, cpf)
                print(f"✅ Sucesso: Paciente '{nome}' cadastrado sob o CPF {cpf}.")
            except ValueError:
                print("❌ Erro: O CPF deve conter apenas números válidos.")

        elif opcao == '2':
            try:
                cpf = int(input("Digite o CPF do paciente a ser removido: "))
                removido = _ubs_cadastro.remover(cpf)

                if removido is not None:
                    print(f"✅ Sucesso: Cadastro do paciente '{removido.paciente}' removido.")
                else:
                    print("⚠️ Aviso: Paciente não encontrado no sistema.")
            except ValueError:
                print("❌ Erro: O CPF deve ser numérico.")

        elif opcao == '3':
            idade:int = 0
            try:
                cpf = int(input("Digite o CPF do paciente que chegou: "))

                cadastro_encontrado = _ubs_cadastro.buscar(cpf)
                if cadastro_encontrado is not None:
                    idade = cadastro_encontrado.paciente.idade
                    _agenda.inserir(cadastro_encontrado.paciente, idade)
                else:
                    print("Registro de paciente não cadastrado:")
                    nome = input("Por favor, insira o nome do paciente: ")
                    idade = int(input("Por favor, insira a idade do paciente: "))
                    paciente = Paciente(cpf, nome, idade, "n/a", TipoAtendimento.VACINACAO)
                    _agenda.inserir(paciente, idade)
            except ValueError:
                print("❌ Erro: Entrada inválida. Use apenas números para CPF e prioridade.")
            finally:
                print(f"✅ Sucesso: Paciente cadastrado (Prioridade: {idade}).")

        elif opcao == '4':
            try:
                paciente_chamado = _agenda.remover()
                if paciente_chamado is not None:
                    print("\n" + "*" * 40)
                    print(f" 📢 ATENDIMENTO: Encaminhar '{paciente_chamado.paciente.nome_completo}' ao consultório.")
                    print("*" * 40)
            except IndexError:
                print("⚠️ Aviso: A fila de espera está vazia no momento.")

        elif opcao == '5':
            alvo =  int(input("Digite o cpf do paciente consultado (Digite 0 para ver a fila completa): "))
            try :
                proximos = _agenda.get_sorted_heap()
                listagem = ""
                cpf_found = False
                if proximos is None or len(proximos) == 0:
                    raise IndexError
                else:
                    pos = 1
                    for n in proximos:
                        listagem+=f"\n{n.get_dado().nome_completo} | {pos}"
                        if n.paciente.cpf == alvo:
                            listagem+=f"\n{pos-1} pessoas até {n.paciente.nome_completo}"
                            cpf_found = True
                            break
                        else:
                            cpf_found = False
                        pos += 1
                    if not cpf_found and alvo != 0:
                        print(f"CPF {alvo} não encontrado, fornecendo lista completa\n"+listagem)
                    else:
                        print(listagem)
            except IndexError:
                print("⚠️ Aviso: Não há pacientes aguardando na fila.")

        elif opcao == '6':
            print("Encerrando o sistema da UBS. Até logo!")
            break

        else:
            print("❌ Opção inválida. Escolha um número de 1 a 6.")
        print("")


if __name__ == "__main__":
    setup()
    main()

