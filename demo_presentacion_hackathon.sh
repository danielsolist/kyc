#!/bin/bash

# 🎬 DEMO PARA PRESENTACIÓN HACKATHON
# Script optimizado para demostración en vivo

echo "🚀 KYC LIGHTNING ONBOARD - DEMO EN VIVO"
echo "========================================"
echo ""

# Verificar que el servidor esté corriendo
echo "🔍 Verificando conectividad..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Servidor KYC activo"
else
    echo "❌ Error: Servidor no disponible en puerto 8000"
    echo "   Ejecuta: python3.12 -m uvicorn main:app --port 8000"
    exit 1
fi

echo ""
echo "🎯 PROCESANDO KYC EN TIEMPO REAL..."
echo "Cliente: Ana Martínez López"
echo "CURP: CURP555666777ABCDEF"
echo ""

# Timestamp inicio
start_time=$(date +%s.%N)

# Comando principal del demo
echo "📡 Enviando solicitud a Saptiva AI..."
response=$(curl -s -X POST "http://localhost:8000/kyc/process-simple" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "DEMO_HACKATHON_LIVE",
    "personal_info": {
      "name": "Ana Martínez López",
      "id_number": "CURP555666777ABCDEF",
      "birth_date": "1992-07-20",
      "address": "Polanco 456, CDMX",
      "phone": "+52 55 5555 6666",
      "email": "ana.martinez@email.com"
    }
  }')

# Timestamp final
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)

echo ""
echo "⚡ RESULTADO EN ${duration} SEGUNDOS:"
echo "=================================="

# Parsear respuesta JSON de forma legible
echo "$response" | python3.12 -m json.tool

echo ""
echo "🎯 ANÁLISIS DEL RESULTADO:"

# Extraer campos clave
status=$(echo "$response" | python3.12 -c "import sys, json; data=json.load(sys.stdin); print(data.get('status', 'N/A'))")
approved=$(echo "$response" | python3.12 -c "import sys, json; data=json.load(sys.stdin); print(data.get('approved', 'N/A'))")
score=$(echo "$response" | python3.12 -c "import sys, json; data=json.load(sys.stdin); print(data.get('verification_score', 'N/A'))")
risk_level=$(echo "$response" | python3.12 -c "import sys, json; data=json.load(sys.stdin); print(data.get('risk_level', 'N/A'))")

if [ "$approved" = "True" ]; then
    echo "✅ CLIENTE APROBADO"
    echo "📊 Score de verificación: $score"
    echo "🎯 Nivel de riesgo: $risk_level"
    echo "⚡ Tiempo de procesamiento: ${duration}s"
else
    echo "❌ CLIENTE RECHAZADO"
    echo "📊 Score de verificación: $score"
    echo "🎯 Nivel de riesgo: $risk_level"
fi

echo ""
echo "🧠 MODELOS SAPTIVA UTILIZADOS:"
echo "• Saptiva OCR - Extracción de documentos"
echo "• Saptiva Guard - Validación de compliance"
echo "• Saptiva Ops - Análisis de riesgo"
echo "• Saptiva KAL - Function calling especializado"

echo ""
echo "🛡️ EJECUTANDO VALIDACIÓN DE COMPLIANCE CON APIS REALES..."
curl -s -X POST "http://localhost:8000/kyc/validate-compliance" \
  -H "Content-Type: application/json" \
  -d '{"identity_verified": true, "credit_score": 720, "sanctions_clear": true, "documents_validated": ["INE", "CURP", "Comprobante_domicilio"]}' > /dev/null

echo ""
echo "💰 COSTOS REALES GENERADOS (SAPTIVA APIs):"
curl -s "http://localhost:8000/billing/session-summary" | python3.12 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    session = data.get('billing_summary', {}).get('session_summary', {})
    models = data.get('billing_summary', {}).get('models_breakdown', {})
    print(f'• Total: \${session.get(\"total_cost\", 0):.6f} USD')
    print(f'• Llamadas reales: {session.get(\"total_calls\", 0)}')
    print(f'• Tokens procesados: {session.get(\"total_tokens\", 0)}')
    print(f'• Modelos usados: {session.get(\"models_count\", 0)}')
    for model, stats in models.items():
        print(f'  - {model}: {stats.get(\"calls\", 0)} calls, \${stats.get(\"total_cost\", 0):.6f}')
except Exception as e:
    print(f'• Error: {e}')
"

echo ""
echo "🎬 DEMO COMPLETADO"
echo "=================="
echo "🏆 De DÍAS a SEGUNDOS con Saptiva AI"
echo "🚀 KYC Lightning Onboard - Hackathon 2024"
echo ""

# Opcional: Mostrar compliance validation
echo "🛡️ VALIDACIÓN DE COMPLIANCE (OPCIONAL):"
echo "curl -X POST localhost:8000/kyc/validate-compliance \\"
echo "  -d '{\"identity_verified\": true, \"credit_score\": 720, \"sanctions_clear\": true}'"
echo ""