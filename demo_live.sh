#!/bin/bash

# 🚀 KYC Lightning Onboard - Demo en Vivo para Hackathon
# Ejecuta este script durante tu presentación

echo "🚀 KYC Lightning Onboard - Demo en Vivo"
echo "========================================"
echo ""

echo "📋 Cliente de ejemplo: Ana Martínez"
echo "⏱️  Iniciando procesamiento KYC..."
echo ""

# Comando principal del demo
curl -X POST "http://localhost:8000/kyc/process-simple" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "HACKATHON_LIVE_DEMO", 
    "personal_info": {
      "name": "Ana Martínez Rodríguez",
      "id_number": "CURP555666777ABC",
      "birth_date": "1992-07-20",
      "address": "Av. Polanco 456, CDMX",
      "phone": "+52 55 5555 6666",
      "email": "ana.martinez@email.com"
    }
  }' | jq '.'

echo ""
echo "✅ ¡KYC procesado exitosamente!"
echo ""

echo "📊 Estadísticas del sistema:"
echo "----------------------------"
curl -s http://localhost:8000/kyc/stats | jq '.'

echo ""
echo "🎯 Estado del cliente procesado:"
echo "--------------------------------"
curl -s http://localhost:8000/kyc/status/HACKATHON_LIVE_DEMO | jq '.'

echo ""
echo "🚀 ¡Demo completado! Tiempo total: ~3 segundos"