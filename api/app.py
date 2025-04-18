from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Configure storing location
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods = ['GET','POST'])
def home():
    return render_template('/main.html')

@app.route('/upload', methods=['POST'])
def upload_audio():

    if request.method == 'POST':
        print(request.data)
        audio_file = request.files['sound']

        # appropriate file extension check
        ALLOWED_EXT = {'wav', 'mp3', 'ogg', 'flac'}
        ext = audio_file.filename.rsplit('.', 1)[-1].lower()
        if ext not in ALLOWED_EXT:
            return jsonify({'error': f'Extension .{ext} not allowed'}), 400

        # Save with filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(save_path)


        return jsonify({
            'message': 'File received',
            'filename': audio_file.filename,
            'size_bytes': os.path.getsize(save_path)
        }), 200
    
    else:
        print("retry")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
