import time
from collections import deque
from dataclasses import dataclass
from typing import List, Optional
from elevador import Elevador
from estatisticas import Estatisticas
from validacoes import ANDARES_VALIDOS

@dataclass
class Chamada:
    andar_chamada: int
    andar_destino: int
    is_pcd: bool
    timestamp: float

    def __repr__(self):
        tipo = "PcD" if self.is_pcd else "Normal"
        return f"Chamada({tipo}: {self.andar_chamada} -> {self.andar_destino})"

class SistemaElevadores:
    def __init__(self):
        self.elevadores = [Elevador(0), Elevador(1)]
        self.fila = deque()
        self.estatisticas = Estatisticas(num_elevadores=2)

    def adicionar_chamada(self, andar_chamada: int, andar_destino: int, is_pcd: bool = False):
        chamada = Chamada(andar_chamada, andar_destino, is_pcd, time.time())
        if is_pcd:
            self.fila.appendleft(chamada)
        else:
            self.fila.append(chamada)
        self.estatisticas.registrar_chamada(andar_chamada)

    def escolher_elevador(self, andar_chamada: int) -> Elevador:
        melhor_elevador = None
        menor_custo = float('inf')

        for e in self.elevadores:
            dist = abs(e.posicao - andar_chamada)
            custo = dist

            if e.ocupado:
                custo += 5

            if e.direcao == "Subindo" and andar_chamada > e.posicao:
                custo -= 2
            elif e.direcao == "Descendo" and andar_chamada < e.posicao:
                custo -= 2

            if custo < menor_custo:
                menor_custo = custo
                melhor_elevador = e
                #calcula qual elevador está mais perto do usuario

        return melhor_elevador

    def processar_fila(self):
        if not self.fila:
            return

        chamada = self.fila.popleft() #pega a primeira chamada da fila
        elevador = self.escolher_elevador(chamada.andar_chamada)
        elevador.ocupado = True

        self.estatisticas.registrar_espera(time.time() - chamada.timestamp)#registra o tempo de espera da chamada para fins de estatística
        print(f"\n🚀 Atendendo {chamada} com Elevador {elevador.id}")

        elevador.mover_para(chamada.andar_chamada, self.estatisticas)#move o elevador para o andar de chamada
        print(f"  [Elevador {elevador.id}] 🚪 Embarque no andar {chamada.andar_chamada}")

        elevador.mover_para(chamada.andar_destino, self.estatisticas)#move o elevador para o andar de destino
        print(f"  [Elevador {elevador.id}] 🚪 Desembarque no andar {chamada.andar_destino}")

        self._otimizar_rota(elevador)
        elevador.ocupado = False

    def _otimizar_rota(self, elevador: Elevador):
        if not self.fila:
            return

        for i in range(len(self.fila)):
            chamada = self.fila[i]
            if chamada.andar_chamada == elevador.posicao:
                del self.fila[i]
                print(f"\n✨ Otimização: Elevador {elevador.id} já está no andar {chamada.andar_chamada}, atendendo agora!")
                self.estatisticas.registrar_espera(time.time() - chamada.timestamp)#registra o tempo de espera da chamada
                elevador.mover_para(chamada.andar_destino, self.estatisticas)
                print(f"  [Elevador {elevador.id}] 🚪 Desembarque no andar {chamada.andar_destino}")
                self._otimizar_rota(elevador)
                return

    def get_status(self) -> List[str]:
        return [f"Elevador {e.id}: Andar {e.posicao} | {'Ocupado' if e.ocupado else 'Livre'} | {e.direcao or 'Parado'}" for e in self.elevadores]#retorna o status de cada elevador para exibição no menu de status
