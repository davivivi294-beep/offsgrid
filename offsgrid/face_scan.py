"""
Módulo de reconhecimento facial educacional do offsgrid.

⚠️  AVISO: isto NÃO é Face ID. É reconhecimento facial com webcam comum.
    Face ID real usa sensor infravermelho + depth + chip dedicado.
    Este módulo é 100% educacional e fácil de burlar com uma foto.
"""

import os
import time

try:
    import cv2
except ImportError:
    cv2 = None

from .ascii_art import (VERDE, VERDE_ESCURO, VERMELHO, AMARELO,
                        CIANO, BRANCO, RESET, NEGRITO)
from .ferramentas import limpar, digitar, barra, pausar


# ---------- CONFIG ----------
PASTA_FOTOS = "fotos_usuarios"
ARQUIVO_FOTO = "meu_rosto.jpg"
LIMIAR_CONFIANCA = 70  # 0 a 100 — quanto maior, mais rígido


def _checar_opencv():
    if cv2 is None:
        limpar()
        print(f"{VERMELHO}[!] OpenCV não instalado.{RESET}")
        print(f"{AMARELO}instale com: pip install opencv-python{RESET}")
        pausar()
        return False
    return True


def _detector():
    # procura o arquivo em vários lugares possíveis
    import os
    candidatos = [
        "haarcascade_frontalface_default.xml",  # pasta atual
        os.path.join(os.path.dirname(__file__), "..", "haarcascade_frontalface_default.xml"),
        os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml"),
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
    ]
    for caminho in candidatos:
        if os.path.isfile(caminho):
            det = cv2.CascadeClassifier(caminho)
            if not det.empty():
                return det
    # se nada funcionou, tenta o padrão (vai dar erro, mas avisa)
    print("[!] ATENÇÃO: haarcascade_frontalface_default.xml não encontrado.")
    print("[!] baixe de: https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml")
    print("[!] e coloque em:", os.getcwd())
    return cv2.CascadeClassifier()

# ---------- 1. DETECÇÃO SIMPLES ----------
def face_detect():
    """Só detecta rostos na webcam e desenha um quadrado."""
    if not _checar_opencv():
        return

    limpar()
    print(VERDE + NEGRITO + "=== [FACE] DETECÇÃO DE ROSTO ===" + RESET)
    print(f"{VERDE_ESCURO}(pressione 'q' na janela pra sair){RESET}\n")

    det = _detector()
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print(f"{VERMELHO}[!] Não consegui abrir a webcam.{RESET}")
        pausar()
        return

    try:
        while True:
            ok, frame = cam.read()
            if not ok:
                break

            cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rostos = det.detectMultiScale(cinza, 1.3, 5)

            for (x, y, w, h) in rostos:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "ROSTO DETECTADO", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.putText(frame, "offsgrid - face scan", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("offsgrid - face scan", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()

    pausar()


# ---------- 2. CADASTRAR ROSTO ----------
def face_cadastrar():
    """Tira uma foto do usuário e salva pra reconhecimento futuro."""
    if not _checar_opencv():
        return

    limpar()
    print(VERDE + NEGRITO + "=== [FACE] CADASTRAR ROSTO ===" + RESET)
    print()
    digitar("posicione o rosto na câmera...", 0.02)
    time.sleep(1)

    det = _detector()
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print(f"{VERMELHO}[!] Não consegui abrir a webcam.{RESET}")
        pausar()
        return

    os.makedirs(PASTA_FOTOS, exist_ok=True)
    caminho = os.path.join(PASTA_FOTOS, ARQUIVO_FOTO)

    capturado = False
    try:
        while True:
            ok, frame = cam.read()
            if not ok:
                break

            cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rostos = det.detectMultiScale(cinza, 1.3, 5)

            for (x, y, w, h) in rostos:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "PRESSIONE ESPACO", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("offsgrid - cadastrar rosto", frame)
            tecla = cv2.waitKey(1) & 0xFF

            if tecla == ord(" ") and len(rostos) > 0:
                cv2.imwrite(caminho, frame)
                capturado = True
                print(f"\n{VERDE}[✔] rosto salvo em {caminho}{RESET}")
                break
            elif tecla == ord("q"):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()

    if not capturado:
        print(f"{AMARELO}[!] nada foi salvo.{RESET}")
    pausar()


# ---------- 3. RECONHECER ROSTO ----------
def face_reconhecer():
    """Compara o rosto da webcam com a foto cadastrada."""
    if not _checar_opencv():
        return

    limpar()
    print(VERDE + NEGRITO + "=== [FACE] RECONHECER ROSTO ===" + RESET)
    print()

    caminho = os.path.join(PASTA_FOTOS, ARQUIVO_FOTO)
    if not os.path.isfile(caminho):
        print(f"{VERMELHO}[!] nenhuma foto cadastrada.{RESET}")
        print(f"{AMARELO}use a opção 'cadastrar rosto' primeiro.{RESET}")
        pausar()
        return

    # carrega o reconhecedor LBPH (vem com opencv-contrib)
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except AttributeError:
        print(f"{VERMELHO}[!] precisa do opencv-contrib-python.{RESET}")
        print(f"{AMARELO}instale: pip install opencv-contrib-python{RESET}")
        pausar()
        return

    # treina com a foto salva
    import numpy as np
    img = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
    det = _detector()
    rostos = det.detectMultiScale(img, 1.3, 5)
    if len(rostos) == 0:
        print(f"{VERMELHO}[!] não achei rosto na foto salva.{RESET}")
        pausar()
        return

    (x, y, w, h) = rostos[0]
    rosto_treino = img[y:y + h, x:x + w]
    recognizer.train([rosto_treino], np.array([1]))

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print(f"{VERMELHO}[!] não consegui abrir webcam.{RESET}")
        pausar()
        return

    digitar("comparando rostos... (pressione 'q' pra sair)", 0.02)
    time.sleep(0.5)

    try:
        while True:
            ok, frame = cam.read()
            if not ok:
                break

            cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rostos = det.detectMultiScale(cinza, 1.3, 5)

            for (x, y, w, h) in rostos:
                rosto = cinza[y:y + h, x:x + w]
                try:
                    label, conf = recognizer.predict(rosto)
                    # conf baixa = mais parecido (0 = idêntico)
                    if conf < LIMIAR_CONFIANCA:
                        texto = f"ACESSO LIBERADO ({int(100 - conf)}%)"
                        cor = (0, 255, 0)
                    else:
                        texto = f"ACESSO NEGADO ({int(100 - conf)}%)"
                        cor = (0, 0, 255)
                except Exception:
                    texto = "?"
                    cor = (0, 255, 255)

                cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 2)
                cv2.putText(frame, texto, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)

            cv2.imshow("offsgrid - reconhecimento", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()

    pausar()
