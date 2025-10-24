#!/bin/bash

# 💰 Demo Saptiva Billing - Cost & Usage Tracking
# Demuestra tracking de costos y tokens por modelo

clear
echo "💰 SAPTIVA BILLING DEMO - COST & USAGE TRACKING"
echo "==============================================="
echo "📊 Monitoreo de costos y tokens por modelo Saptiva"
echo ""
echo "🔑 API Key: va-ai-7ZSCkAlaygy39P-H9lxQeRN3vyN81fuc07BZRQhJOe4w9XcBt3f-7QBt6fAIcJWYSXlIWEJCtOYZq1Qkxpg6G7JmA8UeKzoSlciYNe6tLh4"
echo ""

sleep 2

echo "💲 INFORMACIÓN DE PRECIOS SAPTIVA"
echo "================================="
curl -s http://localhost:8000/billing/pricing-info | jq '.pricing_info.saptiva_pricing | to_entries | .[] | {model: .key, input_price: .value.input_price_per_m, output_price: .value.output_price_per_m, base_model: .value.base_model}'
echo ""

sleep 3

echo "📝 SIMULANDO USAGE DE DIFERENTES MODELOS"
echo "========================================"

echo "🔧 1. Logging usage Saptiva Turbo (100 input + 50 output tokens)..."
curl -s -X POST "http://localhost:8000/billing/log-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Saptiva Turbo",
    "input_tokens": 100,
    "output_tokens": 50,
    "operation": "kyc_processing"
  }' | jq '.logged_usage | {model, input_tokens, output_tokens, total_cost}'

echo ""

echo "🧠 2. Logging usage Saptiva Cortex (200 input + 150 output tokens)..."
curl -s -X POST "http://localhost:8000/billing/log-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Saptiva Cortex",
    "input_tokens": 200,
    "output_tokens": 150,
    "operation": "rag_query"
  }' | jq '.logged_usage | {model, input_tokens, output_tokens, total_cost}'

echo ""

echo "🔍 3. Logging usage Saptiva Embed (500 input tokens)..."
curl -s -X POST "http://localhost:8000/billing/log-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Saptiva Embed",
    "input_tokens": 500,
    "output_tokens": 0,
    "operation": "embedding_generation"
  }' | jq '.logged_usage | {model, input_tokens, output_tokens, total_cost}'

echo ""

echo "🛡️ 4. Logging usage Saptiva Guard (75 input + 25 output tokens)..."
curl -s -X POST "http://localhost:8000/billing/log-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Saptiva Guard",
    "input_tokens": 75,
    "output_tokens": 25,
    "operation": "content_moderation"
  }' | jq '.logged_usage | {model, input_tokens, output_tokens, total_cost}'

echo ""

echo "🇲🇽 5. Logging usage Saptiva KAL (300 input + 200 output tokens)..."
curl -s -X POST "http://localhost:8000/billing/log-usage" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Saptiva KAL",
    "input_tokens": 300,
    "output_tokens": 200,
    "operation": "function_calling"
  }' | jq '.logged_usage | {model, input_tokens, output_tokens, total_cost}'

echo ""
sleep 3

echo "📊 RESUMEN DE SESIÓN ACTUAL"
echo "=========================="
curl -s http://localhost:8000/billing/session-summary | jq '.billing_summary.session_summary'
echo ""

sleep 2

echo "🔍 COMPARACIÓN ENTRE MODELOS"
echo "============================"
curl -s http://localhost:8000/billing/model-comparison | jq '.model_comparison.model_comparison | to_entries | .[] | {model: .key, calls: .value.calls, total_cost: .value.total_cost, cost_per_token: .value.cost_per_token, efficiency_score: .value.efficiency_score}'
echo ""

sleep 2

echo "📈 PROYECCIÓN DE COSTOS"
echo "======================"
curl -s "http://localhost:8000/billing/cost-projection?daily_calls=1000" | jq '.cost_projection.cost_projection'
echo ""

sleep 2

echo "📅 USAGE DIARIO"
echo "==============="
curl -s http://localhost:8000/billing/daily-usage | jq '.daily_usage'
echo ""

echo "💡 ANÁLISIS DE COSTOS POR MODELO:"
echo "================================="
echo "🔍 Saptiva Embed: \$0.01/M tokens (MÁS BARATO para embeddings)"
echo "🛡️ Saptiva Guard: \$0.02/\$0.06/M tokens (BARATO para moderación)"
echo "⚡ Saptiva Turbo: \$0.2/\$0.6/M tokens (EQUILIBRADO precio/rendimiento)"
echo "🧠 Saptiva Cortex: \$0.30/\$0.8/M tokens (PREMIUM para razonamiento)"
echo "🇲🇽 Saptiva KAL: \$0.2/\$0.6/M tokens (ESPECIALIZADO México + Tools)"
echo ""

echo "🎯 RECOMENDACIONES DE OPTIMIZACIÓN:"
echo "==================================="
echo "💰 Para embeddings: Usar Saptiva Embed (\$0.01/M)"
echo "🛡️ Para moderación: Usar Saptiva Guard (\$0.02/\$0.06/M)"
echo "⚡ Para uso general: Saptiva Turbo o Ops (\$0.2/\$0.6/M)"
echo "🧠 Para razonamiento complejo: Saptiva Cortex (\$0.30/\$0.8/M)"
echo "🔧 Para Function Calling: Saptiva KAL o Legacy"
echo ""

echo "📊 MÉTRICAS CLAVE MONITOREADAS:"
echo "==============================="
echo "✅ Tokens de entrada y salida por modelo"
echo "✅ Costo por llamada y por token"
echo "✅ Eficiencia (tokens por dólar)"
echo "✅ Usage diario y proyecciones"
echo "✅ Comparación entre modelos"
echo "✅ Tracking de sesión en tiempo real"
echo ""

echo "🔗 ENDPOINTS DE BILLING DISPONIBLES:"
echo "===================================="
echo "📊 GET /billing/session-summary - Resumen de sesión"
echo "📅 GET /billing/daily-usage - Usage diario"
echo "🔍 GET /billing/model-comparison - Comparación modelos"
echo "📈 GET /billing/cost-projection - Proyección costos"
echo "💲 GET /billing/pricing-info - Info de precios"
echo "📝 POST /billing/log-usage - Registrar usage manual"
echo ""

echo "✨ ¡DEMO BILLING COMPLETADO!"
echo "Tracking completo de costos y usage por modelo Saptiva"