#!/usr/bin/env python3
import requests
from urllib.parse import urlparse, urljoin, urlencode
from bs4 import BeautifulSoup
import argparse

# Common hidden parameters to test
COMMON_PARAMS = [
    'debug', 'test', 'hidden', 'admin', 'source', 'auth', 
    'token', 'session', 'id', 'user', 'key', 'redirect',
    'view', 'file', 'page', 'cmd', 'command', 'exec',
    'query', 'search', 'back', 'next', 'prev', 'lang'
]

def find_hidden_params(url, wordlist=None, output_file=None):
    if wordlist:
        try:
            with open(wordlist, 'r') as f:
                params = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Wordlist file {wordlist} not found. Using default parameters.")
            params = COMMON_PARAMS
    else:
        params = COMMON_PARAMS

    # Parse the URL
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    # Get original response
    try:
        original_response = requests.get(url, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return

    results = []
    
    print(f"\nTesting {len(params)} parameters against {url}\n")
    
    for param in params:
        test_url = f"{base_url}?{param}=test"
        try:
            response = requests.get(test_url, allow_redirects=False)
            
            # Check for differences
            if response.status_code != original_response.status_code:
                status = f"Different status code: {response.status_code}"
                results.append((param, status))
                print(f"[+] {param}: {status}")
            elif response.content != original_response.content:
                results.append((param, "Different content"))
                print(f"[+] {param}: Different content")
            elif len(response.content) != len(original_response.content):
                results.append((param, f"Different content length: {len(response.content)}"))
                print(f"[+] {param}: Different content length")
                
        except requests.exceptions.RequestException:
            continue

    if output_file:
        with open(output_file, 'w') as f:
            for param, result in results:
                f.write(f"{param}: {result}\n")
        print(f"\nResults saved to {output_file}")
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hidden Parameter Finder Tool")
    parser.add_argument("url", help="Target URL to test")
    parser.add_argument("-w", "--wordlist", help="Custom wordlist file for parameters")
    parser.add_argument("-o", "--output", help="Output file to save results")
    
    args = parser.parse_args()
    
    find_hidden_params(args.url, args.wordlist, args.output)