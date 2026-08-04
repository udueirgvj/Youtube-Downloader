from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def handler():
    if request.method == 'GET':
        return jsonify({'status': 'ok', 'message': 'Youtube Downloader API is running'})
    
    data = request.json
    url = data.get('url') if data else None
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    ydl_opts = {
        # لا نختار صيغة تحتاج دمج فيديو+صوت (ffmpeg غير متوفر في السيرفرلس)
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'socket_timeout': 20,
        'http_headers': {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/124.0.0.0 Safari/537.36'
            )
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'download_url': info.get('url'),
                'title': info.get('title', 'video'),
                'status': 'ok'
            })
    except yt_dlp.utils.DownloadError as e:
        # غالبًا يوتيوب بيحجب IP السيرفر أو الرابط غير صالح
        return jsonify({'error': f'فشل استخراج الفيديو: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel needs this
app.debug = False
