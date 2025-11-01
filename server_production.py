#!/usr/bin/env python3
"""
SERVIDOR SIMPLES PARA RENDER.COM - GERADOR EBOOK
Versão super simples que funciona 100% no Render
"""

import os
import json
import sys
from flask import Flask, send_file, jsonify, send_from_directory

# DEBUG AMPLO
print("=== DEBUG INICIAL ===")
print(f"OS PATH: {os.path}")
print(f"CWD: {os.getcwd()}")
print(f"FILES: {os.listdir('.')}")
if os.path.exists('app'):
    print(f"APP exists: {os.listdir('app')}")
    if os.path.exists('app/leitor'):
        print(f"LEITOR exists: {os.listdir('app/leitor')}")
print("=== FIM DEBUG ===")

app = Flask(__name__)

@app.route('/')
def home():
    """Servir a página principal"""
    try:
        # Múltiplas tentativas de encontrar o arquivo
        possible_files = [
            'app/leitor/ebook_reader.html',
            'app/leitor/index.html',
            'leitor/ebook_reader.html',
            'index.html'
        ]
        
        for filename in possible_files:
            if os.path.exists(filename):
                print(f"✅ SERVIDO: {filename}")
                return send_file(filename, mimetype='text/html')
        
        # Se não encontrou nenhum
        return f"""
        <h2>ERRO: Arquivo HTML não encontrado</h2>
        <p>Caminhos testados:</p>
        <ul>
        {''.join(f'<li>{path}</li>' for path in possible_files)}
        </ul>
        <p>CWD: {os.getcwd()}</p>
        <p>Files here: {os.listdir('.')}</p>
        <a href="/debug">Ver debug completo</a>
        """
        
    except Exception as e:
        return f"<h1>ERRO: {str(e)}</h1>"

@app.route('/debug')
def debug():
    """Debug completo do sistema"""
    debug_info = {
        "current_dir": os.getcwd(),
        "files_here": os.listdir('.'),
        "app_exists": os.path.exists('app'),
        "leitor_exists": os.path.exists('leitor'),
        "app_leitor_exists": os.path.exists('app/leitor'),
        "files_in_app": os.listdir('app') if os.path.exists('app') else "Pasta app não existe",
        "files_in_app_leitor": os.listdir('app/leitor') if os.path.exists('app/leitor') else "Pasta app/leitor não existe"
    }
    
    # Verificar todos os arquivos possíveis
    possible_files = [
        'app/leitor/ebook_reader.html',
        'app/leitor/index.html',
        'leitor/ebook_reader.html',
        'index.html'
    ]
    
    debug_info["possible_files"] = {}
    for filename in possible_files:
        debug_info["possible_files"][filename] = os.path.exists(filename)
    
    return jsonify(debug_info, indent=2)

@app.route('/api/health')
def health():
    """Health check melhorado"""
    html_found = False
    html_path = None
    
    possible_files = [
        'app/leitor/ebook_reader.html',
        'app/leitor/index.html',
        'leitor/ebook_reader.html',
        'index.html'
    ]
    
    for filename in possible_files:
        if os.path.exists(filename):
            html_found = True
            html_path = filename
            break
    
    return jsonify({
        "status": "healthy" if html_found else "missing_html",
        "html_found": html_found,
        "html_path": html_path,
        "cwd": os.getcwd(),
        "has_app": os.path.exists('app'),
        "has_leitor": os.path.exists('app/leitor'),
        "server_type": "simple_render"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Iniciando servidor na porta {port}")
    print(f"Servindo arquivos de: {os.getcwd()}")
    app.run(host='0.0.0.0', port=port, debug=True)