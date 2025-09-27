#!/usr/bin/env python3
"""
Quick performance test for scaled architecture
"""

import asyncio
import aiohttp
import time
from statistics import mean, median

async def test_endpoint(session, url, num_requests=100):
    """Test endpoint with concurrent requests"""
    start_time = time.time()
    
    async def make_request():
        try:
            async with session.get(url) as response:
                return response.status == 200
        except:
            return False
    
    tasks = [make_request() for _ in range(num_requests)]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    success_count = sum(results)
    
    return {
        'total_time': end_time - start_time,
        'total_requests': num_requests,
        'successful_requests': success_count,
        'success_rate': (success_count / num_requests) * 100,
        'requests_per_second': num_requests / (end_time - start_time)
    }

async def main():
    """Run quick performance tests"""
    base_url = "http://localhost"
    
    print("🚀 QUICK PERFORMANCE TEST")
    print("=" * 40)
    
    connector = aiohttp.TCPConnector(
        limit=1000,
        limit_per_host=1000,
        ttl_dns_cache=300,
        use_dns_cache=True,
    )
    
    async with aiohttp.ClientSession(
        connector=connector,
        timeout=aiohttp.ClientTimeout(total=30)
    ) as session:
        
        # Test scenarios
        tests = [
            {"endpoint": "/health", "requests": 100, "name": "Health Check"},
            {"endpoint": "/", "requests": 200, "name": "Homepage"},
            {"endpoint": "/health", "requests": 500, "name": "Health (Stress)"},
            {"endpoint": "/", "requests": 1000, "name": "Homepage (Heavy Load)"},
        ]
        
        for test in tests:
            print(f"\n📊 {test['name']} - {test['requests']} concurrent requests")
            print("-" * 35)
            
            result = await test_endpoint(
                session, 
                f"{base_url}{test['endpoint']}", 
                test['requests']
            )
            
            print(f"✅ Success Rate: {result['success_rate']:.1f}%")
            print(f"⚡ Requests/sec: {result['requests_per_second']:.1f}")
            print(f"⏱️  Total Time: {result['total_time']:.2f}s")
            print(f"📈 Successful: {result['successful_requests']}/{result['total_requests']}")
            
            # Small delay between tests
            await asyncio.sleep(1)
    
    print("\n✅ Performance test completed!")

if __name__ == "__main__":
    asyncio.run(main())