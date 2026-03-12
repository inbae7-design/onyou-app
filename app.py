from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

app = Flask(__name__)

# 구글 시트 연결 함수
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(os.environ["google_json"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    # '온유스케줄' 파일의 '데이터' 시트를 엽니다.
    return client.open("온유스케줄").worksheet("데이터")

@app.route('/')
def home():
    return render_template('index.html')

# 1. 시트에서 데이터 불러오기 (Load)
@app.route('/api/load', methods=['GET'])
def load_data():
    try:
        sheet = get_sheet()
        records = sheet.get_all_records() # A1(Key), B1(Value) 기준
        data = {str(row['Key']): str(row['Value']) for row in records}
        return jsonify(data)
    except Exception as e:
        print("불러오기 에러:", e)
        return jsonify({}), 200 # 에러가 나도 빈 화면이 뜨게 방어

# 2. 시트에 데이터 저장하기 (Save)
@app.route('/api/save', methods=['POST'])
def save_data():
    try:
        data = request.json
        sheet = get_sheet()
        
        # 구글 시트에 넣을 표 형태로 변환
        rows = [['Key', 'Value']]
        for k, v in data.items():
            rows.append([str(k), str(v)])
            
        sheet.clear() # 기존 내용을 싹 지우고
        try:
            sheet.update(values=rows, range_name='A1') # 새 내용으로 덮어쓰기 (최신버전)
        except TypeError:
            sheet.update('A1', rows) # (구버전 호환용)
            
        return jsonify({"status": "success"})
    except Exception as e:
        print("저장 에러:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
