#!/usr/bin/env python3
"""
Servidor Flask CORRIGIDO FINAL - GERADOR_EBOOK_FINAL_DEPLOY
Resolve problema 404 para arquivos CSS/JS
"""

import os
from flask import Flask, jsonify, send_file

app = Flask(__name__)

# ===== ROTA PARA ARQUIVOS ESTÁTICOS =====
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve arquivos CSS, JS e outros estáticos"""
    if os.path.exists(filename):
        if filename.endswith('.css'):
            return send_file(filename, mimetype='text/css')
        elif filename.endswith('.js'):
            return send_file(filename, mimetype='application/javascript')
        elif filename.endswith(('.html', '.htm')):
            return send_file(filename, mimetype='text/html')
        else:
            return send_file(filename)
    return f"Arquivo {filename} não encontrado", 404

# ===== ROTA PRINCIPAL =====
@app.route('/')
def home():
    """Servir a página principal"""
    html_file = find_ebook_html()

    if html_file:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return html_content
        except Exception as e:
            return f"<html><body><h1>Erro ao ler HTML</h1><p>{e}</p></body></html>"
    
    return """
    
```<body>
        <h1>Ebook não encontrado</h1>
        <p>Arquivos encontrados: {files}</p>
        <p><a href="/debug">Ver debug</a></p>
    </body>```

    """.format(files=', '.join(os.listdir('.')))

# ===== ROTAS DE DEBUG =====
@app.route('/debug')
def debug():
    """Debug informações"""
    return jsonify({
        "current_dir": os.getcwd(),
        "files_in_dir": os.listdir('.'),
        "html_found": bool(find_ebook_html()),
        "css_exists": os.path.exists('base.css'),
        "js_exists": os.path.exists('lucide.min.js') and os.path.exists('turn.min.js'),
        "debug_info": "COM ROTA DE ARQUIVOS ESTÁTICOS"
    })

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "app": "GERADOR_EBOOK_FINAL_DEPLOY", 
        "static_files_ok": os.path.exists('base.css'),
        "static_files_size": {
            "base.css": os.path.getsize('base.css') if os.path.exists('base.css') else 0,
            "lucide.js": os.path.getsize('lucide.min.js') if os.path.exists('lucide.min.js') else 0,
            "turn.js": os.path.getsize('turn.min.js') if os.path.exists('turn.min.js') else 0
        }
    })

def find_ebook_html():
    """Encontra o arquivo HTML"""
    for path in ["ebook_reader.html", "app/ebook_reader.html"]:
        if os.path.exists(path):
            return path
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"Servidor iniciando - Port: {port}")
    print(f"Arquivos: {os.listdir('.')}")
    app.run(host='0.0.0.0', port=port)