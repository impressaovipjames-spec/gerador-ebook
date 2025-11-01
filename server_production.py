from flask import Flask, jsonify
import os

app = Flask(__name__)

def find_ebook_html():
    """Busca o arquivo HTML em múltiplos caminhos"""
    possible_paths = [
        'app/leitor/ebook_reader.html',
        '/opt/render/project/src/app/leitor/ebook_reader.html',
        './app/leitor/ebook_reader.html'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

@app.route('/')
def home():
    """Página principal - serve o ebook_reader.html"""
    try:
        html_path = find_ebook_html()
        if not html_path:
            return """
            <h1>Arquivo HTML não encontrado</h1>
            <p>Caminhos procurados:</p>
            <ul>
                <li>app/leitor/ebook_reader.html</li>
                <li>/opt/render/project/src/app/leitor/ebook_reader.html</li>
                <li>./app/leitor/ebook_reader.html</li>
            </ul>
            <p>Diretório atual: """ + os.getcwd() + """</p>
            <p>Arquivos em app/: """ + str(os.listdir('app')) if os.path.exists('app') else 'app/ não existe' + """</p>
            """, 404
        
        # Ler o arquivo
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 Servindo {len(content)} caracteres do arquivo {html_path}")
        return content
        
    except Exception as e:
        return f"""
        <h1>Erro ao ler arquivo</h1>
        <p>Erro: {str(e)}</p>
        <p>Diretório atual: {os.getcwd()}</p>
        """, 500

@app.route('/api/health')
def health():
    """Health check"""
    html_path = find_ebook_html()
    
    if html_path and os.path.exists(html_path):
        file_size = os.path.getsize(html_path)
        return jsonify({
            "status": "healthy",
            "server_type": "clean_version",
            "html_found": True,
            "html_path": html_path,
            "html_size": file_size,
            "current_dir": os.getcwd(),
            "app_exists": os.path.exists('app'),
            "leitor_exists": os.path.exists('app/leitor')
        })
    else:
        return jsonify({
            "status": "unhealthy",
            "server_type": "clean_version",
            "html_found": False,
            "error": "HTML file not found",
            "current_dir": os.getcwd()
        }), 404

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

@app.route('/api/exports')
def exports():
    """API exports - manter compatibilidade"""
    return jsonify({"status": "exports endpoint working"})

if __name__ == '__main__':
    print("🚀 Iniciando servidor limpo...")
    print(f"📁 Diretório: {os.getcwd()}")
    
    html_path = find_ebook_html()
    if html_path:
        print(f"✅ HTML encontrado: {html_path}")
    else:
        print("❌ HTML não encontrado!")
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Porta: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)