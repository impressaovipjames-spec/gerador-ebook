from flask import Flask, send_file, jsonify, Response
import os
import sys

app = Flask(__name__)

def read_html_file():
    """Lê o arquivo HTML diretamente"""
    possible_paths = [
        'app/leitor/ebook_reader.html',
        '/opt/render/project/src/app/leitor/ebook_reader.html',
        './app/leitor/ebook_reader.html'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Lendo arquivo: {path}")
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"✅ Arquivo lido com sucesso: {len(content)} caracteres")
                return content
            except Exception as e:
                print(f"❌ Erro lendo arquivo: {e}")
                continue
    
    # Buscar por todo o sistema de arquivos
    print("🔍 Procurando arquivo...")
    for root, dirs, files in os.walk('.'):
        for file in files:
            if 'ebook_reader.html' in file:
                full_path = os.path.join(root, file)
                print(f"✅ Encontrado arquivo: {full_path}")
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return content
                except Exception as e:
                    print(f"❌ Erro lendo {full_path}: {e}")
                    continue
    
    raise FileNotFoundError("ebook_reader.html não encontrado")

@app.route('/')
def home():
    """Rota principal - lê e serve o arquivo HTML diretamente"""
    try:
        html_content = read_html_file()
        print(f"📄 Servindo conteúdo HTML diretamente ({len(html_content)} chars)")
        return Response(html_content, mimetype='text/html')
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}")
        return jsonify({
            "error": "Arquivo ebook_reader.html não encontrado",
            "details": str(e),
            "current_dir": os.getcwd(),
            "paths_tested": [
                'app/leitor/ebook_reader.html',
                '/opt/render/project/src/app/leitor/ebook_reader.html',
                './app/leitor/ebook_reader.html'
            ]
        }), 404
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return jsonify({
            "error": "Erro interno",
            "details": str(e),
            "current_dir": os.getcwd()
        }), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    try:
        html_content = read_html_file()
        return jsonify({
            "status": "healthy",
            "server_type": "direct_html",
            "html_found": True,
            "html_size": len(html_content),
            "current_dir": os.getcwd(),
            "has_app": os.path.exists('app'),
            "has_leitor": os.path.exists('app/leitor') if os.path.exists('app') else False
        })
    except FileNotFoundError as e:
        return jsonify({
            "status": "unhealthy",
            "server_type": "direct_html",
            "html_found": False,
            "error": str(e),
            "current_dir": os.getcwd()
        }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "server_type": "direct_html",
            "html_found": False,
            "error": str(e),
            "current_dir": os.getcwd()
        }), 500

@app.route('/debug')
def debug():
    """Debug endpoint"""
    return jsonify({
        "current_working_directory": os.getcwd(),
        "server_type": "direct_html",
        "method": "reading file directly with Response()",
        "debug": "PDF implementando Response() em vez de send_file()"
    })

@app.route('/api/exports')
def exports():
    """Existing exports endpoint"""
    return jsonify({"status": "exports endpoint working"})

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask - Lendo HTML diretamente...")
    print(f"📁 Diretório de trabalho: {os.getcwd()}")
    
    # Test reading on startup
    try:
        html_content = read_html_file()
        print(f"✅ Arquivo lido com sucesso: {len(html_content)} caracteres")
    except Exception as e:
        print(f"❌ Aviso: {e}")
    
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Servidor rodando na porta {port}")
    print(f"🔗 Acesse: http://0.0.0.0:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)