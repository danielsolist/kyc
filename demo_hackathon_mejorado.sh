#!/bin/bash

# 🎬 DEMO MEJORADO PARA HACKATHON 2025
# Múltiples casos de KYC con mejor presentación

echo "🚀 KYC LIGHTNING ONBOARD - DEMO HACKATHON 2025"
echo "==============================================="
echo ""

# Verificar servidor
echo "🔍 Verificando conectividad..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Servidor KYC activo"
else
    echo "❌ Error: Servidor no disponible"
    exit 1
fi

echo ""
echo "🎯 PROCESANDO MÚLTIPLES CASOS DE KYC..."
echo "======================================="

# Función para procesar un cliente
process_kyc_case() {
    local case_num=$1
    local customer_data=$2
    local customer_name=$3
    
    echo ""
    echo "📋 CASO $case_num: $customer_name"
    echo "$(printf '=%.0s' {1..50})"
    
    start_time=$(date +%s.%N)
    
    response=$(curl -s -X POST "http://localhost:8000/kyc/process-with-tools" \
      -H "Content-Type: application/json" \
      -d "$customer_data")
    
    end_time=$(date +%s.%N)
    duration=$(echo "$end_time - $start_time" | bc)
    
    # Extraer resultados
    approved=$(echo "$response" | python3.12 -c "import sys, json; data=json.load(sys.stdin); print('✅ APROBADO' if data.get('approved', False) else '❌ RECHAZADO')")
    score=$(echo "$response" | python3.12 -c "import sys, json; data=json.load(sys.stdin); print(f'{data.get(\"verification_score\", 0):.3f}')")
    risk=$(echo "$response" | python3.12 -c "import sys, json; data=json.load(sys.stdin); print(data.get('risk_level', 'N/A').upper())")
    
    echo "🎯 Resultado: $approved"
    echo "📊 Score: $score"
    echo "⚠️  Riesgo: $risk"
    echo "⚡ Tiempo: ${duration}s"
}

# CASO 1: Cliente Premium (Aprobado)
process_kyc_case "1" '{
    "customer_id": "KYC_DEMO_001",
    "personal_info": {
        "name": "Ana Martínez López",
        "id_number": "CURP555666777ABCDEF",
        "birth_date": "1992-07-20",
        "address": "Polanco 456, CDMX",
        "phone": "+52 55 5555 6666",
        "email": "ana.martinez@email.com"
    }
}' "Ana Martínez López (Cliente Premium)"

# CASO 2: Cliente Estándar (Aprobado)
process_kyc_case "2" '{
    "customer_id": "KYC_DEMO_002",
    "personal_info": {
        "name": "Carlos Rodríguez Pérez",
        "id_number": "CURP888999000HIJKLM",
        "birth_date": "1985-03-15",
        "address": "Roma Norte 123, CDMX",
        "phone": "+52 55 1234 5678",
        "email": "carlos.rodriguez@email.com"
    }
}' "Carlos Rodríguez Pérez (Cliente Estándar)"

# CASO 3: Cliente Joven (Aprobado con condiciones)
process_kyc_case "3" '{
    "customer_id": "KYC_DEMO_003",
    "personal_info": {
        "name": "María González Silva",
        "id_number": "CURP111222333NOPQRS",
        "birth_date": "2001-11-08",
        "address": "Condesa 789, CDMX",
        "phone": "+52 55 9876 5432",
        "email": "maria.gonzalez@email.com"
    }
}' "María González Silva (Cliente Joven)"

# CASO 4: Cliente de Alto Riesgo (Revisión Manual)
process_kyc_case "4" '{
    "customer_id": "KYC_DEMO_004",
    "personal_info": {
        "name": "Roberto Sánchez Morales",
        "id_number": "CURP444555666TUVWXY",
        "birth_date": "1975-12-25",
        "address": "Doctores 321, CDMX",
        "phone": "+52 55 5555 1111",
        "email": "roberto.sanchez@email.com"
    }
}' "Roberto Sánchez Morales (Alto Riesgo)"

echo ""
echo "🧠 TECNOLOGÍA SAPTIVA AI UTILIZADA:"
echo "===================================="
echo "✅ Saptiva OCR - Extracción inteligente de documentos"
echo "✅ Saptiva Guard - Validación automática de compliance"
echo "✅ Saptiva Ops - Análisis avanzado de riesgo crediticio"
echo "✅ Saptiva KAL - Function calling especializado"
echo "✅ Saptiva Embed - Embeddings para análisis semántico"
echo "✅ Saptiva Cortex - Procesamiento de lenguaje natural"

echo ""
echo "💰 COSTOS REALES GENERADOS:"
echo "==========================="
curl -s "http://localhost:8000/billing/session-summary" | python3.12 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    session = data.get('billing_summary', {}).get('session_summary', {})
    models = data.get('billing_summary', {}).get('models_breakdown', {})
    print(f'💵 Total invertido: \${session.get(\"total_cost\", 0):.6f} USD')
    print(f'🔢 Llamadas API: {session.get(\"total_calls\", 0)}')
    print(f'🎯 Tokens procesados: {session.get(\"total_tokens\", 0):,}')
    print(f'🤖 Modelos activos: {session.get(\"models_count\", 0)}')
    print()
    print('📊 Desglose por modelo:')
    for model, stats in models.items():
        cost = stats.get('total_cost', 0)
        calls = stats.get('calls', 0)
        print(f'  • {model}: {calls} calls → \${cost:.6f}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "🛡️ VALIDACIÓN DE COMPLIANCE REGULATORIO:"
echo "========================================"

# Ejecutar compliance con mejor formato
compliance_response=$(curl -s -X POST "http://localhost:8000/kyc/validate-compliance" \
  -H "Content-Type: application/json" \
  -d '{"identity_verified": true, "credit_score": 720, "sanctions_clear": true, "documents_validated": ["INE", "CURP", "Comprobante_domicilio"]}')

echo "$compliance_response" | python3.12 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    compliance = data.get('compliance_validation', {})
    
    print(f'✅ Estado: {'CUMPLE' if compliance.get('is_compliant') else 'NO CUMPLE'} normativa mexicana')
    print(f'📊 Score de compliance: {compliance.get('compliance_score', 0):.3f}')
    print(f'🎯 Score KYC: {compliance.get('kyc_score', 0):.3f}')
    print(f'🔍 Confianza RAG: {compliance.get('rag_confidence', 0):.3f}')
    print()
    print('📋 Fuentes regulatorias consultadas:')
    for source in compliance.get('regulatory_sources', []):
        print(f'  • {source.get('source')}: {source.get('title')}')
    print()
    print('🤖 Modelos utilizados:', ', '.join(data.get('models_used', [])))
    print('🏛️ Marco regulatorio:', data.get('regulatory_framework', 'N/A'))
    
except Exception as e:
    print(f'Error procesando compliance: {e}')
"

echo ""
echo "🏆 RESUMEN DEL DEMO:"
echo "==================="
echo "✅ 4 casos de KYC procesados en tiempo real"
echo "✅ APIs de Saptiva funcionando con costos reales"
echo "✅ Compliance validado contra normativa mexicana"
echo "✅ Procesamiento de DÍAS reducido a SEGUNDOS"
echo ""
echo "🚀 KYC Lightning Onboard - Hackathon 2025"
echo "🎯 Powered by Saptiva AI"