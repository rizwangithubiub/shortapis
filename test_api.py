#!/usr/bin/env python3
"""
Test script for URL Shortening Service API
Run this script to test all API endpoints
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_create_short_url():
    """Test creating a short URL"""
    print("=== Testing Create Short URL ===")
    
    url = f"{BASE_URL}/shorten"
    data = {"url": "https://www.google.com"}
    
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        return response.json()['shortCode']
    return None

def test_get_original_url(short_code):
    """Test retrieving original URL"""
    print(f"\n=== Testing Get Original URL ({short_code}) ===")
    
    url = f"{BASE_URL}/shorten/{short_code}"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_update_short_url(short_code):
    """Test updating a short URL"""
    print(f"\n=== Testing Update Short URL ({short_code}) ===")
    
    url = f"{BASE_URL}/shorten/{short_code}"
    data = {"url": "https://www.github.com"}
    
    response = requests.put(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_statistics(short_code):
    """Test getting URL statistics"""
    print(f"\n=== Testing Get Statistics ({short_code}) ===")
    
    url = f"{BASE_URL}/shorten/{short_code}/stats"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_redirect(short_code):
    """Test URL redirection"""
    print(f"\n=== Testing URL Redirection ({short_code}) ===")
    
    url = f"{BASE_URL}/{short_code}"
    response = requests.get(url, allow_redirects=False)
    print(f"Status Code: {response.status_code}")
    print(f"Location Header: {response.headers.get('Location', 'Not Found')}")

def test_delete_short_url(short_code):
    """Test deleting a short URL"""
    print(f"\n=== Testing Delete Short URL ({short_code}) ===")
    
    url = f"{BASE_URL}/shorten/{short_code}"
    response = requests.delete(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

def test_error_cases():
    """Test various error cases"""
    print("\n=== Testing Error Cases ===")
    
    # Test invalid URL
    print("\n--- Testing Invalid URL ---")
    url = f"{BASE_URL}/shorten"
    data = {"url": "not-a-valid-url"}
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test missing URL field
    print("\n--- Testing Missing URL Field ---")
    data = {"invalid": "field"}
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test non-existent short code
    print("\n--- Testing Non-existent Short Code ---")
    url = f"{BASE_URL}/shorten/nonexistent"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def main():
    """Run all tests"""
    print("Starting API Tests...")
    print("Make sure the Flask app is running on localhost:5000")
    print("=" * 50)
    
    try:
        # Test creating a short URL
        short_code = test_create_short_url()
        
        if short_code:
            # Test getting original URL
            test_get_original_url(short_code)
            
            # Test redirection (this will increment access count)
            test_redirect(short_code)
            
            # Test getting statistics
            test_get_statistics(short_code)
            
            # Test updating URL
            test_update_short_url(short_code)
            
            # Test getting statistics again to see updated info
            test_get_statistics(short_code)
            
            # Test deleting URL
            test_delete_short_url(short_code)
            
            # Try to get the deleted URL (should return 404)
            test_get_original_url(short_code)
        
        # Test error cases
        test_error_cases()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the Flask app is running on localhost:5000")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    
    print("\n" + "=" * 50)
    print("API Tests Completed!")

if __name__ == "__main__":
    main()