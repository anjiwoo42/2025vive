import streamlit as st
import random
from collections import defaultdict

# 메뉴 + 가격 + 맛집 정보
menu_data = {
    "한식": {
        "김치찌개": {
            "price": 8000,
            "restaurants": ["청진동 해장국 (서울 종로)", "진고개 (을지로)"]
        },
        "불고기": {
            "price": 10000,
            "restaurants": ["한일관 (압구정)", "백리향 (롯데호텔 소공동)"]
        },
        "비빔밥": {
            "price": 8500,
            "restaurants": ["고궁 (전주)", "진주회관 (서울 시청)"]
        }
    },
    "중식": {
        "짜장면": {
            "price": 6000,
            "restaurants": ["홍보각 (신세계백화점 본점)", "팔선 (웨스틴조선호텔)"]
        },
        "마라탕": {
            "price": 11000,
            "restaurants": ["라화쿵부 (전국 체인)", "천향 (건대)"]
        }
    },
    "일식": {
        "초밥": {
            "price": 14000,
            "restaurants": ["스시효 (청담)", "스시마츠모토 (이태원)"]
        },
        "라멘": {
            "price": 9500,
            "restaurants": ["멘야산다이메 (홍대)", "하카타분코 (서래마을)"]
        }
    },
    "양식": {
        "파스타": {
            "price": 13000,
            "restaurants": ["매듭 (이태원)", "까사마루 (합정)"]
        },
        "햄버거": {
            "price": 9000,
            "restaurants": ["버거파크 (이태원)", "다운타우너 (청담)"]
        }
    },
    "기타": {
        "샐러드": {
            "price": 7000,
            "restaurants": ["샐러디 (체인)", "그린파크 (강남)"]
        },
        "컵밥": {
            "price": 5500,
            "restaurants": ["컵밥거리 (신촌)", "엄마의컵밥 (홍대)"]
        }
    }
}

# 세션 상태 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

if 'current_menu' not in st.session_state:
    st.session_state.current_menu = None

st.title("🍱 오늘 점심 뭐 먹지?")

# 카테고리 선택
selected_categories = st.multiselect(
    "먹고 싶은 음식 종류를 골라보세요!", 
    options=list(menu_data.keys()), 
    default=list(menu_data.keys())
)

# 가중치 적용 함수
def get_weighted_menu_list(menu_dicts, history):
    rating_map = defaultdict(list)
    for entry in history:
        rating_map[entry["menu"]].append(entry["rating"])

    weighted_menu = []
    for menu_name in menu_dicts:
        ratings = rating_map[menu_name]
        weight = round(sum(ratings)/len(ratings)) if ratings else 1
        weighted_menu.extend([menu_name] * weight)
    return weighted_menu

# 추천 버튼
if st.button("메뉴 추천받기"):
    combined_menu = {}
    for category in selected_categories:
        combined_menu.update(menu_data[category])

    if not combined_menu:
        st.warning("카테고리를 하나 이상 선택해 주세요!")
    else:
        weighted_menu = get_weighted_menu_list(combined_menu, st.session_state.history)
        recommendation = random.choice(weighted_menu)
        st.session_state.current_menu = recommendation
        selected_item = combined_menu[recommendation]
        st.success(f"👉 오늘은 **{recommendation} ({selected_item['price']:,}원)** 어때요?")

        # 맛집 정보 출력
        st.markdown("#### 📍 대한민국 대표 맛집 추천:")
        for idx, place in enumerate(selected_item["restaurants"], 1):
            st.write(f"{idx}. {place}")

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

# 평가 기록 출력
if st.session_state.history:
    st.markdown("---")
    st.subheader("📊 내가 준 점심 평점")
    for entry in st.session_state.history:
        menu_name = entry['menu']
        price = next(
            (menu_data[cat][menu_name]["price"] for cat in menu_data if menu_name in menu_data[cat]), 
            "N/A"
        )
        st.write(f"- {menu_name} ({price:,}원) : ⭐ {entry['rating']}점")

# footer
st.markdown("---")
st.caption("© 2025 점심고민 해결소")
