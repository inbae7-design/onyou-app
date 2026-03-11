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

# --- 메인 탭 3개 구성 ---
tab_todo, tab_schedule, tab_account = st.tabs(["✅ 오늘 할 일", "🗓️ 주간 시간표", "💰 온유 가계부"])

# ==========================================
# 1. 오늘 할 일 (체크리스트 유지)
# ==========================================
with tab_todo:
    st.subheader("오늘의 할 일과 일정")
    
    # 임시 데이터
    schedule_data = pd.DataFrame(
        [
            {"시간": "14:00", "일정": "피아노 학원", "완료": False},
            {"시간": "16:00", "일정": "영어 학원", "완료": False},
            {"시간": "18:00", "일정": "숙제하기", "완료": False}
        ]
    )
    
    # 체크박스가 있는 표 만들기
    edited_df = st.data_editor(schedule_data, num_rows="dynamic", use_container_width=True)
    
    if st.button("체크리스트 저장", key="btn_todo"):
        st.success("스케줄이 저장되었습니다! (구글 시트 연동 전)")


# ==========================================
# 2. 주간 시간표 (학교/학원 하위 메뉴)
# ==========================================
with tab_schedule:
    st.subheader("월~일 시간표 관리")
    
    # 하위 탭 생성
    sub_school, sub_academy = st.tabs(["🏫 학교 시간표", "🎒 학원 시간표"])
    
    # 시간표 기본 뼈대 (월~일)
    weekly_template = pd.DataFrame({
        "시간/교시": ["1교시", "2교시", "3교시", "4교시", "5교시", "6교시", "방과후"],
        "월": ["", "", "", "", "", "", ""],
        "화": ["", "", "", "", "", "", ""],
        "수": ["", "", "", "", "", "", ""],
        "목": ["", "", "", "", "", "", ""],
        "금": ["", "", "", "", "", "", ""],
        "토": ["", "", "", "", "", "", ""],
        "일": ["", "", "", "", "", "", ""]
    })

    with sub_school:
        st.markdown("**표 안의 빈칸을 터치해서 과목을 입력하세요.**")
        st.data_editor(weekly_template.copy(), num_rows="dynamic", use_container_width=True, key="school_table")
        if st.button("학교 시간표 저장", key="btn_school"):
            st.success("학교 시간표가 저장되었습니다!")

    with sub_academy:
        st.markdown("**표 안의 빈칸을 터치해서 학원 일정을 입력하세요.**")
        st.data_editor(weekly_template.copy(), num_rows="dynamic", use_container_width=True, key="academy_table")
        if st.button("학원 시간표 저장", key="btn_academy"):
            st.success("학원 시간표가 저장되었습니다!")


# ==========================================
# 3. 온유 가계부 (학원비/생활비/용돈 하위 메뉴)
# ==========================================
with tab_account:
    st.subheader("우리가족 지출 관리")
    
    # 하위 탭 생성
    sub_academy_fee, sub_living, sub_allowance = st.tabs(["🎒 학원비", "🛒 생활비", "💸 용돈 기입장"])
    
    # 가계부 입력을 위한 공통 폼 함수
    def create_expense_form(form_key, title):
        with st.form(form_key):
            st.markdown(f"**{title} 입력하기**")
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("날짜")
                item = st.text_input("내역 (어디에 썼나요?)")
            with col2:
                price = st.number_input("금액 (원)", min_value=0, step=100)
                note = st.text_input("메모")
                
            submitted = st.form_submit_button(f"{title} 기록하기")
            if submitted:
                st.success(f"{date} | {item} ({price}원) 기록 완료!")

    with sub_academy_fee:
        create_expense_form("form_academy_fee", "학원비")
        
    with sub_living:
        create_expense_form("form_living", "생활비")
        
    with sub_allowance:
        create_expense_form("form_allowance", "용돈 기입장")
