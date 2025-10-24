import asyncio
import logging
from typing import Dict, Any, List
from .saptiva_service import SaptivaService
from .validation_service import ValidationService
from .database_service import DatabaseService

logger = logging.getLogger(__name__)

class KYCOrchestrator:
    """Orquestador principal del flujo KYC"""
    
    def __init__(self):
        self.saptiva_service = SaptivaService()
        self.validation_service = ValidationService()
        self.db_service = DatabaseService()
    
    async def process_kyc_application(self, 
                                    customer_id: str,
                                    documents: List[Dict[str, Any]],
                                    personal_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una aplicación KYC completa
        """
        try:
            logger.info(f"Iniciando proceso KYC para cliente: {customer_id}")
            logger.info(f"Documentos recibidos: {len(documents)}")
            
            # Paso 1: Extraer datos de documentos
            document_results = []
            for doc in documents:
                logger.info(f"Procesando documento: {doc.get('type', 'unknown')}")
                result = await self.saptiva_service.extract_document_data(
                    doc["content"], 
                    doc["type"]
                )
                document_results.append(result)
            
            logger.info(f"Documentos procesados: {len(document_results)}")
            
            # Paso 2: Validar información personal
            logger.info("Iniciando validación de información personal")
            validation_result = await self.validation_service.validate_personal_info(
                personal_info, 
                document_results
            )
            logger.info("Validación de información personal completada")
            
            # Paso 3: Verificación de identidad y listas de sanciones
            # Si no hay documentos, usar la información personal directamente
            logger.info("Preparando datos para verificación de identidad")
            if document_results:
                logger.info("Usando datos de documentos extraídos")
                identity_data = document_results[0]["extracted_fields"]
                id_number = document_results[0]["extracted_fields"]["id_number"]
            else:
                logger.info("Usando información personal directamente")
                identity_data = personal_info
                id_number = personal_info.get("id_number", "")
            
            logger.info(f"Verificando identidad para ID: {id_number}")
            identity_result = await self.saptiva_service.validate_identity(identity_data)
            logger.info("Verificación de identidad completada")
            
            # Paso 4: Consulta buró de crédito
            credit_result = await self.saptiva_service.check_credit_bureau(id_number)
            
            # Paso 5: Evaluación de riesgo final
            risk_assessment = await self.saptiva_service.calculate_risk_assessment(
                identity_result,
                credit_result
            )
            
            # Paso 6: Guardar resultados en base de datos
            kyc_record = {
                "customer_id": customer_id,
                "status": "completed",
                "documents": document_results,
                "identity_verification": identity_result,
                "credit_check": credit_result,
                "risk_assessment": risk_assessment,
                "approved": risk_assessment["approved"],
                "processing_time": (
                    sum(doc.get("processing_time", 0) for doc in document_results) +
                    identity_result.get("validation_time", 0) +
                    credit_result.get("bureau_response_time", 0)
                )
            }
            
            await self.db_service.save_kyc_record(kyc_record)
            
            # Respuesta final
            response = {
                "status": "completed",
                "customer_id": customer_id,
                "verification_score": risk_assessment["final_score"],
                "risk_level": risk_assessment["risk_level"],
                "approved": risk_assessment["approved"],
                "processing_time": kyc_record["processing_time"],
                "details": {
                    "documents_processed": len(document_results),
                    "identity_verified": identity_result["identity_verified"],
                    "credit_score": credit_result["credit_score"],
                    "sanctions_clear": identity_result["sanctions_check"] == "clear"
                }
            }
            
            logger.info(f"KYC completado para {customer_id}: {response['status']}")
            return response
            
        except Exception as e:
            import traceback
            logger.error(f"Error procesando KYC para {customer_id}: {str(e)}")
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            
            # Guardar error en base de datos
            error_record = {
                "customer_id": customer_id,
                "status": "error",
                "error_message": str(e),
                "approved": False
            }
            await self.db_service.save_kyc_record(error_record)
            
            raise
    
    async def get_kyc_status(self, customer_id: str) -> Dict[str, Any]:
        """
        Obtiene el estado actual de un proceso KYC
        """
        try:
            record = await self.db_service.get_kyc_record(customer_id)
            if not record:
                return {"status": "not_found", "customer_id": customer_id}
            
            return {
                "status": record["status"],
                "customer_id": customer_id,
                "approved": record.get("approved", False),
                "risk_level": record.get("risk_assessment", {}).get("risk_level", "unknown"),
                "last_updated": record.get("created_at")
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estado KYC para {customer_id}: {str(e)}")
            raise