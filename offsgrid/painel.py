import sys
import time
import getpass
import shutil

from .ascii_art import (BANNER, MONOPOLI, NOME, SENHA,
                        VERDE, VERDE_ESCURO, VERMELHO, AMARELO,
                        CIANO, BRANCO, RESET, NEGRITO)
from .ferramentas import (
    limpar, digitar, barra, pausar,
    scan_rede, scan_portas, info_sistema, hash_tool, base64_tool,
    gerador_senha, dns_lookup, http_probe, qr_generator,
    ping_host, monitor_rede, gerar_payload_simulado,
)
from .simulacoes import sim_espelhamento, sim_monopoli, sim_logs


def tela_login():
    limpar()
    print(BANNER)
    print(VERDE_ESCURO + "─" * 60 + RESET)
    print(f"{VERMELHO}{NEGRITO}  🔒 ACESSO RESTRITO{RESET}")
    print(VERDE_ESCURO + "─" * 60 + RESET)
    time.sleep(0.4)

    tentativas = 3
    while tentativas > 0:
        try:
            senha = getpass.getpass(f"{VERDE}  senha > {RESET}")
        except Exception:
            senha = input(f"{VERDE}  senha > {RESET}")

        if senha == SENHA:
            print(f"{VERDE}[✔] senha correta. abrindo painel...{RESET}")
            barra(1.5, "autenticando")
            return True
        tentativas -= 1
        print(f"{VERMELHO}[✘] incorreta. restam: {tentativas}{RESET}")
        time.sleep(0.8)

    print(f"{VERMELHO}{NEGRITO}[!] BLOQUEADO.{RESET}")
    time.sleep(2)
    return False


def menu():
    while True:
        limpar()
        print(BANNER)
        largura = min(shutil.get_terminal_size().columns, 62)
        print(VERDE_ESCURO + "─" * largura + RESET)
        print(f"{NEGRITO}{BRANCO}  PAINEL DE FERRAMENTAS{RESET}")
        print(VERDE_ESCURO + "─" * largura + RESET)
        print(f"  {CIANO}== REAIS =={RESET}")
        print(f"  {VERDE}[1]{RESET}  scan de rede")
        print(f"  {VERDE}[2]{RESET}  scan de portas")
        print(f"  {VERDE}[3]{RESET}  info do sistema")
        print(f"  {VERDE}[4]{RESET}  hash de arquivo/texto")
        print(f"  {VERDE}[5]{RESET}  base64 encode/decode")
        print(f"  {VERDE}[6]{RESET}  gerador de senha")
        print(f"  {VERDE}[7]{RESET}  DNS lookup")
        print(f"  {VERDE}[8]{RESET}  HTTP probe")
        print(f"  {VERDE}[9]{RESET}  gerador de QR code")
        print(f"  {VERDE}[10]{RESET} ping em host")
        print(f"  {VERDE}[11]{RESET} monitor de rede")
        print(f"  {AMARELO}== SIMULADAS =={RESET}")
        print(f"  {AMARELO}[12]{RESET} gerador de payload (simulado)")
        print(f"  {AMARELO}[13]{RESET} espelhamento de tela (simulado)")
        print(f"  {AMARELO}[14]{RESET} exibir monopoli (simulado)")
        print(f"  {AMARELO}[15]{RESET} logs do sistema (simulado)")
        print(f"  {VERMELHO}[0]{RESET}  sair")
        print(VERDE_ESCURO + "─" * largura + RESET)

        op = input(f"{VERDE}{NOME}> {RESET}").strip()

        acoes = {
            "1": scan_rede, "2": scan_portas, "3": info_sistema,
            "4": hash_tool, "5": base64_tool, "6": gerador_senha,
            "7": dns_lookup, "8": http_probe, "9": qr_generator,
            "10": ping_host, "11": monitor_rede, "12": gerar_payload_simulado,
            "13": sim_espelhamento, "14": sim_monopoli, "15": sim_logs,
        }

        if op == "0":
            limpar()
            print(BANNER)
            digitar("encerrando sessão...", 0.03, VERMELHO)
            time.sleep(0.8)
            digitar("desconectando offsgrid...", 0.03, VERMELHO)
            time.sleep(0.8)
            print(VERDE_ESCURO + "\n[ sessão finalizada ]" + RESET)
            sys.exit(0)
        elif op in acoes:
            acoes[op]()
        else:
            print(f"{VERMELHO}[!] opção inválida{RESET}")
            time.sleep(1)


def main():
    if not tela_login():
        return
    menu()


if __name__ == "__main__":
    main()
