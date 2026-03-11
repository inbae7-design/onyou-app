import streamlit as st
import pandas as pd
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- 모바일 화면에 맞춘 기본 설정 ---
st.set_page_config(page_title="온유 스케줄 매니저", page_icon="👧", layout="centered")

# --- 메인 타이틀 ---
st.title("👧 온유 스케줄 매니저")
st.markdown("오늘도 즐거운 하루 보내자! 우리 쭈 화이팅! ✨")
st.divider()

# --- 구글 시트 연결 (에러 방지를 위해 임시 주석 처리) ---
# 실제 시트와 연결하실 때 아래 주석(#)을 풀고 사용하세요.
# @st.cache_resource
# def init_connection():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds_dict = json.loads(os.environ["google_json"]) # Koyeb 환경변수 사용
#     creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
#     return gspread.authorize(creds)
# 
# client = init_connection()

# --- 화면 탭 구성 (스케줄 / 용돈 기입장) ---
tab1, tab2 = st.tabs(["📅 오늘 스케줄", "💰 용돈 기입장"])

with tab1:
    st.subheader("✅ 오늘의 할 일과 학원")
    
    # 임시 데이터 (나중에 구글 시트 데이터로 교체)
    schedule_data = pd.DataFrame(
        [
            {"시간": "14:00", "일정": "피아노 학원", "완료": False},
            {"시간": "16:00", "일정": "영어 학원", "완료": False},
            {"시간": "18:00", "일정": "숙제하기", "완료": False}
        ]
    )
    
    # 체크박스가 있는 표 만들기
    edited_df = st.data_editor(schedule_data, num_rows="dynamic", use_container_width=True)
    
    if st.button("스케줄 저장하기", key="btn_schedule"):
        st.success("스케줄이 저장되었습니다! (구글 시트 연동 전)")

with tab2:
    st.subheader("💸 어디에 썼을까요?")
    
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        with col1:
            item = st.text_input("어디에 썼나요? (예: 아이스크림)")
        with col2:
            price = st.number_input("얼마인가요?", min_value=0, step=100)
            
        category = st.selectbox("카테고리", ["간식", "준비물", "장난감", "기타"])
        
        submitted = st.form_submit_button("지출 기록하기")
        if submitted:
            st.success(f"{item} ({price}원) 기록 완료! (구글 시트 연동 전)")
