from flask import Flask, send_file, jsonify
import os
import sys

app = Flask(__name__)

def find_ebook_reader():
    """Encontra o arquivo ebook_reader.html com múltiplas tentativas"""
    possible_paths = [
        'app/leitor/ebook_reader.html',
        '/opt/render/project/src/app/leitor/ebook_reader.html',
        './app/leitor/ebook_reader.html'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Encontrado: {path}")
            return os.path.abspath(path)
    
    # Se não encontrar, procurar na estrutura de arquivos
    print("🔍 Procurando arquivos HTML...")
    for root, dirs, files in os.walk('.'):
        if 'ebook_reader.html' in files:
            html_path = os.path.join(root, 'ebook_reader.html')
            print(f"✅ Encontrado por busca: {html_path}")
            return os.path.abspath(html_path)
    
    raise FileNotFoundError("ebook_reader.html não encontrado")

@app.route('/')
def home():
    """Rota principal - serve o ebook_reader.html"""
    try:
        html_path = find_ebook_reader()
        print(f"📄 Servindo arquivo: {html_path}")
        return send_file(html_path, mimetype='text/html')
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}")
        return jsonify({
            "error": "Arquivo ebook_reader.html não encontrado",
            "details": str(e),
            "current_dir": os.getcwd(),
            "files_in_dir": os.listdir('.') if '.' else "N/A"
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
    """Endpoint de saúde - verifica se tudo está funcionando"""
    try:
        # Tenta encontrar o arquivo
        html_path = find_ebook_reader()
        
        return jsonify({
            "status": "healthy",
            "server_type": "stable_debug",
            "html_found": True,
            "html_path": html_path,
            "current_dir": os.getcwd(),
            "has_app": os.path.exists('app'),
            "has_leitor": os.path.exists('app/leitor') if os.path.exists('app') else False
        })
    except FileNotFoundError as e:
        return jsonify({
            "status": "unhealthy",
            "server_type": "stable_debug",
            "html_found": False,
            "error": str(e),
            "current_dir": os.getcwd(),
            "files_in_app": os.listdir('app/leitor') if os.path.exists('app/leitor') else "N/A"
        }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "server_type": "stable_debug",
            "html_found": False,
            "error": str(e),
            "current_dir": os.getcwd()
        }), 500

@app.route('/debug')
def debug():
    """Endpoint de debug - informações detalhadas sobre o sistema"""
    debug_info = {
        "current_working_directory": os.getcwd(),
        "python_executable": sys.executable,
        "environment_variables": {
            "PORT": os.environ.get('PORT', 'Not set'),
            "PYTHONPATH": os.environ.get('PYTHONPATH', 'Not set')
        },
        "file_structure": {},
        "html_search_results": []
    }
    
    # Lista arquivos principais
    try:
        debug_info["root_files"] = os.listdir('.')
    except Exception as e:
        debug_info["root_files_error"] = str(e)
    
    # Procura por app/
    try:
        if os.path.exists('app'):
            debug_info["app_exists"] = True
            debug_info["app_contents"] = os.listdir('app')
            if os.path.exists('app/leitor'):
                debug_info["leitor_exists"] = True
                debug_info["leitor_contents"] = os.listdir('app/leitor')
        else:
            debug_info["app_exists"] = False
    except Exception as e:
        debug_info["directory_error"] = str(e)
    
    # Busca por arquivo HTML
    try:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if 'ebook_reader.html' in file:
                    full_path = os.path.join(root, file)
                    debug_info["html_search_results"].append({
                        "path": full_path,
                        "absolute_path": os.path.abspath(full_path),
                        "exists": os.path.exists(full_path),
                        "size": os.path.getsize(full_path) if os.path.exists(full_path) else 0
                    })
    except Exception as e:
        debug_info["html_search_error"] = str(e)
    
    return jsonify(debug_info)

@app.route('/api/exports')
def exports():
    """API exports - endpoint existente mantido"""
    return jsonify({"status": "exports endpoint working"})

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask estável com debug...")
    print(f"📁 Diretório de trabalho: {os.getcwd()}")
    
    # Tenta encontrar o arquivo ao iniciar
    try:
        html_path = find_ebook_reader()
        print(f"✅ Arquivo encontrado: {html_path}")
    except Exception as e:
        print(f"❌ Aviso: {e}")
    
    # Configuração para production
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Servidor rodando na porta {port}")
    print(f"🔗 Acesse: http://0.0.0.0:{port}")
    
    # Usar o servidor padrão do Flask para Render
    app.run(host='0.0.0.0', port=port, debug=False)