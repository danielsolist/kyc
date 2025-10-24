#!/bin/bash

# 🧠 Demo Saptiva RAG - Retrieval-Augmented Generation
# Demuestra Saptiva Embed + Saptiva Cortex + RAGster

clear
echo "🧠 SAPTIVA RAG DEMO - RETRIEVAL-AUGMENTED GENERATION"
echo "===================================================="
echo "🤖 Powered by Saptiva Embed + Saptiva Cortex + RAGster"
echo ""
echo "🔑 API Key: va-ai-7ZSCkAlaygy39P-H9lxQeRN3vyN81fuc07BZRQhJOe4w9XcBt3f-7QBt6fAIcJWYSXlIWEJCtOYZq1Qkxpg6G7JmA8UeKzoSlciYNe6tLh4"
echo "🌐 Embed API: https://api.saptiva.com/api/embed"
echo "🌐 Chat API: https://api.saptiva.com/v1/chat/completions"
echo ""

sleep 2

echo "📚 INFORMACIÓN DEL SISTEMA RAG"
echo "=============================="
curl -s http://localhost:8000/kyc/rag-info | jq '.'
echo ""

sleep 3

echo "🧠 DEMO 1: CONSULTA SOBRE NORMATIVA CNBV"
echo "========================================"
echo "❓ Pregunta: ¿Qué documentos requiere la CNBV para KYC?"
echo ""

curl -s -X POST "http://localhost:8000/kyc/rag-query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Qué documentos requiere la CNBV para el proceso KYC de clientes bancarios?"
  }' | jq '.'

echo ""
sleep 3

echo "🧠 DEMO 2: CONSULTA SOBRE PROTECCIÓN DE DATOS"
echo "============================================="
echo "❓ Pregunta: ¿Cómo debe manejarse la información personal según CONDUSEF?"
echo ""

curl -s -X POST "http://localhost:8000/kyc/rag-query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cómo debe manejarse la información personal de clientes según CONDUSEF en procesos KYC?"
  }' | jq '.'

echo ""
sleep 3

echo "🧠 DEMO 3: CONSULTA SOBRE PREVENCIÓN DE LAVADO"
echo "=============================================="
echo "❓ Pregunta: ¿Qué establece BANXICO sobre prevención de lavado de dinero?"
echo ""

curl -s -X POST "http://localhost:8000/kyc/rag-query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Qué controles establece BANXICO para prevenir el lavado de dinero en instituciones financieras?"
  }' | jq '.'

echo ""
sleep 3

echo "🛡️ DEMO 4: VALIDACIÓN DE COMPLIANCE CON RAG"
echo "==========================================="
echo "📋 Validando proceso KYC contra normativa mexicana..."
echo ""

curl -s -X POST "http://localhost:8000/kyc/validate-compliance" \
  -H "Content-Type: application/json" \
  -d '{
    "identity_verified": true,
    "credit_score": 720,
    "sanctions_clear": true,
    "documents_validated": ["CURP", "RFC", "Comprobante_Ingresos"],
    "customer_risk_level": "low"
  }' | jq '.'

echo ""
sleep 2

echo "🎯 CAPACIDADES RAG DEMOSTRADAS:"
echo "==============================="
echo "✅ Saptiva Embed - Vectorización semántica de normativas"
echo "✅ Búsqueda semántica - Encuentra documentos relevantes"
echo "✅ Saptiva Cortex - Generación contextualizada"
echo "✅ RAGster - Base de conocimiento vectorial"
echo "✅ Trazabilidad - Fuentes regulatorias identificadas"
echo "✅ Compliance automático - Validación normativa en tiempo real"
echo ""

echo "📊 MODELOS SAPTIVA UTILIZADOS:"
echo "=============================="
echo "🔍 Saptiva Embed (Qwen3 Embedding 8b)"
echo "   • Vectorización semántica: \$0.01 por M tokens"
echo "   • Mejor para: Memoria contextual, búsqueda, RAG"
echo ""
echo "🧠 Saptiva Cortex (Qwen 3:30B - Think)"
echo "   • Tareas de razonamiento: \$0.30/\$0.8 por M tokens"
echo "   • Mejor para: Agentes con lógica, comprensión profunda"
echo ""

echo "🏛️ BASE DE CONOCIMIENTO:"
echo "========================"
echo "📋 CNBV - Disposiciones KYC"
echo "📋 CONDUSEF - Protección de datos"
echo "📋 BANXICO - Prevención lavado de dinero"
echo "📋 UIF - Operaciones sospechosas"
echo "📋 SHCP - Régimen fiscal"
echo ""

echo "⚡ VENTAJAS DEL RAG:"
echo "==================="
echo "🎯 Respuestas basadas en normativa actualizada"
echo "🔍 Búsqueda semántica (no solo palabras clave)"
echo "📚 Memoria externa inteligente"
echo "🛡️ Compliance automático y trazable"
echo "⚡ Procesamiento en tiempo real"
echo "📊 Fuentes regulatorias verificables"
echo ""

echo "💰 PRICING RAG:"
echo "==============="
echo "🔍 Saptiva Embed: \$0.01 por M tokens"
echo "🧠 Saptiva Cortex: \$0.30/\$0.8 por M tokens"
echo "📚 RAGster: Incluido en la plataforma"
echo "🛡️ Compliance checking: Automatizado"
echo ""

echo "🏆 RESULTADO FINAL:"
echo "=================="
echo "• Consultas normativas respondidas en tiempo real"
echo "• Fuentes regulatorias trazables y verificables"
echo "• Compliance automático con normativa mexicana"
echo "• Búsqueda semántica inteligente"
echo "• Generación contextualizada precisa"
echo ""

echo "🔗 DOCUMENTACIÓN TÉCNICA:"
echo "========================="
echo "📖 RAG: https://saptiva.gitbook.io/saptiva-docs/basicos/rag"
echo "🔍 Embed: https://api.saptiva.com/api/embed"
echo "🧠 Cortex: https://api.saptiva.com/v1/chat/completions"
echo ""

echo "✨ ¡DEMO RAG COMPLETADO!"
echo "Saptiva RAG = Memoria externa inteligente para compliance"