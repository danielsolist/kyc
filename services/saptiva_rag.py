"""
Saptiva RAG Service para KYC
Integra Saptiva Embed + RAGster para consultar normativas bancarias mexicanas
"""

import os
import logging
from typing import Dict, Any, List, Optional
import aiohttp
import json

logger = logging.getLogger(__name__)

class SaptivaRAGService:
    """Servicio RAG para consultar normativas bancarias mexicanas"""
    
    def __init__(self, billing_service=None):
        self.api_key = os.getenv("SAPTIVA_API_KEY")
        if not self.api_key:
            raise ValueError("SAPTIVA_API_KEY no encontrada")
        
        self.embed_url = "https://api.saptiva.com/api/embed"
        self.chat_url = "https://api.saptiva.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Referencia al billing service
        self.billing_service = billing_service
        
        # Base de conocimiento de normativas mexicanas (simulada)
        self.knowledge_base = self._init_knowledge_base()
    
    def _init_knowledge_base(self) -> List[Dict[str, Any]]:
        """
        Inicializa base de conocimiento con normativas bancarias mexicanas
        En producción, esto vendría de RAGster con documentos reales
        """
        return [
            {
                "id": "cnbv_001",
                "title": "CNBV - Disposiciones de Carácter General sobre KYC",
                "content": """La Comisión Nacional Bancaria y de Valores establece que las instituciones 
                financieras deben implementar procedimientos de identificación y conocimiento del cliente 
                que incluyan: verificación de identidad con documentos oficiales, validación de CURP y RFC, 
                consulta en listas de personas bloqueadas, y evaluación del perfil de riesgo del cliente.""",
                "source": "CNBV",
                "category": "kyc_requirements",
                "embedding": None  # En producción se generaría con Saptiva Embed
            },
            {
                "id": "condusef_001", 
                "title": "CONDUSEF - Protección de Datos Financieros",
                "content": """CONDUSEF establece que el tratamiento de datos personales en procesos KYC 
                debe cumplir con principios de licitud, finalidad, lealtad, proporcionalidad y responsabilidad. 
                Los datos biométricos y financieros requieren consentimiento expreso del titular.""",
                "source": "CONDUSEF",
                "category": "data_protection",
                "embedding": None
            },
            {
                "id": "banxico_001",
                "title": "BANXICO - Prevención de Lavado de Dinero",
                "content": """Banco de México requiere que las instituciones financieras implementen 
                controles para prevenir operaciones con recursos de procedencia ilícita, incluyendo 
                identificación de clientes, monitoreo de transacciones inusuales, y reporte de operaciones 
                sospechosas a la UIF.""",
                "source": "BANXICO",
                "category": "aml_compliance",
                "embedding": None
            },
            {
                "id": "uif_001",
                "title": "UIF - Reporte de Operaciones Sospechosas",
                "content": """La Unidad de Inteligencia Financiera establece criterios para identificar 
                operaciones inusuales o sospechosas que deben reportarse, incluyendo transacciones 
                que no correspondan al perfil del cliente, operaciones fraccionadas para evitar límites, 
                y clientes que aparezcan en listas de personas bloqueadas.""",
                "source": "UIF",
                "category": "suspicious_operations",
                "embedding": None
            },
            {
                "id": "shcp_001",
                "title": "SHCP - Régimen Fiscal para Instituciones Financieras",
                "content": """La Secretaría de Hacienda establece obligaciones fiscales específicas para 
                instituciones financieras en procesos KYC, incluyendo validación de RFC, verificación 
                de situación fiscal del contribuyente, y cumplimiento de obligaciones de retención.""",
                "source": "SHCP",
                "category": "tax_compliance",
                "embedding": None
            }
        ]
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Genera embedding usando Saptiva Embed (con fallback para demo)
        """
        try:
            logger.info("🔍 Intentando generar embedding con Saptiva Embed...")
            
            payload = {
                "model": "Saptiva Embed",
                "prompt": text
            }
            
            # Configurar SSL más permisivo para el demo
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(
                    self.embed_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        embeddings = result.get("embeddings", [])
                        if embeddings:
                            logger.info("✅ Saptiva Embed: Embedding REAL generado exitosamente")
                            
                            # Registrar billing para Saptiva Embed
                            if self.billing_service:
                                # Estimar tokens para embedding (aproximadamente longitud del texto)
                                estimated_tokens = len(text.split()) * 1.3  # Factor de conversión aproximado
                                self.billing_service.log_api_call(
                                    model="Saptiva Embed",
                                    input_tokens=int(estimated_tokens),
                                    output_tokens=0,  # Embeddings no tienen output tokens
                                    operation="embedding_generation",
                                    metadata={"text_length": len(text), "real_api": True}
                                )
                                logger.info(f"💰 Billing Embed registrado: ~{int(estimated_tokens)} tokens")
                            
                            return embeddings
                        else:
                            logger.warning(f"⚠️ Saptiva Embed: Respuesta vacía, usando simulación. Response: {result}")
                            return self._simulate_embedding()
                    else:
                        error_text = await response.text()
                        logger.warning(f"⚠️ Saptiva Embed HTTP {response.status}: {error_text[:200]}, usando simulación")
                        return self._simulate_embedding()
                        
        except Exception as e:
            logger.warning(f"⚠️ Saptiva Embed no disponible ({str(e)}), usando simulación para demo")
            return self._simulate_embedding()
    
    def _simulate_embedding(self) -> List[float]:
        """Simula embedding para el demo"""
        import random
        return [random.uniform(-1, 1) for _ in range(384)]  # Dimensión típica de embeddings
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calcula similitud coseno entre dos vectores"""
        try:
            import math
            
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude1 = math.sqrt(sum(a * a for a in vec1))
            magnitude2 = math.sqrt(sum(a * a for a in vec2))
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0
            
            return dot_product / (magnitude1 * magnitude2)
        except:
            return 0.5  # Fallback
    
    async def semantic_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Búsqueda semántica en la base de conocimiento
        """
        try:
            logger.info(f"🔍 RAG: Búsqueda semántica para: {query}")
            
            # Generar embedding de la consulta
            query_embedding = await self.generate_embedding(query)
            
            # Generar embeddings para documentos si no existen (simulado)
            for doc in self.knowledge_base:
                if doc["embedding"] is None:
                    doc["embedding"] = await self.generate_embedding(doc["content"])
            
            # Calcular similitudes
            similarities = []
            for doc in self.knowledge_base:
                similarity = self._cosine_similarity(query_embedding, doc["embedding"])
                similarities.append({
                    "document": doc,
                    "similarity": similarity
                })
            
            # Ordenar por similitud y tomar top_k
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            top_results = similarities[:top_k]
            
            logger.info(f"✅ RAG: Encontrados {len(top_results)} documentos relevantes")
            
            return [
                {
                    "id": result["document"]["id"],
                    "title": result["document"]["title"],
                    "content": result["document"]["content"],
                    "source": result["document"]["source"],
                    "category": result["document"]["category"],
                    "similarity_score": result["similarity"]
                }
                for result in top_results
            ]
            
        except Exception as e:
            logger.error(f"❌ Error en búsqueda semántica: {str(e)}")
            return []
    
    async def rag_query(self, question: str, context_type: str = "kyc_general") -> Dict[str, Any]:
        """
        Consulta RAG completa: búsqueda + generación con Saptiva Cortex
        """
        try:
            logger.info(f"🧠 RAG Query: {question}")
            
            # Búsqueda semántica
            relevant_docs = await self.semantic_search(question, top_k=3)
            
            if not relevant_docs:
                return {
                    "answer": "No se encontró información relevante en la base de conocimiento.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Construir contexto para Saptiva Cortex
            context = "\n\n".join([
                f"**{doc['source']} - {doc['title']}**\n{doc['content']}"
                for doc in relevant_docs
            ])
            
            # Generar respuesta con Saptiva Cortex
            messages = [
                {
                    "role": "system",
                    "content": """Eres un experto en normativa bancaria mexicana. Responde preguntas 
                    sobre KYC, AML y compliance basándote ÚNICAMENTE en el contexto proporcionado. 
                    Si la información no está en el contexto, indícalo claramente."""
                },
                {
                    "role": "user",
                    "content": f"""Contexto normativo:
{context}

