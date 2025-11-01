#!/usr/bin/env python3
"""
Servidor de Produção Flask - Gerador eBook v1.0.0
Optimizado para hospedagem online com HTTPS
"""

import os
import json
import hashlib
import requests
import threading
import time
from flask import Flask, send_from_directory, jsonify, request
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='app/leitor')

# Configurações globais
ACCESS_KIT_PATH = 'app/config/ACCESS_KIT.json'
ONLINE_MODE = False
ACCESS_TOKEN = None
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.ebook-system.demo')

def load_access_token():
    """Load access token from environment or file"""
    global ONLINE_MODE, ACCESS_TOKEN
    
    # Tentar carregar do ambiente primeiro
    ACCESS_TOKEN = os.getenv('API_ACCESS_TOKEN')
    
    # Se não tem no ambiente, tentar arquivo local
    if not ACCESS_TOKEN and os.path.exists(ACCESS_KIT_PATH):
        try:
            with open(ACCESS_KIT_PATH, 'r') as f:
                kit = json.load(f)
                ACCESS_TOKEN = kit.get('auth', {}).get('token')
                
                # Verificar expiração
                expires_at = kit.get('expires_at')
                if expires_at:
                    expires_ts = time.mktime(time.strptime(expires_at, "%Y-%m-%dT%H:%M:%SZ"))
                    ONLINE_MODE = time.time() < expires_ts
                    
                    if ONLINE_MODE:
                        logger.info(f"🔑 Modo ONLINE ativo (expira: {expires_at})")
                    else:
                        logger.info("🔒 Token expirado - modo OFFLINE")
                else:
                    ONLINE_MODE = False
        except Exception as e:
            logger.warning(f"⚠️  Erro ao carregar tokens: {e}")
            ONLINE_MODE = False
    else:
        ONLINE_MODE = False

# Carregar token na inicialização
load_access_token()

@app.route('/')
def homepage():
    """Serve the main homepage"""
    return send_from_directory('app/leitor', 'ebook_reader.html')

@app.route('/leitor')
def reader():
    """Serve the ebook reader page"""
    return send_from_directory('app/leitor', 'ebook_reader.html')

@app.route('/admin')
def admin_panel():
    """Serve the admin panel"""
    return send_from_directory('app/leitor', 'ebook_reader.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "ok": True,
        "version": "1.0.0",
        "environment": "production",
        "online_mode": ONLINE_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route('/api/smoke')
def smoke_test():
    """Smoke test endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "gerador-ebook",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route('/exports')
def exports_list():
    """List available export files"""
    try:
        exports_dir = 'app/exports'
        if not os.path.exists(exports_dir):
            return jsonify({"error": "Export directory not found"}), 404
        
        files = []
        for filename in os.listdir(exports_dir):
            if os.path.isfile(os.path.join(exports_dir, filename)):
                file_path = os.path.join(exports_dir, filename)
                file_size = os.path.getsize(file_path)
                files.append({
                    "name": filename,
                    "size": file_size,
                    "url": f"/exports/{filename}"
                })
        
        return jsonify({"files": files, "count": len(files)})
    except Exception as e:
        logger.error(f"Error listing exports: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/exports')
def exports_api():
    """API endpoint for exports"""
    return exports_list()

@app.route('/exports/<filename>')
def download_export(filename):
    """Download export files"""
    try:
        return send_from_directory('app/exports', filename)
    except Exception as e:
        logger.error(f"Error downloading {filename}: {e}")
        return jsonify({"error": "File not found"}), 404

@app.route('/api/mode')
def mode_status():
    """Get current mode status"""
    return jsonify({
        "online_mode": ONLINE_MODE,
        "access_token": bool(ACCESS_TOKEN),
        "api_base_url": API_BASE_URL
    })

@app.route('/api/upload-logo', methods=['POST'])
def upload_logo():
    """Handle logo upload (placeholder)"""
    # Placeholder for logo upload functionality
    return jsonify({
        "message": "Logo upload feature coming soon",
        "status": "not_implemented"
    })

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory('app/leitor', 'favicon.ico')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('app/leitor', filename)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 Iniciando servidor na porta {port}")
    logger.info(f"📱 Modo DEBUG: {debug}")
    logger.info(f"🌐 Modo ONLINE: {ONLINE_MODE}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)