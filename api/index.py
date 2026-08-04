from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def handler():
    if request.method == 'GET':
        return jsonify({'status': 'ok', 'message': 'Youtube Downloader API is running'})
    
    # ✅ معالجة طلبات POST
    data = request.json
    url = data.get('url') if data else None
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'download_url': info.get('url'),
                'title': info.get('title', 'video'),
                'status': 'ok'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
