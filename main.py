'''Sistema de elevador SENAC-DF

Integrantes do grupo:
João Vitor Moreira Bento
Tauã Rocha
Allana Kamilla
Aline karolly da silva macedo'''



import os
import time
from validacoes import validar_andar, formatar_andar
from sistema import SistemaElevadores

#ANSI escape codes pra formatação do texto no terminal
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho():
    limpar_tela()
    print(f"{CYAN}{'═'*50}{RESET}")
    print(f"{BOLD}{MAGENTA}🎓 SISTEMA DE ELEVADORES INTELIGENTES - FACULDADE{RESET}")
    print(f"{CYAN}{'═'*50}{RESET}\n")

def exibir_menu():
    print(f"{BOLD}Menu de Operações:{RESET}")
    print(f"1. {GREEN}📞 Solicitar Elevador{RESET}")
    print(f"2. {CYAN}📊 Status em Tempo Real{RESET}")
    print(f"3. {YELLOW}📈 Análise do Sistema{RESET}")
    print(f"4. {RED}❌ Encerrar Sistema{RESET}")
    print(f"\n{BOLD}Selecione a opção:{RESET} ", end="")

def main():
    sistema = SistemaElevadores()

    while True:
        exibir_cabecalho()
        exibir_menu()
        opcao = input().strip()

        if opcao == '1':
            print(f"\n{BOLD}--- Nova Solicitação ---{RESET}")
            try:
                andar_chamada = int(input("Andar de Origem: "))
                if not validar_andar(andar_chamada):
                    print(f"{RED}❌ Andar inválido! Intervalo: -2 a 4.{RESET}")
                    time.sleep(2) #congelar a tela por 2 segundos
                    continue

                andar_destino = int(input("Andar de Destino: "))
                if not validar_andar(andar_destino):
                    print(f"{RED}❌ Destino inválido! Intervalo: -2 a 4.{RESET}")
                    time.sleep(2)
                    continue

                is_pcd = input("Acessibilidade PcD? (S/N): ").strip().upper() == 'S'
                sistema.adicionar_chamada(andar_chamada, andar_destino, is_pcd)
                print(f"{GREEN}✅ Solicitação processada.{RESET}")
            except ValueError:
                print(f"{RED}❌ Erro: Insira valores numéricos inteiros.{RESET}")
                time.sleep(2)

        elif opcao == '2':
            print(f"\n{BOLD}--- Status dos Equipamentos ---{RESET}")
            for s in sistema.get_status():
                print(f"🔹 {s}")
            print("\n")
            input("Pressione Enter para retornar...") #congelar a tela até o usuário pressionar enter

        elif opcao == '3':
            print(f"\n{BOLD}--- Analytics & Performance ---{RESET}")
            resumo = sistema.estatisticas.obter_resumo()

            print(f"🏢 Hotspot (Mais Chamado): {formatar_andar(resumo['andar_mais_chamado'])}")
            print(f"📏 Desgaste (Andares Percorridos):")
            for i, dist in enumerate(resumo['distancia_elevadores']):
                print(f"   - Elevador {i}: {dist} andares")

            print(f"⏳ Latência Média de Espera: {resumo['tempo_medio_espera']:.2f}s")
            print(f"\n📊 Volume por Pavimento:")
            for andar, qtd in resumo['chamadas_por_andar'].items():
                print(f"   {formatar_andar(andar)}: {qtd} chamadas")
            print("\n")
            input("Pressione Enter para retornar...")

        elif opcao == '4':
            print(f"\n{YELLOW}Desligando sistemas... Até logo! 👋{RESET}")
            break
        else:
            print(f"{RED}❌ Opção inválida!{RESET}")
            time.sleep(1)

        if sistema.fila:
            print(f"\n{MAGENTA}⚙️  Despachando elevadores...{RESET}")
            sistema.processar_fila()

if __name__ == "__main__":
    main()
