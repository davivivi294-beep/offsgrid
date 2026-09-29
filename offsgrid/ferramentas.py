import socket
import subprocess
import platform
import hashlib
import base64
import secrets
import string
import time
import os
import sys

try:
    import psutil
except ImportError:
    psutil = None

try:
    import requests
except ImportError:
    requests = None

try:
    import qrcode
except ImportError:
    qrcode = None

from .ascii_art import (VERDE, VERDE_ESCURO, VERMELHO, AMARELO,
                        CIANO, BRANCO, RESET, NEGRITO)


def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def digitar(texto, delay=0.02, cor=VERDE):
    for c in texto:
        sys.stdout.write(cor + c + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def barra(segundos=1.5, label="processando"):
    largura = 40
    for i in range(largura + 1):
        preenchido = "█" * i
        vazio = "░" * (largura - i)
        pct = int((i / largura) * 100)
        sys.stdout.write(f"\r{VERDE}{label} [{preenchido}{vazio}] {pct}%{RESET}")
        sys.stdout.flush()
        time.sleep(segundos / largura)
    print()

def pausar(msg="pressione ENTER para voltar..."):
    input(f"\n{VERDE_ESCURO}{msg}{RESET}")


def scan_rede():
    limpar()
    print(VERDE + NEGRITO + "=== [1] SCAN DE REDE (REAL) ===" + RESET)
    print()
    digitar("descobrindo IP local...", 0.02)
    try:
        hostname = socket.gethostname()
        ip_local = socket.gethostbyname(hostname)
    except Exception:
        ip_local = "127.0.0.1"
    print(f"  {CIANO}hostname:{RESET} {hostname}")
    print(f"  {CIANO}IP local:{RESET} {ip_local}")
    print()
    base = ".".join(ip_local.split(".")[:3])
    digitar(f"varrendo faixa {base}.1 até {base}.254 ...", 0.02)
    print()
    encontrados = []
    for i in range(1, 255):
        ip = f"{base}.{i}"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.05)
            if s.connect_ex((ip, 80)) == 0:
                encontrados.append(ip)
                print(f"  {VERDE}[ATIVO]{RESET} {ip}")
            s.close()
        except Exception:
            pass
    if not encontrados:
        print(f"  {AMARELO}(nenhum host com porta 80 aberta){RESET}")
    print()
    digitar(f"varredura concluída. {len(encontrados)} ativo(s).", 0.02, VERDE_ESCURO)
    pausar()


def scan_portas():
    limpar()
    print(VERDE + NEGRITO + "=== [2] SCAN DE PORTAS (REAL) ===" + RESET)
    print()
    alvo = input(f"{VERDE}IP/domínio (padrão 127.0.0.1): {RESET}").strip() or "127.0.0.1"
    try:
        ip = socket.gethostbyname(alvo)
    except Exception:
        print(f"{VERMELHO}[!] não resolvido{RESET}")
        pausar()
        return
    print(f"{CIANO}alvo:{RESET} {alvo} ({ip})\n")
    portas = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
    abertas = []
    for p in portas:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.4)
        if s.connect_ex((ip, p)) == 0:
            abertas.append(p)
            print(f"  {VERDE}[ABERTA]{RESET} {p}")
        else:
            print(f"  {VERMELHO}[FECHADA]{RESET} {p}")
        s.close()
    print()
    digitar(f"scan concluído. {len(abertas)} aberta(s).", 0.02, VERDE_ESCURO)
    pausar()


def info_sistema():
    limpar()
    print(VERDE + NEGRITO + "=== [3] INFO DO SISTEMA (REAL) ===" + RESET)
    print()
    print(f"  {CIANO}sistema:{RESET} {platform.system()} {platform.release()}")
    print(f"  {CIANO}versão:{RESET} {platform.version()}")
    print(f"  {CIANO}máquina:{RESET} {platform.machine()}")
    print(f"  {CIANO}processador:{RESET} {platform.processor()}")
    print(f"  {CIANO}python:{RESET} {platform.python_version()}")
    print(f"  {CIANO}hostname:{RESET} {socket.gethostname()}")
    if psutil:
        try:
            print(f"  {CIANO}CPU:{RESET} {psutil.cpu_count()} núcleos - {psutil.cpu_percent(interval=0.5)}%")
            m = psutil.virtual_memory()
            print(f"  {CIANO}RAM:{RESET} {m.total // (1024**2)} MB - {m.percent}%")
            d = psutil.disk_usage("/")
            print(f"  {CIANO}disco:{RESET} {d.total // (1024**3)} GB - {d.percent}%")
        except Exception:
            pass
    pausar()


def hash_tool():
    limpar()
    print(VERDE + NEGRITO + "=== [4] HASH (REAL) ===" + RESET)
    print()
    print("  [1] texto\n  [2] arquivo")
    op = input(f"{VERDE}opção > {RESET}").strip()
    if op == "1":
        dados = input(f"{VERDE}texto: {RESET}").encode()
    elif op == "2":
        c = input(f"{VERDE}caminho: {RESET}").strip()
        if not os.path.isfile(c):
            print(f"{VERMELHO}[!] não encontrado{RESET}")
            pausar()
            return
        with open(c, "rb") as f:
            dados = f.read()
    else:
        return
    print()
    print(f"  {CIANO}MD5:{RESET}    {hashlib.md5(dados).hexdigest()}")
    print(f"  {CIANO}SHA1:{RESET}   {hashlib.sha1(dados).hexdigest()}")
    print(f"  {CIANO}SHA256:{RESET} {hashlib.sha256(dados).hexdigest()}")
    pausar()