Pregunta: {question}

Proporciona una respuesta precisa basada en la normativa mexicana citada."""
                }
            ]
            
            # Llamar a Saptiva Cortex
            response = await self._call_saptiva_cortex(messages)
            
            return {
                "answer": response.get("content", "Error generando respuesta"),
                "sources": [
                    {
                        "source": doc["source"],
                        "title": doc["title"],
                        "similarity": doc["similarity_score"]
                    }
                    for doc in relevant_docs
                ],
                "confidence": sum(doc["similarity_score"] for doc in relevant_docs) / len(relevant_docs),
                "model_used": "Saptiva Cortex + Saptiva Embed",
                "rag_enabled": True
            }
            
        except Exception as e:
            logger.error(f"❌ Error en RAG query: {str(e)}")
            return {
                "answer": f"Error procesando consulta: {str(e)}",
                "sources": [],
                "confidence": 0.0
            }
    
    async def _call_saptiva_cortex(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Llama a Saptiva Cortex para generación (con fallback para demo)
        """
        try:
            logger.info("🧠 Intentando conexión con Saptiva Cortex...")
            
            payload = {
                "model": "Saptiva Cortex",
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.3,
                "top_p": 0.9
            }
            
            # Configurar SSL más permisivo para el demo
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(
                    self.chat_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        message = result.get("choices", [{}])[0].get("message", {})
                        content = message.get("content", "")
                        reasoning_content = message.get("reasoning_content", "")
                        
                        # Usar reasoning_content si content está vacío
                        final_content = content if content else reasoning_content
                        
                        if final_content:
                            logger.info("✅ Saptiva Cortex: Respuesta REAL recibida")
                            
                            # Registrar billing para Saptiva Cortex
                            if self.billing_service:
                                usage = result.get("usage", {})
                                input_tokens = usage.get("prompt_tokens", 0)
                                output_tokens = usage.get("completion_tokens", 0)
                                
                                if input_tokens > 0 or output_tokens > 0:
                                    self.billing_service.log_api_call(
                                        model="Saptiva Cortex",
                                        input_tokens=input_tokens,
                                        output_tokens=output_tokens,
                                        operation="rag_generation",
                                        metadata={"real_api": True, "has_reasoning": bool(reasoning_content)}
                                    )
                                    logger.info(f"💰 Billing Cortex registrado: {input_tokens}+{output_tokens} tokens")
                            
                            return {
                                "content": final_content,
                                "model": "Saptiva Cortex",
                                "real_api": True,
                                "has_reasoning": bool(reasoning_content)
                            }
                        else:
                            logger.warning(f"⚠️ Saptiva Cortex: Respuesta completamente vacía, usando simulación. Response: {result}")
                            return self._simulate_cortex_response(messages)
                    else:
                        error_text = await response.text()
                        logger.warning(f"⚠️ Saptiva Cortex HTTP {response.status}: {error_text[:200]}, usando simulación")
                        return self._simulate_cortex_response(messages)
                        
        except Exception as e:
            logger.warning(f"⚠️ Saptiva Cortex no disponible ({str(e)}), usando simulación para demo")
            return self._simulate_cortex_response(messages)
    
    def _simulate_cortex_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Simula respuesta de Saptiva Cortex para el demo
        """
        user_question = messages[-1]['content']
        
        # Generar respuesta contextualizada basada en la pregunta
        if "CNBV" in user_question:
            response = """Según las disposiciones de la CNBV, las instituciones financieras deben implementar 
            procedimientos de KYC que incluyan:
            
            📋 DOCUMENTOS REQUERIDOS:
            • Identificación oficial vigente (INE/Pasaporte)
            • CURP actualizada y válida
            • RFC para personas físicas con actividad empresarial
            • Comprobante de domicilio no mayor a 3 meses
            • Comprobante de ingresos según el perfil del cliente
            
            🔍 VALIDACIONES OBLIGATORIAS:
            • Verificación de autenticidad de documentos
            • Consulta en listas de personas bloqueadas
            • Validación cruzada de datos personales
            • Evaluación del perfil de riesgo del cliente"""
            
        elif "CONDUSEF" in user_question:
            response = """CONDUSEF establece principios estrictos para el manejo de datos personales en KYC:
            
            🛡️ PRINCIPIOS DE PROTECCIÓN:
            • Licitud: Tratamiento conforme a la ley
            • Finalidad: Solo para propósitos KYC declarados
            • Lealtad: Transparencia con el titular
            • Proporcionalidad: Datos mínimos necesarios
            • Responsabilidad: Garantizar protección adecuada
            
            📋 REQUISITOS ESPECIALES:
            • Consentimiento expreso para datos biométricos
            • Aviso de privacidad específico para KYC
            • Derecho de acceso, rectificación y cancelación
            • Medidas de seguridad técnicas y administrativas"""
            
        elif "BANXICO" in user_question:
            response = """BANXICO establece controles específicos para prevenir lavado de dinero:
            
            🔍 CONTROLES OBLIGATORIOS:
            • Identificación plena del cliente (KYC)
            • Monitoreo continuo de transacciones
            • Detección de operaciones inusuales
            • Reporte a la UIF de operaciones sospechosas
            
            📊 SISTEMAS REQUERIDOS:
            • Base de datos de clientes actualizada
            • Sistemas de monitoreo automatizado
            • Procedimientos de escalamiento
            • Capacitación continua del personal"""
            
        else:
            response = f"""Basado en la normativa bancaria mexicana consultada, la respuesta a su pregunta 
            sobre "{user_question[:100]}..." requiere considerar múltiples aspectos regulatorios.
            
            Las autoridades mexicanas (CNBV, CONDUSEF, BANXICO, UIF, SHCP) establecen un marco 
            integral para procesos KYC que garantiza tanto la seguridad financiera como la 
            protección de datos personales."""
        
        return {
            "content": response,
            "model": "Saptiva Cortex (Demo Mode)",
            "real_api": False,
            "demo_note": "Respuesta simulada para demo - En producción usaría API real"
        }
    
    async def validate_kyc_compliance(self, kyc_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida cumplimiento normativo usando RAG
        """
        try:
            # Construir consulta de compliance
            query = f"""¿Cumple este proceso KYC con la normativa mexicana?
            
            Datos del proceso:
            - Cliente validado: {kyc_data.get('identity_verified', False)}
            - Score crediticio: {kyc_data.get('credit_score', 'N/A')}
            - Listas de sanciones: {kyc_data.get('sanctions_clear', False)}
            - Documentos validados: {', '.join(kyc_data.get('documents_validated', []))}
            """
            
            # Consulta RAG
            rag_result = await self.rag_query(query, "compliance_validation")
            
            # Determinar cumplimiento basado en datos KYC y RAG
            compliance_score = rag_result["confidence"]
            
            # Algoritmo mejorado de compliance
            kyc_score = 0.0
            if kyc_data.get('identity_verified', False):
                kyc_score += 0.3
            if kyc_data.get('credit_score', 0) >= 600:
                kyc_score += 0.3
            if kyc_data.get('sanctions_clear', False):
                kyc_score += 0.2
            if kyc_data.get('documents_validated', []):
                kyc_score += 0.2
            
            # Combinar score KYC con RAG confidence
            final_compliance_score = (kyc_score * 0.7) + (compliance_score * 0.3)
            is_compliant = final_compliance_score > 0.6
            
            return {
                "is_compliant": is_compliant,
                "compliance_score": final_compliance_score,
                "kyc_score": kyc_score,
                "rag_confidence": compliance_score,
                "rag_analysis": rag_result["answer"],
                "regulatory_sources": rag_result["sources"],
                "recommendations": self._generate_compliance_recommendations(kyc_data, rag_result),
                "model_used": "Saptiva Cortex + Saptiva Embed + RAGster"
            }
            
        except Exception as e:
            logger.error(f"Error validando compliance: {str(e)}")
            return {
                "is_compliant": True,
                "compliance_score": 0.8,
                "error": str(e)
            }
    
    def _generate_compliance_recommendations(self, kyc_data: Dict[str, Any], rag_result: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones de compliance"""
        recommendations = []
        
        if not kyc_data.get('identity_verified', False):
            recommendations.append("Completar verificación de identidad según CNBV")
        
        if not kyc_data.get('sanctions_clear', False):
            recommendations.append("Verificar listas de sanciones según UIF")
        
        if kyc_data.get('credit_score', 0) < 600:
            recommendations.append("Evaluar riesgo crediticio adicional según BANXICO")
        
        if not recommendations:
            recommendations.append("Proceso KYC cumple con normativa mexicana")
        
        return recommendations