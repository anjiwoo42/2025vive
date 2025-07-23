import streamlit as st
import pandas as pd
import random

# 초기 메뉴 데이터
if "menu_df" not in st.session_state:
    st.session_state.menu_df = pd.DataFrame({
        "메뉴": ["김치찌개", "제육볶음", "된장찌개", "비빔밥", "돈까스", "냉면", "우동"],
        "평점": [3, 4, 3, 5, 4, 2, 3],
        "선택횟수": [0]*7
    })

df = st.session_state.menu_df

st.title("🍱 오늘 뭐 먹지? 점심 메뉴 추천기")

# 메뉴 추천 버튼
if st.button("메뉴 추천 받기"):
    # 평점 높은 메뉴 우선 추천
    weights = df["평점"] + 1  # 평점이 높을수록 확률 높임
    recommended_menu = random.choices(df["메뉴"], weights=weights, k=1)[0]
    st.success(f"오늘의 추천 메뉴는 👉 **{recommended_menu}** 입니다!")

    # 선택 횟수 증가
    df.loc[df["메뉴"] == recommended_menu, "선택횟수"] += 1

    # 평점 매기기
    st.write("해당 메뉴의 평점을 남겨주세요:")
    new_rating = st.slider("평점 (1~5)", 1, 5, 3)
    if st.button("평점 제출"):
        idx = df[df["메뉴"] == recommended_menu].index[0]
        df.at[idx, "평점"] = round((df.at[idx, "평점"] + new_rating) / 2, 1)
        st.success("감사합니다! 평점이 반영되었습니다.")

# 메뉴 리스트 보기
with st.expander("📋 현재 메뉴 목록 보기"):
    st.dataframe(df.sort_values(by="평점", ascending=False), use_container_width=True)

# 메뉴 추가
with st.expander("➕ 새로운 메뉴 추가하기"):
    new_menu = st.text_input("새 메뉴 이름")
    if st.button("메뉴 추가"):
        if new_menu and new_menu not in df["메뉴"].values:
            new_row = pd.DataFrame([[new_menu, 3.0, 0]], columns=df.columns)
            st.session_state.menu_df = pd.concat([df, new_row], ignore_index=True)
            st.success(f"{new_menu} 메뉴가 추가되었습니다!")
        else:
            st.warning("메뉴 이름을 확인해주세요. 이미 존재하거나 빈 값입니다.")
