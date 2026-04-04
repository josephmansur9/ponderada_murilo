# Leitura da porta serial do Arduino
import requests, time, random

URL = 'http://localhost:5001/leituras'

def simular_estacao():
    print("Iniciando simulação de dados... (Ctrl+C para parar)")
    while True:
        dados = {
            "temperatura": round(random.uniform(20.0, 30.0), 2),
            "umidade": round(random.uniform(40.0, 70.0), 2),
            "pressao": round(random.uniform(1010.0, 1015.0), 2)
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(URL, json=dados, headers=headers)
            print(f"Enviado: {dados} | Status: {response.status_code}")
        except Exception as e:
            print(f"Erro ao conectar na API: {e}")
        time.sleep(5) # Envia a cada 5 segundos [cite: 78]

if __name__ == '__main__':
    simular_estacao()