def base64_tool():
    limpar()
    print(VERDE + NEGRITO + "=== [5] BASE64 (REAL) ===" + RESET)
    print()
    print("  [1] codificar\n  [2] decodificar")
    op = input(f"{VERDE}opção > {RESET}").strip()
    if op == "1":
        t = input(f"{VERDE}texto: {RESET}")
        print(f"\n{CIANO}resultado:{RESET} {base64.b64encode(t.encode()).decode()}")
    elif op == "2":
        t = input(f"{VERDE}base64: {RESET}")
        try:
            print(f"\n{CIANO}resultado:{RESET} {base64.b64decode(t.encode()).decode()}")
        except Exception:
            print(f"{VERMELHO}[!] inválido{RESET}")
    pausar()


def gerador_senha():
    limpar()
    print(VERDE + NEGRITO + "=== [6] GERADOR DE SENHA (REAL) ===" + RESET)
    print()
    try:
        tam = int(input(f"{VERDE}tamanho (padrão 16): {RESET}") or "16")
    except ValueError:
        tam = 16
    alf = string.ascii_letters + string.digits + "!@#$%&*()-_=+"
    s = "".join(secrets.choice(alf) for _ in range(tam))
    print(f"\n  {CIANO}senha:{RESET} {NEGRITO}{VERDE}{s}{RESET}")
    print(f"  {CIANO}entropia:{RESET} ~{tam * 6} bits")
    pausar()


def dns_lookup():
    limpar()
    print(VERDE + NEGRITO + "=== [7] DNS LOOKUP (REAL) ===" + RESET)
    print()
    h = input(f"{VERDE}domínio: {RESET}").strip()
    if not h:
        return
    try:
        ip = socket.gethostbyname(h)
        print(f"\n  {CIANO}{h}{RESET} -> {VERDE}{ip}{RESET}")
        try:
            nome, _, ips = socket.gethostbyname_ex(h)
            print(f"  {CIANO}canônico:{RESET} {nome}")
            for i in ips:
                print(f"  {CIANO}IP:{RESET} {i}")
        except Exception:
            pass
    except Exception:
        print(f"{VERMELHO}[!] não resolvido{RESET}")
    pausar()


def http_probe():
    limpar()
    print(VERDE + NEGRITO + "=== [8] HTTP PROBE (REAL) ===" + RESET)
    print()
    if not requests:
        print(f"{VERMELHO}[!] instale requests{RESET}")
        pausar()
        return
    url = input(f"{VERDE}URL: {RESET}").strip()
    if not url:
        return
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = requests.get(url, timeout=6)
        print(f"\n  {CIANO}status:{RESET} {r.status_code}")
        print(f"  {CIANO}tempo:{RESET} {r.elapsed.total_seconds()}s")
        print(f"  {CIANO}tamanho:{RESET} {len(r.content)} bytes")
        print(f"\n  {CIANO}headers:{RESET}")
        for k, v in r.headers.items():
            print(f"    {VERDE}{k}{RESET}: {v}")
    except Exception as e:
        print(f"{VERMELHO}[!] {e}{RESET}")
    pausar()


def qr_generator():
    limpar()
    print(VERDE + NEGRITO + "=== [9] QR CODE (REAL) ===" + RESET)
    print()
    if not qrcode:
        print(f"{VERMELHO}[!] instale qrcode[pil]{RESET}")
        pausar()
        return
    t = input(f"{VERDE}texto/URL: {RESET}").strip()
    if not t:
        return
    nome = input(f"{VERDE}arquivo (padrão qr.png): {RESET}").strip() or "qr.png"
    if not nome.endswith(".png"):
        nome += ".png"
    qrcode.make(t).save(nome)
    print(f"\n{VERDE}[✔] salvo em {nome}{RESET}")
    pausar()


def ping_host():
    limpar()
    print(VERDE + NEGRITO + "=== [10] PING (REAL) ===" + RESET)
    print()
    h = input(f"{VERDE}host: {RESET}").strip()
    if not h:
        return
    p = "-n" if os.name == "nt" else "-c"
    try:
        r = subprocess.run(["ping", p, "4", h], capture_output=True, text=True, timeout=15)
        print(r.stdout)
    except Exception as e:
        print(f"{VERMELHO}[!] {e}{RESET}")
    pausar()


def monitor_rede():
    limpar()
    print(VERDE + NEGRITO + "=== [11] MONITOR DE REDE (REAL) ===" + RESET)
    print()
    if not psutil:
        print(f"{VERMELHO}[!] instale psutil{RESET}")
        pausar()
        return
    try:
        print(f"{VERDE_ESCURO}(ctrl+c pra parar){RESET}\n")
        a = psutil.net_io_counters()
        while True:
            time.sleep(1)
            b = psutil.net_io_counters()
            env = (b.bytes_sent - a.bytes_sent) / 1024
            rec = (b.bytes_recv - a.bytes_recv) / 1024
            print(f"\r{CIANO}↑ {env:8.2f} KB/s  ↓ {rec:8.2f} KB/s{RESET}", end="")
            a = b
    except KeyboardInterrupt:
        print()
    pausar()


def gerar_payload_simulado():
    limpar()
    print(VERDE + NEGRITO + "=== [12] PAYLOAD (SIMULADO) ===" + RESET)
    print()
    digitar("montando payload educacional...", 0.02)
    barra(1.5, "compilando")
    nome = f"payload_{secrets.token_hex(4)}.bin"
    print(f"\n{VERDE}[✔] gerado: {nome}{RESET}")
    print(f"{AMARELO}⚠ arquivo NÃO executável. apenas simbólico.{RESET}")
    pausar()
