import streamlit as st
import random

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

st.title("🍱 오늘 점심 뭐 먹지?")

# 카테고리 선택
selected_categories = st.multiselect(
    "먹고 싶은 음식 종류를 골라보세요!",
    options=list(menu_data.keys()),
    default=list(menu_data.keys())
)

# 메뉴 추천 버튼
if st.button("메뉴 추천받기"):
    combined_menu = {}
    for category in selected_categories:
        combined_menu.update(menu_data[category])

    if not combined_menu:
        st.warning("카테고리를 하나 이상 선택해 주세요!")
    else:
        menu_name = random.choice(list(combined_menu.keys()))
        menu_info = combined_menu[menu_name]

        st.success(f"👉 오늘은 **{menu_name} ({menu_info['price']:,}원)** 어때요?")
        st.markdown("#### 📍 대한민국 대표 맛집 추천:")
        for idx, place in enumerate(menu_info["restaurants"], 1):
            st.write(f"{idx}. {place}")

# footer
st.markdown("---")
st.caption("© 2025 점심고민 해결소")
