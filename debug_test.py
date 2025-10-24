#!/usr/bin/env python3
"""
Script de debug para KYC
"""

import asyncio
import sys
import traceback
import os
from dotenv import load_dotenv
from services.kyc_orchestrator import KYCOrchestrator

# Cargar variables de entorno
load_dotenv()

async def test_kyc():
    try:
        orchestrator = KYCOrchestrator()
        
        personal_info = {
            "name": "Juan Pérez",
            "id_number": "CURP123456789",
            "birth_date": "1990-01-01",
            "address": "Calle Principal 123",
            "phone": "+52 55 1234 5678",
            "email": "juan@email.com"
        }
        
        result = await orchestrator.process_kyc_application(
            customer_id="DEBUG001",
            documents=[],
            personal_info=personal_info
        )
        
        print("✅ KYC procesado exitosamente!")
        print(f"Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_kyc())