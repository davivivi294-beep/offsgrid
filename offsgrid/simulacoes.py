import time
import random
from .ascii_art import (VERDE, VERDE_ESCURO, VERMELHO, AMARELO,
                        CIANO, RESET, NEGRITO, MONOPOLI)
from .ferramentas import limpar, digitar, barra, pausar


def glitch(tela, vezes=6):
    chars = "!@#$%&*<>/\\|01"
    for _ in range(vezes):
        linhas = tela.split("\n")
        nova = []
        for l in linhas:
            if l.strip() and random.random() < 0.3:
                l = "".join(random.choice(chars) if random.random() < 0.15 else c for c in l)
            nova.append(l)
        limpar()
        print(VERMELHO + "\n".join(nova) + RESET)
        time.sleep(0.08)


def piscar_nome(vezes=4):
    for _ in range(vezes):
        limpar()
        print(VERDE + NEGRITO + MONOPOLI + RESET)
        time.sleep(0.15)
        limpar()
        print(VERMELHO + NEGRITO + MONOPOLI.replace("offsgrid", "OFFSGRID") + RESET)
        time.sleep(0.15)


def sim_espelhamento():
    limpar()
    print(VERDE + NEGRITO + "=== [13] ESPELHAMENTO (SIMULADO) ===" + RESET)
    print()
    digitar("abrindo socket 5555...", 0.02)
    time.sleep(0.5)
    barra(2, "espelhando")
    digitar("injetando interface...", 0.02)
    time.sleep(0.5)
    glitch(MONOPOLI, vezes=6)
    limpar()
    print(VERDE + NEGRITO + MONOPOLI + RESET)
    piscar_nome(3)
    limpar()
    print(VERDE + NEGRITO + MONOPOLI + RESET)
    pausar()


def sim_monopoli():
    limpar()
    print(VERDE + NEGRITO + "=== [14] MONOPOLI (SIMULADO) ===" + RESET)
    print()
    digitar("preparando arte...", 0.02)
    barra(1.5, "renderizando")
    limpar()
    print(VERDE + NEGRITO + MONOPOLI + RESET)
    piscar_nome(4)
    limpar()
    print(VERDE + NEGRITO + MONOPOLI + RESET)
    pausar()


def sim_logs():
    limpar()
    print(VERDE + NEGRITO + "=== [15] LOGS (SIMULADO) ===" + RESET)
    print()
    logs = [
        "acesso root concedido (simulado)",
        "câmera acessada (simulado)",
        "galeria listada (simulado)",
        "microfone ouvindo (simulado)",
        "localização obtida (simulado)",
        "contatos exportados (simulado)",
        "mensagens lidas (simulado)",
        "backup criado (simulado)",
    ]
    for log in logs:
        ts = time.strftime("%H:%M:%S")
        print(f"{VERDE_ESCURO}[{ts}]{RESET} {VERMELHO}{log}{RESET}")
        time.sleep(0.35)
    pausar()
