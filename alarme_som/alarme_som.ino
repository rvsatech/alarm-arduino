unsigned long ultimoAlerta = 0;
int gatilho = 0;

int lerPico() {
  int maior = 0;
  int menor = 1023;
  unsigned long inicio = millis();
  while (millis() - inicio < 100) {
    int som = analogRead(A0);
    if (som > maior) {
      maior = som;
    }
    if (som < menor) {
      menor = som;
    }
  }
  return maior - menor;
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);

  int silencio = 0;
  for (int i = 0; i < 20; i++) {
    int pico = lerPico();
    if (pico > silencio) {
      silencio = pico;
    }
  }
  gatilho = silencio + 1;
  Serial.print("G:");
  Serial.println(gatilho);
}

void loop() {
  int nivel = lerPico();
  Serial.print("N:");
  Serial.println(nivel);

  if (nivel > gatilho) {
    digitalWrite(LED_BUILTIN, HIGH);
    if (millis() - ultimoAlerta > 500) {
      Serial.print("ALERTA:");
      Serial.println(nivel);
      ultimoAlerta = millis();
    }
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
