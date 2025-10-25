#!/usr/bin/env python3
"""
Test simple para verificar la nueva API key de Saptiva
"""
import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_saptiva_api():
    """Test básico de la API de Saptiva"""
    print("🚀 Probando nueva API key de Saptiva...")
    
    api_key = os.getenv("SAPTIVA_API_KEY")
    if not api_key:
        print("❌ Error: SAPTIVA_API_KEY no encontrada en .env")
        return
    
    print(f"🔑 API Key: {api_key[:20]}...")
    
    # Test endpoint de chat
    url = "https://api.saptiva.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "Saptiva Ops",
        "messages": [
            {
                "role": "user",
                "content": "Analiza el riesgo crediticio de un cliente con score 720 y sin historial de sanciones."
            }
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        print("📡 Enviando solicitud a Saptiva...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API funcionando correctamente!")
            print(f"🤖 Modelo: {result.get('model', 'N/A')}")
            print(f"💬 Respuesta: {result['choices'][0]['message']['content'][:100]}...")
            
            # Mostrar uso de tokens
            usage = result.get('usage', {})
            print(f"🔢 Tokens: {usage.get('total_tokens', 0)}")
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {str(e)}")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    test_saptiva_api()