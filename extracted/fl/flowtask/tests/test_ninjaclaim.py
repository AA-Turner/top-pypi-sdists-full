import asyncio
import os
from flowtask.components.NetworkNinjaClaims import NetworkNinjaClaims

async def test():
    print("🚀 Iniciando test de NetworkNinjaClaims...")
    print("=" * 60)
    
    claims = NetworkNinjaClaims(
        nn_username=os.getenv('SHAREPOINT_TROCADV_USERNAME'),
        nn_password=os.getenv('SHAREPOINT_TROCADV_PASSWORD'),
        use_persistent_session=True,
        headless=False  # Modo visible para ver el proceso
    )
    
    try:
        # Test 1: Login y extracción de cookies
        print("\n📝 Test 1: Login y extracción de cookies...")
        print("-" * 60)
        cookies = await claims.login_and_extract_cookies()
        print(f"\n✅ Cookies extraídas: {len(cookies)}")
        for name, value in cookies.items():
            display_value = value[:30] + "..." if len(value) > 30 else value
            print(f"   🍪 {name}: {display_value}")
        
        # Test 2: Extracción de claims
        print("\n📊 Test 2: Extracción de claims...")
        print("-" * 60)
        result = await claims.claims()
        print(f"\n✅ Claims extraídos: {len(result)}")
        print("\nPrimeros registros:")
        print(result.head())
        
        # Guardar resultados
        output_file = 'networkninja_claims_test.csv'
        result.to_csv(output_file, index=False)
        print(f"\n💾 Resultados guardados en: {output_file}")
        
        print("\n" + "=" * 60)
        print("✨ Test completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(test())