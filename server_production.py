#!/usr/bin/env python3
"""
Servidor Flask limpo para GERADOR_EBOOK_FINAL_DEPLOY
Elimina problemas de offline, múltiplos servidores e complexidades
"""

import os
import sys
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    """Servir a página principal"""
    # Tenta encontrar o arquivo HTML em diferentes localizações
    html_file = find_ebook_html()
    
    if html_file:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return html_content
        except Exception as e:
            return f"""
            <html>
            <head><title>Erro</title></head>
            <body>
                <h1>Erro ao ler arquivo HTML</h1>
                <p>Arquivo encontrado: {html_file}</p>
                <p>Erro: {e}</p>
                <p><a href="/debug">Ver debug</a></p>
            </body>
            </html>
            """
    else:
        return """
        <html>
        <head><title>Ebook não encontrado</title></head>
        <body>
            <h1>Ebook não encontrado</h1>
            <p>Não foi possível localizar o arquivo ebook_reader.html</p>
            <p>Verifique se o arquivo existe em:</p>
            <ul>
                <li>ebook_reader.html</li>
                <li>app/ebook_reader.html</li>
                <li>./ebook_reader.html</li>
            </ul>
            <p><a href="/debug">Ver debug</a></p>
        </body>
        </html>
        """

@app.route('/debug')
def debug():
    """Debug informações"""
    return jsonify({
        "current_dir": os.getcwd(),
        "python_version": "Flask production",
        "method": "direct file reading",
        "html_found": bool(find_ebook_html()),
        "debug_info": "Versão limpa - sem dependências complexas"
    })

@app.route('/api/health')
def health():
    """Health check para Render"""
    return jsonify({
        "status": "healthy",
        "app": "GERADOR_EBOOK_FINAL_DEPLOY",
        "method": "clean production version"
    })

def find_ebook_html():
    """Encontra o arquivo HTML em diferentes localizações"""
    possible_paths = [
        "ebook_reader.html",
        "app/ebook_reader.html",
        os.path.join(os.getcwd(), "ebook_reader.html"),
        os.path.join(os.getcwd(), "app", "ebook_reader.html"),
        os.path.join(".", "ebook_reader.html"),
        os.path.join("app", "ebook_reader.html")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

if __name__ == '__main__':
    # Porta para Render
    port = int(os.environ.get('PORT', 10000))
    
    print("=== GERADOR_EBOOK_FINAL_DEPLOY - SERVIDOR LIMPO ===")
    print(f"Diretório: {os.getcwd()}")
    print(f"Porta: {port}")
    print(f"Arquivo HTML encontrado: {find_ebook_html()}")
    print("============================================")
    
    # Usar apenas o Flask
    app.run(host='0.0.0.0', port=port)