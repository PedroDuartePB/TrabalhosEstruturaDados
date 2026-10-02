from Arvores import ArvoreBusca, Heap
from ClassesAux import TipoAtendimento, Paciente

# A parte visual foi feita só para auxiliar na entrega com ajuda de IA
def exibir_menu() -> str:
    print("\n" + "=" * 35)
    print(" 🏥 SISTEMA DE GESTÃO DA UBS")
    print("=" * 35)
    print("1. Cadastrar paciente no sistema")
    print("2. Remover paciente do sistema")
    print("3. Registrar chegada na recepção (Fila)")
    print("4. Chamar próximo paciente (Atendimento)")
    print("5. Visualizar próximo da fila")
    print("6. Sair do sistema")
    return input("Escolha uma opção: ")


def main():
    ubs_cadastro = ArvoreBusca()
    agenda = Heap()

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
                ubs_cadastro.inserir(paciente, cpf)
                print(f"✅ Sucesso: Paciente '{nome}' cadastrado sob o CPF {cpf}.")
            except ValueError:
                print("❌ Erro: O CPF deve conter apenas números válidos.")

        elif opcao == '2':
            try:
                cpf = int(input("Digite o CPF do paciente a ser removido: "))
                removido = ubs_cadastro.remover(cpf)

                if removido is not None:
                    print(f"✅ Sucesso: Cadastro do paciente '{removido.paciente}' removido.")
                else:
                    print("⚠️ Aviso: Paciente não encontrado no sistema.")
            except ValueError:
                print("❌ Erro: O CPF deve ser numérico.")

        elif opcao == '3':
            try:
                cpf = int(input("Digite o CPF do paciente que chegou: "))

                paciente_encontrado = ubs_cadastro.buscar(cpf)
                if paciente_encontrado is not None:
                    idade = paciente_encontrado.paciente.idade
                    agenda.inserir(paciente_encontrado, idade)
                else:
                    print("Registro de paciente não cadastrado:")
                    nome = input("Por favor, insira o nome do paciente: ")
                    idade = int(input("Por favor, insira a idade do paciente: "))
                    paciente = Paciente(cpf, nome, idade, "n/a", TipoAtendimento.VACINACAO)
                    agenda.inserir(paciente, idade)
            except ValueError:
                print("❌ Erro: Entrada inválida. Use apenas números para CPF e prioridade.")
            finally:
                print(f"✅ Sucesso: Paciente cadastrado (Prioridade: {idade}).")


        elif opcao == '4':
            try:
                paciente_chamado = agenda.remover()
                if paciente_chamado is not None:
                    print("\n" + "*" * 40)
                    print(f" 📢 ATENDIMENTO: Encaminhar '{paciente_chamado.paciente.nome_completo}' ao consultório.")
                    print("*" * 40)
            except IndexError:
                print("⚠️ Aviso: A fila de espera está vazia no momento.")

        elif opcao == '5':
            try :
                proximo = agenda.get_topo()
                if proximo is not None:
                    print(f"👀 PRÓXIMO DA FILA: {proximo.paciente.nome_completo} (Chave de prioridade: {proximo.chave_busca})")
                else:
                    print("ERRO NA CHECAGEM DA FILA")
            except IndexError:
                print("⚠️ Aviso: Não há pacientes aguardando na fila.")

        elif opcao == '6':
            print("Encerrando o sistema da UBS. Até logo!")
            break

        else:
            print("❌ Opção inválida. Escolha um número de 1 a 6.")
        print("")


if __name__ == "__main__":
    main()

