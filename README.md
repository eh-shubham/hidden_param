# Hidden Parameter Finder

A tool to discover hidden parameters in web applications.

## Features
- Tests common hidden parameters
- Custom wordlist support
- Detects differences in responses
- Output results to file

## Installation
```bash
git clone https://github.com/eh-shubham/hidden-param-finder.git
cd hidden-param-finder
pip install -r requirements.txt

## How to Use This Tool

Basic Usage:
python hidden_params.py https://example.com/page

With Custom Wordlist:
python hidden_params.py https://example.com/page -w my_wordlist.txt

Save Results to File:
python hidden_params.py https://example.com/page -o results.txt
