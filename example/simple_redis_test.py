#!/usr/bin/env python3
"""
Teste simples do Redis usando apenas a biblioteca redis padrão
"""

import asyncio
import json
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_redis_simple():
    """Teste simples do Redis"""
    try:
        # Importa usando apenas redis padrão
        import redis.asyncio as redis
        
        print("🔄 Conectando ao Redis...")
        
        # Conecta ao Redis
        client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        
        # Testa a conexão
        response = await client.ping()
        print(f"✅ Redis respondeu: {response}")
        
        # Teste básico SET/GET
        print("\n📝 Testando SET/GET...")
        await client.set("test_key", "Hello Redis!")
        value = await client.get("test_key")
        print(f"   Valor armazenado: {value}")
        
        # Teste com JSON
        print("\n📦 Testando com dados JSON...")
        data = {"name": "Pedro", "project": "FastAPI + Redis", "timestamp": "2025-07-24"}
        await client.set("json_test", json.dumps(data))
        json_value = await client.get("json_test")
        parsed_data = json.loads(json_value)
        print(f"   Dados JSON: {parsed_data}")
        
        # Teste contador
        print("\n🔢 Testando contador...")
        for _ in range(3):
            count = await client.incr("counter")
            print(f"   Contador: {count}")
        
        # Teste com expiração
        print("\n⏰ Testando expiração (5 segundos)...")
        await client.setex("temp_key", 5, "Valor temporário")
        ttl = await client.ttl("temp_key")
        print(f"   TTL: {ttl} segundos")
        
        # Lista todas as chaves
        print("\n📋 Listando todas as chaves...")
        keys = await client.keys("*")
        print(f"   Chaves: {keys}")
        
        # Limpa os dados de teste
        print("\n🧹 Limpando dados de teste...")
        await client.delete("test_key", "json_test", "counter")
        
        # Fecha a conexão
        await client.aclose()
        print("\n✅ Teste concluído com sucesso!")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Instale o Redis: pip install redis")
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando teste simples do Redis")
    print("=" * 50)
    asyncio.run(test_redis_simple())
