import re
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ValidationService:
    """Servicio de validación de datos"""
    
    def __init__(self):
        self.setup_validation_rules()
    
    def setup_validation_rules(self):
        """Configura las reglas de validación"""
        self.validation_rules = {
            "curp": r"^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9A-Z][0-9]$",
            "rfc": r"^[A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3}$",
            "phone": r"^\+?52?[0-9]{10}$",
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        }
    
    async def validate_personal_info(self, 
                                   personal_info: Dict[str, Any],
                                   document_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Valida información personal contra datos extraídos de documentos
        """
        try:
            validation_results = {
                "valid": True,
                "errors": [],
                "warnings": [],
                "field_matches": {}
            }
            
            # Validar formato de campos
            for field, pattern in self.validation_rules.items():
                if field in personal_info:
                    value = personal_info[field]
                    if not re.match(pattern, str(value)):
                        validation_results["errors"].append(f"Formato inválido para {field}: {value}")
                        validation_results["valid"] = False
            
            # Comparar con datos extraídos de documentos
            if document_data and len(document_data) > 0:
                extracted_fields = document_data[0].get("extracted_fields", {})
                
                # Validar coincidencia de nombres
                if "name" in personal_info and "name" in extracted_fields:
                    similarity = self._calculate_name_similarity(
                        personal_info["name"], 
                        extracted_fields["name"]
                    )
                    validation_results["field_matches"]["name"] = similarity
                    
                    if similarity < 0.8:
                        validation_results["warnings"].append(
                            f"Baja similitud en nombres: {similarity:.2f}"
                        )
                
                # Validar coincidencia de ID
                if "id_number" in personal_info and "id_number" in extracted_fields:
                    id_match = personal_info["id_number"] == extracted_fields["id_number"]
                    validation_results["field_matches"]["id_number"] = id_match
                    
                    if not id_match:
                        validation_results["errors"].append("Número de identificación no coincide")
                        validation_results["valid"] = False
            
            # Validaciones adicionales de negocio
            age_validation = self._validate_age(personal_info.get("birth_date"))
            if not age_validation["valid"]:
                validation_results["errors"] += age_validation["errors"]
                validation_results["valid"] = False
            
            logger.info(f"Validación completada: {len(validation_results['errors'])} errores")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error en validación: {str(e)}")
            raise
    
    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        """Calcula similitud entre nombres usando algoritmo simple"""
        try:
            # Normalizar nombres
            name1_clean = re.sub(r'[^a-zA-Z\s]', '', name1.upper().strip())
            name2_clean = re.sub(r'[^a-zA-Z\s]', '', name2.upper().strip())
            
            # Algoritmo simple de similitud
            words1 = set(name1_clean.split())
            words2 = set(name2_clean.split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union) if union else 0.0
            
        except Exception:
            return 0.0
    
    def _validate_age(self, birth_date: str) -> Dict[str, Any]:
        """Valida edad mínima para servicios bancarios"""
        try:
            from datetime import datetime, date
            
            if not birth_date:
                return {"valid": False, "errors": ["Fecha de nacimiento requerida"]}
            
            # Parsear fecha
            try:
                birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
            except ValueError:
                return {"valid": False, "errors": ["Formato de fecha inválido (YYYY-MM-DD)"]}
            
            # Calcular edad
            today = date.today()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            
            # Validar edad mínima (18 años)
            if age < 18:
                return {"valid": False, "errors": ["Edad mínima requerida: 18 años"]}
            
            # Validar edad máxima razonable (120 años)
            if age > 120:
                return {"valid": False, "errors": ["Edad no válida"]}
            
            return {"valid": True, "errors": [], "age": age}
            
        except Exception as e:
            return {"valid": False, "errors": [f"Error validando edad: {str(e)}"]}
    
    async def validate_document_quality(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida calidad de documentos extraídos"""
        try:
            quality_check = {
                "valid": True,
                "confidence_threshold": 0.8,
                "issues": []
            }
            
            confidence = document_data.get("confidence_score", 0)
            
            if confidence < quality_check["confidence_threshold"]:
                quality_check["valid"] = False
                quality_check["issues"].append(
                    f"Confianza baja en OCR: {confidence:.2f}"
                )
            
            # Verificar campos requeridos
            required_fields = ["name", "id_number", "birth_date"]
            extracted_fields = document_data.get("extracted_fields", {})
            
            for field in required_fields:
                if field not in extracted_fields or not extracted_fields[field]:
                    quality_check["valid"] = False
                    quality_check["issues"].append(f"Campo requerido faltante: {field}")
            
            return quality_check
            
        except Exception as e:
            logger.error(f"Error validando calidad de documento: {str(e)}")
            raise