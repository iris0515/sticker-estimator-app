import streamlit as st
import math
import pandas as pd

# ---------- 공용 설정 ----------
st.set_page_config(page_title="스티커 견적 계산기", page_icon="📐", layout="centered")

# ---------- 공용 함수 ----------
def format_number(n):
    return format(n, ",").replace(",", ".")

def number_to_korean(num):
    digits = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
    units = ["", "십", "백", "천"]
    big_units = ["", "만", "억", "조", "경"]
    result, group = "", 0
    while num > 0:
        part, part_str = num % 10000, ""
        num //= 10000
        for i in range(4):
            d = part % 10
            part //= 10
            if d != 0:
                part_str = (units[i] if d == 1 and i > 0 else digits[d] + units[i]) + part_str
        result = part_str + big_units[group] + result if part_str else result
        group += 1
    return result

def format_result(n):
    return f"{format_number(n)} ({number_to_korean(n)})"

# ---------- 스타일 ----------
st.markdown("""
    <style>
    .main { background-color: #f8fcfb; }
    .stButton>button {
        background-color: #00b894;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        font-weight: bold;
    }
    .stTabs [role="tab"] {
        font-size: 18px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- 제목 ----------
st.markdown("<h1 style='text-align:center; color:#00b894;'>🧾 스티커 견적 계산기</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>모든 견적을 하나의 앱에서 간편하게 계산해보세요!</p>", unsafe_allow_html=True)

# ---------- 탭 ----------
tab1, tab2, tab3 = st.tabs(["📐 면적 계산기", "🎨 작가 견적", "📦 일반/완칼/헤다"])

# ---------- 면적 계산기 ----------
with tab1:
    st.markdown("### 🧮 스티커 면적 계산기")
    with st.form("area_calc"):
        col1, col2 = st.columns(2)
        with col1:
            width = st.number_input("가로(mm)", min_value=1.0, value=50.0)
            quantity = st.number_input("총 수량", min_value=1, value=100)
        with col2:
            height = st.number_input("세로(mm)", min_value=1.0, value=50.0)
            sheet_type = st.selectbox("기본 용지 사이즈", ["270x400mm", "280x400mm"])
        submitted = st.form_submit_button("계산하기")

        if submitted:
            max_width, max_height = (270, 400) if sheet_type == "270x400mm" else (280, 400)
            total = math.floor(max_width / width) * math.floor(max_height / height)
            divided_ceil = math.ceil(quantity / total)
            im_qty = math.ceil(quantity / 20) if total >= 20 else divided_ceil
            sticky_qty = math.ceil(quantity / 16) if total >= 16 else divided_ceil

            st.success(f"총 {format_result(total)}개 들어갈 수 있습니다.")
            st.info(f"기본 수량: {format_result(divided_ceil)}개")
            st.write(f"완칼(아임): {format_result(im_qty)}개 / 완칼(스티키): {format_result(sticky_qty)}개")

# ---------- 작가 견적 계산기 ----------
with tab2:
    st.markdown("### 🎨 작가 견적 계산기")
    with st.form("artist_calc"):
        sticker = st.selectbox("스티커 용지", ["유포지", "리무버블유포지", "아트지", "리무버블아트지", "모조지", "투명스티커", "마스킹씰"])
        fuji = st.selectbox("후지 종류", ["백색후지", "투명후지"])
        coating = st.selectbox("코팅 필름", ["무광", "유광", "씰크벨벳(무광)", "스파클(모래알)", "레인보우", "별빛", "샌드스타", "매트펄", "없음"])
        cutting = st.selectbox("재단 여부", ["있음", "없음"])
        qty = st.number_input("제작 수량", min_value=1, value=100)
        calc = st.form_submit_button("견적 계산")

        if calc:
            base = {"유포지": 2900, "리무버블유포지": 3400, "아트지": 2800,
                    "리무버블아트지": 3300, "모조지": 2800, "투명스티커": 3800, "마스킹씰": 4500}
            adj = {"무광": 500, "유광": 500, "씰크벨벳(무광)": 1000, "스파클(모래알)": 1000, "레인보우": 1000,
                   "별빛": 1000, "샌드스타": 1000, "매트펄": 1300, "없음": 0}
            def fuji_adj(s, f): return 1100 if f == "투명후지" and s == "유포지" else 800 if f == "투명후지" and s == "리무버블유포지" else 0

            unit = base[sticker] + adj[coating] + fuji_adj(sticker, fuji)
            if qty >= 100: unit -= 300
            elif qty >= 70: unit -= 200
            elif qty >= 30: unit -= 100
            if cutting == "있음": unit += 500
            total = unit * qty

            st.success(f"단가: {format_result(unit)}원")
            st.info(f"총 가격: {format_result(total)}원")

with tab3:
    st.markdown("### 📦 일반 / 완칼 / 헤다포장 계산기")

    with st.expander("📋 일반 견적 계산기"):
        general_data = pd.DataFrame({
            "스티커용지": ["유포지"] * 3 + ["리무버블유포지"] * 3 + ["아트지"] * 3,
            "코팅필름": ["무광", "유광", "없음"] * 3,
            "재단없을때가격": [5000, 5000, 5000, 5500, 5500, 5500, 4500, 4500, 4500],
            "재단있을때가격": [7000, 7000, 7000, 7500, 7500, 7500, 6500, 6500, 6500]
        })

        g_type = st.selectbox("스티커 용지 (일반)", general_data["스티커용지"].unique())
        g_coating = st.selectbox("코팅 필름 (일반)", ["무광", "유광", "없음"])
        g_cut = st.selectbox("재단 여부 (일반)", ["있음", "없음"])
        g_qty = st.number_input("제작 수량 (일반)", min_value=1, value=100)
        if st.button("일반 견적 계산"):
            row = general_data[(general_data["스티커용지"] == g_type) & (general_data["코팅필름"] == g_coating)]
            if not row.empty:
                unit_price = row["재단있을때가격"].values[0] if g_cut == "있음" else row["재단없을때가격"].values[0]
                if g_coating in ["무광", "유광"]:
                    unit_price += 500
                total = unit_price * g_qty
                st.success(f"단가: {format_result(unit_price)}원")
                st.info(f"총 가격: {format_result(total)}원")
            else:
                st.error("선택한 옵션의 데이터를 찾을 수 없습니다.")

    with st.expander("🧷 완칼 견적 계산기 (스티키)"):
        sticky_data = pd.DataFrame([
            {"용지": "프리미엄완칼", "코팅": "유광", "용지가격": 5000, "코팅가격": 500},
            {"용지": "프리미엄완칼", "코팅": "스파클", "용지가격": 5000, "코팅가격": 1000},
            {"용지": "유포지", "코팅": "매트펄", "용지가격": 4000, "코팅가격": 1300},
            {"용지": "아트지", "코팅": "벨벳무광", "용지가격": 3800, "코팅가격": 1000}
        ])
        s_type = st.selectbox("스티커 용지 (스티키)", sticky_data["용지"].unique())
        s_coating = st.selectbox("코팅 필름 (스티키)", sticky_data[sticky_data["용지"] == s_type]["코팅"].unique())
        s_qty = st.number_input("제작 수량 (스티키)", min_value=1, value=100)
        if st.button("스티키 견적 계산"):
            row = sticky_data[(sticky_data["용지"] == s_type) & (sticky_data["코팅"] == s_coating)]
            if not row.empty:
                base = row.iloc[0]["용지가격"] + row.iloc[0]["코팅가격"]
                if s_qty >= 125:
                    unit_price = base - 500
                elif s_qty >= 62:
                    unit_price = base - 300
                elif s_qty >= 31:
                    unit_price = base - 200
                else:
                    unit_price = base
                st.success(f"단가: {format_result(unit_price)}원")
                st.info(f"총 가격: {format_result(unit_price * s_qty)}원")

    with st.expander("🧲 완칼 견적 계산기 (아임)"):
        im_data = pd.DataFrame([
            {"용지": "아트지", "코팅": "무광", "용지가격": 4100, "코팅가격": 500},
            {"용지": "아트지", "코팅": "스파클(모래알)", "용지가격": 4100, "코팅가격": 1000},
            {"용지": "리무버블아트지", "코팅": "벨벳무광", "용지가격": 5100, "코팅가격": 1000},
            {"용지": "유포지", "코팅": "유광", "용지가격": 4500, "코팅가격": 500},
            {"용지": "리무버블유포지", "코팅": "별빛", "용지가격": 5500, "코팅가격": 1000}
        ])
        im_type = st.selectbox("스티커 용지 (아임)", im_data["용지"].unique())
        im_coating = st.selectbox("코팅 필름 (아임)", im_data[im_data["용지"] == im_type]["코팅"].unique())
        im_qty = st.number_input("제작 수량 (아임)", min_value=1, value=100)
        if st.button("아임 견적 계산"):
            row = im_data[(im_data["용지"] == im_type) & (im_data["코팅"] == im_coating)]
            if not row.empty:
                base = row.iloc[0]["용지가격"] + row.iloc[0]["코팅가격"]
                if im_qty >= 100: unit_price = base - 700
                elif im_qty >= 70: unit_price = base - 400
                elif im_qty >= 30: unit_price = base - 200
                else: unit_price = base
                st.success(f"단가: {format_result(unit_price)}원")
                st.info(f"총 가격: {format_result(unit_price * im_qty)}원")

    with st.expander("📦 헤다포장 견적 계산기"):
        h_count = st.number_input("포장할 제품 수량", min_value=1, value=100)
        h_per_pack = st.number_input("몇 개씩 포장할까요?", min_value=1, value=5)
        h_material_price = st.number_input("1세트 포장재 단가 (원)", min_value=0, value=200)
        h_handling_price = st.number_input("1세트 포장 작업비 (원)", min_value=0, value=300)

        if st.button("헤다포장 견적 계산"):
            pack_count = math.ceil(h_count / h_per_pack)
            unit_price = h_material_price + h_handling_price
            total_price = unit_price * pack_count
            st.success(f"필요한 포장 세트 수: {format_result(pack_count)}세트")
            st.info(f"단가: {format_result(unit_price)}원")
            st.info(f"총 가격: {format_result(total_price)}원")   