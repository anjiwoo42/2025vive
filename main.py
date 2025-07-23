import streamlit as st
import random
from collections import defaultdict

# 메뉴 + 가격 데이터 (단위: 원)
menu_data = {
    "한식": {
        "김치찌개": 8000,
        "불고기": 10000,
        "비빔밥": 8500,
        "제육볶음": 9000,
        "된장찌개": 7500
    },
    "중식": {
        "짜장면": 6000,
        "짬뽕": 7000,
        "탕수육": 12000,
        "마라탕": 11000,
        "꿔바로우": 13000
    },
    "일식": {
        "초밥": 14000,
        "우동": 7500,
        "규동": 9000,
        "돈까스": 8500,
        "라멘": 9500
    },
    "양식": {
        "파스타": 13000,
        "피자": 15000,
        "스테이크": 20000,
        "햄버거": 9000,
        "리조또": 12000
    },
    "기타": {
        "샐러드": 7000,
        "분식": 6000,
        "도시락": 8000,
        "샌드위치": 6500,
        "컵밥": 5500
    }
}

# 세션 상태 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

if 'current_menu' not in st.session_state:
    st.session_state.current_menu = None

st.title("🍱 오늘 점심 뭐 먹지?")

# 선택한 카테고리
selected_categories = st.multiselect(
    "먹고 싶은 음식 종류를 골라보세요!", 
    options=list(menu_data.keys()), 
    default=list(menu_data.keys())
)

# 평점 기반 추천 확률 가중치 계산
def get_weighted_menu_list(menu_dicts, history):
    rating_map = defaultdict(list)
    for entry in history:
        rating_map[entry["menu"]].append(entry["rating"])

    weighted_menu = []
    for menu_name, price in menu_dicts.items():
        if rating_map[menu_name]:
            avg_rating = sum(rating_map[menu_name]) / len(rating_map[menu_name])
            weight = round(avg_rating)
        else:
            weight = 1
        weighted_menu.extend([menu_name] * weight)
    return weighted_menu

# 추천 버튼
if st.button("메뉴 추천받기"):
    combined_menu = {}
    for category in selected_categories:
        combined_menu.update(menu_data[category])  # dict 병합

    if not combined_menu:
        st.warning("카테고리를 하나 이상 선택해 주세요!")
    else:
        weighted_menu = get_weighted_menu_list(combined_menu, st.session_state.history)
        recommendation = random.choice(weighted_menu)
        st.session_state.current_menu = recommendation
        price = combined_menu[recommendation]
        st.success(f"👉 오늘은 **{recommendation} ({price:,}원)** 어때요?")

# 평점 입력
if st.session_state.current_menu:
    st.markdown("### ⭐ 이 메뉴에 평점을 매겨주세요!")
    rating = st.slider("평점 (1점 ~ 5점)", 1, 5, 3)

    if st.button("평점 제출"):
        st.session_state.history.append({
            "menu": st.session_state.current_menu,
            "rating": rating
        })
        st.success(f"'{st.session_state.current_menu}'에 {rating}점을 주셨어요!")
        st.session_state.current_menu = None

# 평가 기록
if st.session_state.history:
    st.markdown("---")
    st.subheader("📊 내가 준 점심 평점")
    for entry in st.session_state.history:
        menu_name = entry['menu']
        price = next(
            (menu_data[cat][menu_name] for cat in menu_data if menu_name in menu_data[cat]), 
            "N/A"
        )
        st.write(f"- {menu_name} ({price:,}원) : ⭐ {entry['rating']}점")

# footer
st.markdown("---")
st.caption("© 2025 점심고민 해결소")
