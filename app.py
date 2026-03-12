from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import json
import os
import io

app = Flask(__name__)

# ★여기에 아까 복사해둔 구글 드라이브 '폴더 ID'를 따옴표 안에 넣어주세요!★
FOLDER_ID = "11uYn0zVbCyr_IecC6MuozB_kk7TSPpId?hl=ko"

def get_credentials():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(os.environ["google_json"])
    return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

def get_sheet():
    client = gspread.authorize(get_credentials())
    return client.open("온유스케줄").worksheet("데이터")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/load', methods=['GET'])
def load_data():
    try:
        sheet = get_sheet()
        records = sheet.get_all_records()
        data = {str(row['Key']): str(row['Value']) for row in records}
        return jsonify(data)
    except Exception as e:
        return jsonify({}), 200

@app.route('/api/save', methods=['POST'])
def save_data():
    try:
        data = request.json
        sheet = get_sheet()
        rows = [['Key', 'Value']]
        for k, v in data.items():
            rows.append([str(k), str(v)])
        sheet.clear()
        try:
            sheet.update(values=rows, range_name='A1')
        except TypeError:
            sheet.update('A1', rows)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ★사진 업로드를 처리하는 새로운 기능★
@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    
    try:
        creds = get_credentials()
        drive_service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {'name': file.filename, 'parents': [FOLDER_ID]}
        media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.mimetype, resumable=True)
        
        # 1. 드라이브에 파일 올리기
        uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = uploaded_file.get('id')
        
        # 2. 누구나 앱에서 사진을 볼 수 있도록 권한 열어주기
        drive_service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
        
        # 3. 화면에 보여줄 이미지 주소 만들기
        img_url = f"https://drive.google.com/uc?id={file_id}"
        return jsonify({"url": img_url})
    except Exception as e:
        print("사진 업로드 에러:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
