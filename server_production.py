#!/usr/bin/env python3
"""
SERVIDOR CORRETIVO PARA GERADOR EBOOK
Corrige problemas na rota / e debug
"""

import os
import json
import sys
import traceback
from flask import Flask, send_file, jsonify, send_from_directory

# DEBUG AMPLO
print("=== DEBUG INICIAL ===")
print(f"OS PATH: {os.path}")
print(f"CWD: {os.getcwd()}")
print(f"Files: {os.listdir('.')}")
print("=== FIM DEBUG ===")

app = Flask(__name__)

@app.route('/')
def home():
    """Servir a página principal com debug completo"""
    try:
        print(f"=== ROTA / CHAMADA ===")
        print(f"CWD: {os.getcwd()}")
        print(f"Files here: {os.listdir('.')}")
        
        # Verificar se app existe
        if os.path.exists('app'):
            print(f"App dir: {os.listdir('app')}")
            if os.path.exists('app/leitor'):
                print(f"Leitor dir: {os.listdir('app/leitor')}")
        
        # Buscar arquivo
        html_file = 'app/leitor/ebook_reader.html'
        
        if os.path.exists(html_file):
            print(f"✅ ARQUIVO ENCONTRADO: {html_file}")
            print(f"Absolute path: {os.path.abspath(html_file)}")
            return send_file(html_file, mimetype='text/html')
        else:
            print(f"❌ ARQUIVO NÃO ENCONTRADO: {html_file}")
            return f"""
            <h2>Arquivo não encontrado</h2>
            <p>Procurado: {html_file}</p>
            <p>CWD: {os.getcwd()}</p>
            <p>Files: {os.listdir('.')}</p>
            <a href="/debug">Debug completo</a>
            """
            
    except Exception as e:
        print(f"❌ ERRO NA ROTA /: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return f"""
        <h1>Erro na rota /</h1>
        <p>Erro: {str(e)}</p>
        <p><a href="/debug">Ver debug</a></p>
        """

@app.route('/debug')
def debug():
    """Debug completo do sistema"""
    try:
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
        
    except Exception as e:
        print(f"❌ ERRO NO DEBUG: {str(e)}")
        return f"""
        <h1>Erro no debug</h1>
        <p>Erro: {str(e)}</p>
        <pre>{traceback.format_exc()}</pre>
        """

@app.route('/api/health')
def health():
    """Health check melhorado"""
    try:
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
            "server_type": "simple_render",
            "absolute_path": os.path.abspath(html_path) if html_path else None
        })
        
    except Exception as e:
        print(f"❌ ERRO NO HEALTH: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Iniciando servidor na porta {port}")
    print(f"Servindo arquivos de: {os.getcwd()}")
    app.run(host='0.0.0.0', port=port, debug=True)