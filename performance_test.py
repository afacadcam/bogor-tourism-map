# performance_test.py
import time
import requests
import statistics

def test_endpoint_performance(url, num_requests=100):
    """Test endpoint performance"""
    response_times = []
    
    print(f"Testing {url} with {num_requests} requests...")
    
    for i in range(num_requests):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            if response.status_code == 200:
                response_times.append(end_time - start_time)
            else:
                print(f"Request {i+1} failed with status {response.status_code}")
                
        except requests.RequestException as e:
            print(f"Request {i+1} failed: {e}")
    
    if response_times:
        avg_time = statistics.mean(response_times)
        median_time = statistics.median(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print(f"Results for {url}:")
        print(f"  Average response time: {avg_time:.3f}s")
        print(f"  Median response time: {median_time:.3f}s") 
        print(f"  Min response time: {min_time:.3f}s")
        print(f"  Max response time: {max_time:.3f}s")
        print(f"  Success rate: {len(response_times)}/{num_requests}")
        print()

if __name__ == "__main__":
    base_url = "https://tourism.id"
    
    endpoints = [
        f"{base_url}/",
        f"{base_url}/api/places/",
        f"{base_url}/analytics/dashboard/",
        f"{base_url}/analytics/api/category-distribution/",
    ]
    
    for endpoint in endpoints:
        test_endpoint_performance(endpoint, 50)
