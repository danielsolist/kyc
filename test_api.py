#!/usr/bin/env python3
"""
Script de prueba para KYC Lightning Onboard API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_root():
    """Test root endpoint"""
    print("🔍 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_kyc_simple():
    """Test simple KYC processing"""
    print("🔍 Testing simple KYC processing...")
    
    payload = {
        "customer_id": "TEST001",
        "personal_info": {
            "name": "Juan Pérez García",
            "id_number": "CURP123456789",
            "birth_date": "1990-01-01",
            "address": "Calle Principal 123, Ciudad de México",
            "phone": "+52 55 1234 5678",
            "email": "juan.perez@email.com"
        }
    }
    
    response = requests.post(f"{BASE_URL}/kyc/process-simple", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ KYC Processed Successfully!")
        print(f"Customer ID: {result['customer_id']}")
        print(f"Status: {result['status']}")
        print(f"Approved: {result['approved']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Score: {result['verification_score']:.2f}")
        print(f"Processing Time: {result['processing_time']:.2f}s")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_kyc_status():
    """Test KYC status endpoint"""
    print("🔍 Testing KYC status...")
    
    customer_id = "TEST001"
    response = requests.get(f"{BASE_URL}/kyc/status/{customer_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Status Retrieved!")
        print(f"Customer ID: {result['customer_id']}")
        print(f"Status: {result['status']}")
        print(f"Approved: {result['approved']}")
        print(f"Risk Level: {result['risk_level']}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_statistics():
    """Test statistics endpoint"""
    print("🔍 Testing statistics...")
    
    response = requests.get(f"{BASE_URL}/kyc/stats")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Statistics Retrieved!")
        print(f"Total Applications: {stats['total_applications']}")
        print(f"Approved: {stats['approved']}")
        print(f"Rejected: {stats['rejected']}")
        print(f"Errors: {stats['errors']}")
        print(f"Approval Rate: {stats['approval_rate']:.1f}%")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_search():
    """Test search endpoint"""
    print("🔍 Testing search...")
    
    response = requests.get(f"{BASE_URL}/kyc/search?approved=true")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Search Completed!")
        print(f"Results Found: {result['count']}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def run_load_test():
    """Run a simple load test"""
    print("🚀 Running load test (10 requests)...")
    
    payload = {
        "customer_id": f"LOAD_TEST_{int(time.time())}",
        "personal_info": {
            "name": "Test User",
            "id_number": "TEST123456789",
            "birth_date": "1985-06-15",
            "address": "Test Address 456",
            "phone": "+52 55 9876 5432",
            "email": "test@example.com"
        }
    }
    
    start_time = time.time()
    success_count = 0
    
    for i in range(10):
        payload["customer_id"] = f"LOAD_TEST_{i}_{int(time.time())}"
        
        try:
            response = requests.post(f"{BASE_URL}/kyc/process-simple", json=payload, timeout=30)
            if response.status_code == 200:
                success_count += 1
            print(f"Request {i+1}: {response.status_code}")
        except Exception as e:
            print(f"Request {i+1}: Error - {str(e)}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n📊 Load Test Results:")
    print(f"Total Requests: 10")
    print(f"Successful: {success_count}")
    print(f"Failed: {10 - success_count}")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Average Time per Request: {total_time/10:.2f}s")
    print(f"Requests per Second: {10/total_time:.2f}")
    print()

def main():
    """Run all tests"""
    print("🚀 KYC Lightning Onboard API Test Suite")
    print("=" * 50)
    
    try:
        test_health()
        test_root()
        test_kyc_simple()
        test_kyc_status()
        test_statistics()
        test_search()
        test_saptiva_tools()
        test_tools_info()
        test_rag_query()
        test_compliance_validation()
        test_rag_info()
        run_load_test()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()

def test_saptiva_tools():
    """Test Saptiva Tools endpoint"""
    print("🔧 Testing Saptiva Tools (Function Calling)...")
    
    payload = {
        "customer_id": "TOOLS_TEST_001",
        "personal_info": {
            "name": "Ana Martínez Rodríguez",
            "id_number": "CURP555666777ABC",
            "birth_date": "1992-07-20",
            "address": "Av. Polanco 456, CDMX",
            "phone": "+52 55 5555 6666",
            "email": "ana.martinez@email.com"
        }
    }
    
    response = requests.post(f"{BASE_URL}/kyc/process-with-tools", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Saptiva Tools Executed Successfully!")
        print(f"Customer ID: {result['customer_id']}")
        print(f"Status: {result['status']}")
        print(f"Tools Used: {len(result['details']['tools_used'])}")
        print(f"Models: {', '.join(result['details']['models_used'])}")
        print(f"Function Calling: {result['details']['function_calling']}")
        print(f"Decision: {result['details']['decision_final']}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_tools_info():
    """Test tools information endpoint"""
    print("📋 Testing Saptiva Tools Info...")
    
    response = requests.get(f"{BASE_URL}/kyc/tools-info")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        info = response.json()
        print(f"✅ Tools Info Retrieved!")
        print(f"Total Tools: {info['saptiva_tools_info']['total_tools']}")
        print(f"Compatible Model: {info['saptiva_tools_info']['model_compatible']}")
        print(f"Function Calling: {info['saptiva_tools_info']['function_calling']}")
        print(f"Compliance: {', '.join(info['compliance'])}")
    else:
        print(f"❌ Error: {response.text}")
    print()def test_
rag_query():
    """Test RAG query endpoint"""
    print("🧠 Testing Saptiva RAG Query...")
    
    payload = {
        "question": "¿Qué documentos requiere la CNBV para KYC?"
    }
    
    response = requests.post(f"{BASE_URL}/kyc/rag-query", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ RAG Query Successful!")
        print(f"Question: {result['question']}")
        print(f"Models Used: {', '.join(result['models_used'])}")
        print(f"Sources Consulted: {result['sources_consulted']}")
        print(f"Confidence: {result['confidence']:.3f}")
        print(f"Technology: {result['technology']}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_compliance_validation():
    """Test compliance validation with RAG"""
    print("🛡️ Testing RAG Compliance Validation...")
    
    payload = {
        "identity_verified": True,
        "credit_score": 720,
        "sanctions_clear": True,
        "documents_validated": ["CURP", "RFC", "Comprobante_Ingresos"],
        "customer_risk_level": "low"
    }
    
    response = requests.post(f"{BASE_URL}/kyc/validate-compliance", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Compliance Validation Successful!")
        print(f"Is Compliant: {result['compliance_validation']['is_compliant']}")
        print(f"Compliance Score: {result['compliance_validation']['compliance_score']:.3f}")
        print(f"Models Used: {', '.join(result['models_used'])}")
        print(f"Regulatory Framework: {result['regulatory_framework']}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_rag_info():
    """Test RAG system information"""
    print("📚 Testing RAG System Info...")
    
    response = requests.get(f"{BASE_URL}/kyc/rag-info")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        info = response.json()
        print(f"✅ RAG Info Retrieved!")
        print(f"Embedding Model: {info['rag_system']['embedding_model']}")
        print(f"Generation Model: {info['rag_system']['generation_model']}")
        print(f"Documents Indexed: {info['rag_system']['documents_indexed']}")
        print(f"Regulatory Sources: {len(info['rag_system']['regulatory_sources'])}")
    else:
        print(f"❌ Error: {response.text}")
    print()def t
est_billing_pricing():
    """Test billing pricing info"""
    print("💲 Testing Saptiva Pricing Info...")
    
    response = requests.get(f"{BASE_URL}/billing/pricing-info")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        info = response.json()
        pricing = info['pricing_info']['saptiva_pricing']
        print(f"✅ Pricing Info Retrieved!")
        print(f"Models Available: {len(pricing)}")
        print(f"Cheapest Model: Saptiva Embed ($0.01/M)")
        print(f"Most Expensive: Saptiva Cortex ($0.30/$0.8/M)")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_billing_log_usage():
    """Test manual usage logging"""
    print("📝 Testing Manual Usage Logging...")
    
    payload = {
        "model": "Saptiva Turbo",
        "input_tokens": 150,
        "output_tokens": 75,
        "operation": "test_kyc"
    }
    
    response = requests.post(f"{BASE_URL}/billing/log-usage", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        usage = result['logged_usage']
        print(f"✅ Usage Logged Successfully!")
        print(f"Model: {usage['model']}")
        print(f"Total Cost: ${usage['total_cost']}")
        print(f"Input Tokens: {usage['input_tokens']}")
        print(f"Output Tokens: {usage['output_tokens']}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_billing_session_summary():
    """Test session billing summary"""
    print("📊 Testing Session Billing Summary...")
    
    response = requests.get(f"{BASE_URL}/billing/session-summary")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        summary = result['billing_summary']['session_summary']
        print(f"✅ Session Summary Retrieved!")
        print(f"Total Cost: ${summary['total_cost']}")
        print(f"Total Calls: {summary['total_calls']}")
        print(f"Total Tokens: {summary['total_tokens']}")
        print(f"Models Used: {summary['models_count']}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_billing_model_comparison():
    """Test model cost comparison"""
    print("🔍 Testing Model Cost Comparison...")
    
    response = requests.get(f"{BASE_URL}/billing/model-comparison")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        comparison = result['model_comparison']['model_comparison']
        print(f"✅ Model Comparison Retrieved!")
        print(f"Models Compared: {len(comparison)}")
        if result['model_compar