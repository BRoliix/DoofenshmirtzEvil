#!/bin/bash
# Railway startup script

# Create required directories
mkdir -p saved_documents
mkdir -p mock

# Start the application
streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false