# Alarm Arduino

Alarme de intrusão por som com Arduino Uno e Python. O sensor de som fica perto da porta; quando detecta um barulho acima do nível ambiente, o Arduino envia um alerta pela porta serial e o PC toca um alarme e registra o evento em log.

## Hardware

- Arduino Uno (clone com CH340)
- Módulo sensor de som (microfone + LM393)

| Sensor | Arduino |
|---|---|
| AO | A0 |
| G | GND |
| + | 5V |

## Como funciona

1. Ao ligar, o Arduino mede o ruído ambiente por 2 segundos e define o gatilho (ruído + 1).
2. A cada 100 ms, mede a amplitude do som (pico máximo − mínimo) e envia `N:<nível>`.
3. Quando o nível passa do gatilho, envia `ALERTA:<nível>` (no máximo 1 a cada 500 ms).
4. O `alarm.py` lê a serial, mostra o nível ao vivo, toca o alarme e grava o evento em `alertas.csv`.

## Uso

1. Envie `alarme_som/alarme_som.ino` para o Arduino pela Arduino IDE.
2. Ajuste a porta em `alarm.py` (`PORTA = "COM5"`).
3. Instale e rode:

```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python alarm.py
```

Fique em silêncio nos primeiros 2 segundos (calibração). `Ctrl + C` encerra.

## Log

`alertas.csv` (separado por `;`):

```
data;hora;evento;nivel;gatilho;local
2026-11-22;19:45:02;SISTEMA_ATIVADO;;8;porta do quarto
2026-11-22;19:51:37;ALERTA_SOM;23;8;porta do quarto
2026-11-22;20:00:15;SISTEMA_DESATIVADO;;8;porta do quarto
```

> Feche o Serial Monitor/Plotter da IDE antes de rodar o `alarm.py`: só um programa pode usar a porta COM por vez.
