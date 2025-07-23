import streamlit as st
import random

# 점심 메뉴 데이터
menu_data = {
    "한식": ["김치찌개", "불고기", "비빔밥", "제육볶음", "된장찌개"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마라탕", "꿔바로우"],
    "일식": ["초밥", "우동", "규동", "돈까스", "라멘"],
    "양식": ["파스타", "피자", "스테이크", "햄버거", "리조또"],
    "기타": ["샐러드", "분식", "도시락", "샌드위치", "컵밥"]
}

st.title("🍱 오늘 점심 뭐 먹지?")

# 선택한 카테고리
selected_categories = st.multiselect(
    "먹고 싶은 음식 종류를 골라보세요!", 
    options=list(menu_data.keys()), 
    default=list(menu_data.keys())
)

# 추천 버튼
if st.button("메뉴 추천받기"):
    # 선택한 카테고리에서 메뉴 리스트 생성
    combined_menu = []
    for category in selected_categories:
        combined_menu.extend(menu_data[category])
    
    if not combined_menu:
        st.warning("카테고리를 하나 이상 선택해 주세요!")
    else:
        recommendation = random.choice(combined_menu)
        st.success(f"👉 오늘은 **{recommendation}** 어때요?")
        st.caption("마음에 안 들면 다시 추천 버튼을 눌러보세요 😉")

# footer
st.markdown("---")
st.caption("© 2025 점심고민 해결소")
