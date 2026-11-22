import serial
import winsound
import csv
import os
import wave
import struct
import math
from datetime import datetime

PORTA = "COM5"
ARQUIVO_LOG = "alertas.csv"
ARQUIVO_SOM = "bip.wav"
LOCAL = "porta do quarto"

gatilho = 0

def criar_som():
    taxa = 44100
    amostras = bytearray()
    for _ in range(4):
        for i in range(int(taxa * 0.3)):
            valor = int(20000 * math.sin(2 * math.pi * 2500 * i / taxa))
            amostras += struct.pack("<h", valor)
        amostras += b"\x00\x00" * int(taxa * 0.1)
    with wave.open(ARQUIVO_SOM, "wb") as som:
        som.setnchannels(1)
        som.setsampwidth(2)
        som.setframerate(taxa)
        som.writeframes(bytes(amostras))

def sirene():
    winsound.PlaySound(ARQUIVO_SOM, winsound.SND_FILENAME | winsound.SND_ASYNC)

def registrar(evento, nivel=""):
    novo = not os.path.exists(ARQUIVO_LOG)
    with open(ARQUIVO_LOG, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        if novo:
            escritor.writerow(["data", "hora", "evento", "nivel", "gatilho", "local"])
        agora = datetime.now()
        escritor.writerow([
            agora.strftime("%Y-%m-%d"),
            agora.strftime("%H:%M:%S"),
            evento, nivel, gatilho, LOCAL
        ])

criar_som()
porta = serial.Serial(PORTA, 9600)
print("Calibrando... fique em silencio por 2 segundos.")

try:
    while True:
        linha = porta.readline().decode(errors="ignore").strip()

        try:
            if linha.startswith("G:"):
                gatilho = int(linha[2:])
                registrar("SISTEMA_ATIVADO")
                print(f"Pronto! Gatilho = {gatilho}. Alarme ativado.\n")

            elif linha.startswith("N:"):
                nivel = int(linha[2:])
                barra = "#" * min(nivel, 50)
                marca = "  <<< PASSOU" if nivel > gatilho else ""
                print(f"\rNivel: {nivel:4d} (gatilho {gatilho}) |{barra:<50}|{marca:<13}", end="", flush=True)

            elif linha.startswith("ALERTA:"):
                nivel = int(linha[7:])
                hora = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{hora}] ALERTA: barulho detectado! (nivel {nivel})")
                registrar("ALERTA_SOM", nivel)
                sirene()

        except ValueError:
            pass

except KeyboardInterrupt:
    registrar("SISTEMA_DESATIVADO")
    print("\nAlarme desligado. Log salvo em", ARQUIVO_LOG)