# 🎭 offsgrid

Painel educacional de **cyber security** com ferramentas reais e simulações visuais inspiradas na cultura hacker.

![python](https://img.shields.io/badge/python-3.8%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![status](https://img.shields.io/badge/status-educacional-orange)

---

## ⚠️ AVISO EDUCACIONAL

Este projeto é **100% educacional**.

- As ferramentas **reais** operam **apenas na própria máquina/rede do usuário**.
- As ferramentas **simuladas** **não acessam nenhum dispositivo** — são apenas demonstração visual.
- É **proibido** usar este projeto para acessar dispositivos de terceiros (crime — Lei 12.737/2012).

---

## 🚀 Instalação

```bash
git clone https://github.com/SEU_USUARIO/offsgrid.git
cd offsgrid
pip install -r requirements.txt
pip install -e .
offsgrid
```

## 🔑 Senha padrão

```
offsgrid2026
```

Troque em `offsgrid/ascii_art.py`:

```python
SENHA = "offsgrid2026"
```

---

## ✨ Funcionalidades

### 🔧 Reais
| # | Ferramenta | Descrição |
|---|---|---|
| 1 | Scan de rede | Descobre dispositivos na sua rede Wi-Fi |
| 2 | Scan de portas | Testa portas abertas em IPs/domínios |
| 3 | Info do sistema | SO, CPU, RAM, disco |
| 4 | Hash | MD5 / SHA1 / SHA256 de texto ou arquivo |
| 5 | Base64 | Codifica / decodifica |
| 6 | Gerador de senha | Senhas fortes com `secrets` |
| 7 | DNS lookup | Resolve domínio → IP |
| 8 | HTTP probe | Status + headers de sites |
| 9 | QR code | Gera QR e salva PNG |
| 10 | Ping | Testa conectividade |
| 11 | Monitor de rede | Tráfego em tempo real |

### 🎬 Simuladas
| # | Ferramenta | Descrição |
|---|---|---|
| 12 | Payload | Gera nome fictício de arquivo |
| 13 | Espelhamento | Glitch visual + monopoli |
| 14 | Monopoli | ASCII art piscando |
| 15 | Logs | Logs "assustadores" com timestamp |

---

## 📁 Estrutura

```
offsgrid/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── .gitignore
└── offsgrid/
    ├── __init__.py
    ├── __main__.py
    ├── ascii_art.py
    ├── ferramentas.py
    ├── simulacoes.py
    └── painel.py
```

---

## 📜 Licença

MIT
