"""
Saptiva Billing & Usage Tracking Service
Monitorea costos, tokens y usage por modelo de Saptiva
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import asyncio

logger = logging.getLogger(__name__)

class SaptivaBillingService:
    """Servicio para tracking de costos y usage de Saptiva"""
    
    def __init__(self):
        self.api_key = os.getenv("SAPTIVA_API_KEY")
        
        # Precios por modelo según documentación oficial
        self.model_pricing = {
            "Saptiva Turbo": {
                "input_price_per_m": 0.2,
                "output_price_per_m": 0.6,
                "base_model": "Qwen 3:30B - No Think",
                "supports_tools": True
            },
            "Saptiva Cortex": {
                "input_price_per_m": 0.30,
                "output_price_per_m": 0.8,
                "base_model": "Qwen 3:30B - Think", 
                "supports_tools": True
            },
            "Saptiva Ops": {
                "input_price_per_m": 0.2,
                "output_price_per_m": 0.6,
                "base_model": "GPT OSS:20B",
                "supports_tools": False
            },
            "Saptiva Legacy": {
                "input_price_per_m": 0.2,
                "output_price_per_m": 0.6,
                "base_model": "LLama 3.3:70B",
                "supports_tools": True
            },
            "Saptiva OCR": {
                "input_price_per_m": 0.15,
                "output_price_per_m": 0.5,
                "base_model": "Nanonets OCR-s",
                "supports_tools": False
            },
            "Saptiva Embed": {
                "input_price_per_m": 0.01,
                "output_price_per_m": 0.0,  # Solo input para embeddings
                "base_model": "Qwen3 Embedding 8b",
                "supports_tools": False
            },
            "Saptiva Guard": {
                "input_price_per_m": 0.02,
                "output_price_per_m": 0.06,
                "base_model": "Llama Guard3 8b",
                "supports_tools": False
            },
            "Saptiva KAL": {
                "input_price_per_m": 0.2,
                "output_price_per_m": 0.6,
                "base_model": "Mistral Small 3.2 24B Instruct 2506",
                "supports_tools": True
            }
        }
        
        # Storage en memoria para el demo (en producción sería base de datos)
        self.usage_log = []
        self.daily_usage = {}
        self.session_costs = {
            "total_cost": 0.0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "models_used": {},
            "session_start": datetime.now().isoformat()
        }
    
    def log_api_call(self, model: str, input_tokens: int, output_tokens: int, 
                     operation: str = "chat", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Registra una llamada a la API y calcula costos
        """
        try:
            if model not in self.model_pricing:
                logger.warning(f"Modelo desconocido para billing: {model}")
                return {"error": f"Modelo {model} no encontrado en pricing"}
            
            pricing = self.model_pricing[model]
            
            # Calcular costos
            input_cost = (input_tokens / 1_000_000) * pricing["input_price_per_m"]
            output_cost = (output_tokens / 1_000_000) * pricing["output_price_per_m"]
            total_cost = input_cost + output_cost
            
            # Crear registro
            usage_record = {
                "timestamp": datetime.now().isoformat(),
                "model": model,
                "operation": operation,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "input_cost": round(input_cost, 6),
                "output_cost": round(output_cost, 6),
                "total_cost": round(total_cost, 6),
                "pricing_per_m": {
                    "input": pricing["input_price_per_m"],
                    "output": pricing["output_price_per_m"]
                },
                "metadata": metadata or {}
            }
            
            # Agregar a logs
            self.usage_log.append(usage_record)
            
            # Actualizar totales de sesión
            self.session_costs["total_cost"] += total_cost
            self.session_costs["total_input_tokens"] += input_tokens
            self.session_costs["total_output_tokens"] += output_tokens
            
            if model not in self.session_costs["models_used"]:
                self.session_costs["models_used"][model] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_cost": 0.0
                }
            
            model_stats = self.session_costs["models_used"][model]
            model_stats["calls"] += 1
            model_stats["input_tokens"] += input_tokens
            model_stats["output_tokens"] += output_tokens
            model_stats["total_cost"] += total_cost
            
            # Actualizar usage diario
            today = datetime.now().strftime("%Y-%m-%d")
            if today not in self.daily_usage:
                self.daily_usage[today] = {
                    "total_cost": 0.0,
                    "total_calls": 0,
                    "models": {}
                }
            
            self.daily_usage[today]["total_cost"] += total_cost
            self.daily_usage[today]["total_calls"] += 1
            
            if model not in self.daily_usage[today]["models"]:
                self.daily_usage[today]["models"][model] = {
                    "calls": 0,
                    "cost": 0.0,
                    "tokens": {"input": 0, "output": 0}
                }
            
            daily_model = self.daily_usage[today]["models"][model]
            daily_model["calls"] += 1
            daily_model["cost"] += total_cost
            daily_model["tokens"]["input"] += input_tokens
            daily_model["tokens"]["output"] += output_tokens
            
            logger.info(f"💰 Billing: {model} - ${total_cost:.6f} ({input_tokens}+{output_tokens} tokens)")
            
            return usage_record
            
        except Exception as e:
            logger.error(f"Error logging API call: {str(e)}")
            return {"error": str(e)}
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Obtiene resumen de costos de la sesión actual
        """
        try:
            session_duration = datetime.now() - datetime.fromisoformat(self.session_costs["session_start"])
            
            # Calcular estadísticas
            total_tokens = self.session_costs["total_input_tokens"] + self.session_costs["total_output_tokens"]
            avg_cost_per_call = (
                self.session_costs["total_cost"] / len(self.usage_log) 
                if self.usage_log else 0
            )
            
            # Modelo más usado
            most_used_model = None
            max_calls = 0
            for model, stats in self.session_costs["models_used"].items():
                if stats["calls"] > max_calls:
                    max_calls = stats["calls"]
                    most_used_model = model
            
            return {
                "session_summary": {
                    "duration": str(session_duration).split('.')[0],
                    "total_cost": round(self.session_costs["total_cost"], 6),
                    "total_calls": len(self.usage_log),
                    "total_tokens": total_tokens,
                    "input_tokens": self.session_costs["total_input_tokens"],
                    "output_tokens": self.session_costs["total_output_tokens"],
                    "avg_cost_per_call": round(avg_cost_per_call, 6),
                    "most_used_model": most_used_model,
                    "models_count": len(self.session_costs["models_used"])
                },
                "models_breakdown": self.session_costs["models_used"],
                "session_start": self.session_costs["session_start"],
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting session summary: {str(e)}")
            return {"error": str(e)}
    
    def get_daily_usage(self, date: str = None) -> Dict[str, Any]:
        """
        Obtiene usage diario
        """
        try:
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            
            if date not in self.daily_usage:
                return {
                    "date": date,
                    "usage": {
                        "total_cost": 0.0,
                        "total_calls": 0,
                        "models": {}
                    },
                    "message": "No usage data for this date"
                }
            
            usage_data = self.daily_usage[date]
            
            # Calcular estadísticas adicionales
            total_tokens = sum(
                model_data["tokens"]["input"] + model_data["tokens"]["output"]
                for model_data in usage_data["models"].values()
            )
            
            return {
                "date": date,
                "usage": usage_data,
                "statistics": {
                    "total_tokens": total_tokens,
                    "avg_cost_per_call": (
                        usage_data["total_cost"] / usage_data["total_calls"]
                        if usage_data["total_calls"] > 0 else 0
                    ),
                    "models_used": len(usage_data["models"])
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting daily usage: {str(e)}")
            return {"error": str(e)}
    
    def get_model_comparison(self) -> Dict[str, Any]:
        """
        Compara costos y eficiencia entre modelos
        """
        try:
            comparison = {}
            
            for model, stats in self.session_costs["models_used"].items():
                if stats["calls"] > 0:
                    total_tokens = stats["input_tokens"] + stats["output_tokens"]
                    avg_tokens_per_call = total_tokens / stats["calls"]
                    avg_cost_per_call = stats["total_cost"] / stats["calls"]
                    cost_per_token = stats["total_cost"] / total_tokens if total_tokens > 0 else 0
                    
                    comparison[model] = {
                        "calls": stats["calls"],
                        "total_cost": round(stats["total_cost"], 6),
                        "total_tokens": total_tokens,
                        "avg_tokens_per_call": round(avg_tokens_per_call, 2),
                        "avg_cost_per_call": round(avg_cost_per_call, 6),
                        "cost_per_token": round(cost_per_token, 8),
                        "pricing": self.model_pricing.get(model, {}),
                        "efficiency_score": round(
                            (avg_tokens_per_call / avg_cost_per_call) if avg_cost_per_call > 0 else 0,
                            2
                        )
                    }
            
            # Ordenar por eficiencia
            sorted_models = sorted(
                comparison.items(),
                key=lambda x: x[1]["efficiency_score"],
                reverse=True
            )
            
            return {
                "model_comparison": dict(sorted_models),
                "most_efficient": sorted_models[0][0] if sorted_models else None,
                "most_expensive": min(
                    comparison.items(),
                    key=lambda x: x[1]["cost_per_token"]
                )[0] if comparison else None,
                "total_models_compared": len(comparison)
            }
            
        except Exception as e:
            logger.error(f"Error getting model comparison: {str(e)}")
            return {"error": str(e)}
    
    def get_cost_projection(self, daily_calls: int = None) -> Dict[str, Any]:
        """
        Proyecta costos basado en usage actual
        """
        try:
            if not self.usage_log:
                return {"message": "No usage data available for projection"}
            
            # Calcular promedios actuales
            avg_cost_per_call = self.session_costs["total_cost"] / len(self.usage_log)
            
            if not daily_calls:
                # Estimar calls diarios basado en sesión actual
                session_duration = datetime.now() - datetime.fromisoformat(self.session_costs["session_start"])
                hours_elapsed = session_duration.total_seconds() / 3600
                calls_per_hour = len(self.usage_log) / hours_elapsed if hours_elapsed > 0 else 0
                daily_calls = int(calls_per_hour * 24)
            
            # Proyecciones
            daily_cost = daily_calls * avg_cost_per_call
            weekly_cost = daily_cost * 7
            monthly_cost = daily_cost * 30
            yearly_cost = daily_cost * 365
            
            return {
                "cost_projection": {
                    "assumptions": {
                        "daily_calls": daily_calls,
                        "avg_cost_per_call": round(avg_cost_per_call, 6)
                    },
                    "projections": {
                        "daily": round(daily_cost, 2),
                        "weekly": round(weekly_cost, 2),
                        "monthly": round(monthly_cost, 2),
                        "yearly": round(yearly_cost, 2)
                    },
                    "current_session": {
                        "calls": len(self.usage_log),
                        "cost": round(self.session_costs["total_cost"], 6),
                        "duration": str(datetime.now() - datetime.fromisoformat(self.session_costs["session_start"])).split('.')[0]
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting cost projection: {str(e)}")
            return {"error": str(e)}
    
    def get_pricing_info(self) -> Dict[str, Any]:
        """
        Obtiene información de precios de todos los modelos
        """
        return {
            "saptiva_pricing": self.model_pricing,
            "pricing_notes": {
                "currency": "USD",
                "unit": "per million tokens",
                "billing_precision": "6 decimal places",
                "last_updated": "2024-10-24"
            },
            "cost_optimization_tips": [
                "Usa Saptiva Embed ($0.01/M) para embeddings",
                "Saptiva Guard ($0.02/$0.06/M) es más barato para moderación",
                "Saptiva Turbo y Ops ($0.2/$0.6/M) son más económicos que Cortex",
                "Considera el balance entre costo y capacidades del modelo"
            ]
        }