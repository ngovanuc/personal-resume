#!/usr/bin/env python3
"""
Load testing script for personal resume website
Tests concurrent users and response times
"""

import asyncio
import aiohttp
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import sys

class LoadTester:
    def __init__(self, base_url="http://localhost", max_workers=100):
        self.base_url = base_url
        self.max_workers = max_workers
        self.results = []
        
    async def make_request(self, session, endpoint="/"):
        """Make a single HTTP request and measure response time"""
        start_time = time.time()
        try:
            async with session.get(f"{self.base_url}{endpoint}") as response:
                await response.text()
                end_time = time.time()
                return {
                    'status': response.status,
                    'response_time': end_time - start_time,
                    'success': response.status == 200
                }
        except Exception as e:
            end_time = time.time()
            return {
                'status': 0,
                'response_time': end_time - start_time,
                'success': False,
                'error': str(e)
            }
    
    async def concurrent_test(self, num_requests, endpoint="/"):
        """Test with concurrent requests"""
        print(f"🚀 Starting load test: {num_requests} concurrent requests to {endpoint}")
        
        connector = aiohttp.TCPConnector(limit=200, limit_per_host=200)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(
            connector=connector, 
            timeout=timeout
        ) as session:
            tasks = [
                self.make_request(session, endpoint) 
                for _ in range(num_requests)
            ]
            
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = time.time()
            
            # Filter out exceptions
            valid_results = [r for r in results if isinstance(r, dict)]
            
            return {
                'total_time': end_time - start_time,
                'results': valid_results,
                'total_requests': num_requests,
                'successful_requests': len([r for r in valid_results if r['success']]),
                'failed_requests': len([r for r in valid_results if not r['success']])
            }
    
    def analyze_results(self, test_result):
        """Analyze test results and print summary"""
        results = test_result['results']
        response_times = [r['response_time'] for r in results if r['success']]
        
        if not response_times:
            print("❌ No successful requests!")
            return
            
        print("\n📊 LOAD TEST RESULTS")
        print("=" * 50)
        print(f"Total Requests: {test_result['total_requests']}")
        print(f"Successful: {test_result['successful_requests']}")
        print(f"Failed: {test_result['failed_requests']}")
        print(f"Success Rate: {(test_result['successful_requests']/test_result['total_requests']*100):.2f}%")
        print(f"Total Time: {test_result['total_time']:.2f}s")
        print(f"Requests/sec: {test_result['total_requests']/test_result['total_time']:.2f}")
        
        print(f"\n⏱️  RESPONSE TIMES")
        print(f"Average: {statistics.mean(response_times):.3f}s")
        print(f"Median: {statistics.median(response_times):.3f}s")
        print(f"Min: {min(response_times):.3f}s")
        print(f"Max: {max(response_times):.3f}s")
        
        if len(response_times) > 1:
            print(f"Std Dev: {statistics.stdev(response_times):.3f}s")
            
        # Percentiles
        sorted_times = sorted(response_times)
        p95 = sorted_times[int(len(sorted_times) * 0.95)]
        p99 = sorted_times[int(len(sorted_times) * 0.99)]
        print(f"95th percentile: {p95:.3f}s")
        print(f"99th percentile: {p99:.3f}s")

async def main():
    """Main testing function"""
    tester = LoadTester()
    
    print("🎯 Personal Resume Website Load Testing")
    print("=" * 50)
    
    # Test scenarios
    scenarios = [
        {"requests": 50, "endpoint": "/", "name": "Homepage - 50 users"},
        {"requests": 100, "endpoint": "/", "name": "Homepage - 100 users"},
        {"requests": 200, "endpoint": "/health", "name": "Health check - 200 users"},
        {"requests": 500, "endpoint": "/", "name": "Homepage - 500 users"},
        {"requests": 1000, "endpoint": "/", "name": "Homepage - 1000 users (stress test)"},
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🧪 Test {i}/{len(scenarios)}: {scenario['name']}")
        print("-" * 40)
        
        result = await tester.concurrent_test(
            scenario['requests'], 
            scenario['endpoint']
        )
        
        tester.analyze_results(result)
        
        # Wait between tests
        if i < len(scenarios):
            print("\n⏳ Waiting 3 seconds before next test...")
            await asyncio.sleep(3)
    
    print("\n✅ Load testing completed!")
    print("Check Grafana dashboard at http://localhost:3000 for detailed metrics")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Load test interrupted by user")
    except Exception as e:
        print(f"❌ Load test failed: {e}")
        sys.exit(1)