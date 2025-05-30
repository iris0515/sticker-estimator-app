# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1W_qDnZOBpyI-R1n7nguT1IehiUP6K6Ph
"""

import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="스티커 견적 계산기", page_icon="📐", layout="centered")

def format_number(n): return format(n, ",").replace(",", ".")
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

def format_result(n): return f"{format_number(n)} ({number_to_korean(n)})"

st.markdown("<h1 style='text-align:center; color:#00b894;'>🧾 스티커 견적 계산기</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📐 면적 계산기", "📦 헤다포장", "🎨 기타 견적"])

# ---------------- TAB 1: 면적 계산기 ----------------
with tab1:
    st.markdown("### 📐 면적 계산기 (업그레이드)")
    col1_area, col2_area, col3_area = st.columns(3)
    with col1_area:
        width = st.number_input("가로(mm)", min_value=1.0, value=50.0, step=1.0)
    with col2_area:
        height = st.number_input("세로(mm)", min_value=1.0, value=50.0, step=1.0)
    with col3_area:
        quantity = st.number_input("총 수량", min_value=1, value=100, step=1)

    sheet_type = st.selectbox("기본 용지 사이즈", ["270x400mm", "280x400mm"])

    if st.button("면적 계산", key="area_calc_btn"):
        max_width, max_height = (270, 400) if sheet_type == "270x400mm" else (280, 400)
        num_width = math.floor(max_width / width)
        num_height = math.floor(max_height / height)
        total_per_sheet = num_width * num_height

        if total_per_sheet == 0:
            st.error("❌ 해당 크기는 용지에 들어가지 않습니다.")
        else:
            total_needed_sheets = math.ceil(quantity / total_per_sheet)
            im_basis = math.ceil(quantity / 20) if total_per_sheet >= 20 else total_needed_sheets
            sticky_basis = math.ceil(quantity / 16) if total_per_sheet >= 16 else total_needed_sheets

            st.success(f"✅ 한 장당 최대 배치 수: {format_result(total_per_sheet)}개")
            st.info(f"📄 기본 수량 기준: {format_result(total_needed_sheets)}장")
            st.write(f"💡 완칼 기준 수량 (아임 기준 20개): {format_result(im_basis)}장")
            st.write(f"💡 완칼 기준 수량 (스티키 기준 16개): {format_result(sticky_basis)}장")

# ---------------- TAB 2: 헤다포장 계산기 ----------------
with tab2:
    st.markdown("### 📦 헤다포장 견적 계산기 (업그레이드)")

    st.subheader("1️⃣ 헤다 면적 계산기")
    col1_heda, col2_heda = st.columns(2)
    width_h = col1_heda.number_input("가로(mm)", min_value=1.0, value=50.0, key="heda_width")
    height_h = col2_heda.number_input("세로(mm)", min_value=1.0, value=50.0, key="heda_height")

    if st.button("면적 계산", key="heda_area_btn"):
        container_width, container_height = 255, 385
        num_width = math.floor(container_width / width_h)
        num_height = math.floor(container_height / height_h)
        total = num_width * num_height
        if total == 0:
            st.error("❌ 입력한 크기의 아이템이 컨테이너에 들어가지 않습니다.")
        else:
            st.success(f"✅ 한 장에 최대 {total}개 들어갈 수 있습니다.")

    st.divider()
    st.subheader("2️⃣ 헤다 견적 계산기")
    col3_heda, col4_heda = st.columns(2)
    quantity = col3_heda.number_input("헤다 수량", min_value=10, value=100, step=10, key="heda_quantity")
    batch_under_9 = col4_heda.checkbox("9개 이하 배치 (장당 +50원)", key="heda_under_9")
    sticker_included = col4_heda.checkbox("스티커 포함 (장당 -50원)", key="heda_with_sticker")

    if st.button("헤다 견적 계산", key="heda_price_btn"):
        if quantity >= 500:
            heda_unit = 250
        elif quantity >= 300:
            heda_unit = 300
        elif quantity >= 200:
            heda_unit = 350
        elif quantity >= 100:
            heda_unit = 400
        else:
            heda_unit = 450

        if batch_under_9:
            heda_unit += 50
        if sticker_included:
            heda_unit -= 50

        heda_total = quantity * heda_unit

        st.info(f"헤다 단가: {format_result(heda_unit)}원")
        st.success(f"헤다 견적 합계: {format_result(heda_total)}원")

    st.divider()
    st.subheader("3️⃣ 포장 견적 계산기")
    col5_heda, col6_heda = st.columns(2)
    qty_p = col5_heda.number_input("포장 수량", min_value=10, value=100, step=10, key="pack_qty")
    header_add = col6_heda.checkbox("헤더 장착 (장당 +200원)", key="pack_header")
    over_8_types = col6_heda.checkbox("8종 이상 (장당 +100원)", key="pack_8types")
    over_12_types = col6_heda.checkbox("12종 이상 (장당 +200원)", key="pack_12types")
    opp_cost = col6_heda.checkbox("OPP 포장비용 (장당 +50원)", key="pack_opp")

    if st.button("포장 견적 계산", key="pack_price_btn"):
        if qty_p >= 400:
            packaging_unit = 200
        elif qty_p >= 300:
            packaging_unit = 250
        elif qty_p >= 200:
            packaging_unit = 300
        elif qty_p >= 100:
            packaging_unit = 400
        else:
            packaging_unit = 500

        if header_add:
            packaging_unit += 200
        if over_8_types:
            packaging_unit += 100
        if over_12_types:
            packaging_unit += 200
        if opp_cost:
            packaging_unit += 50

        packaging_total = qty_p * packaging_unit

        st.info(f"포장 단가: {format_result(packaging_unit)}원")
        st.success(f"포장 견적 합계: {format_result(packaging_total)}원")

        total_sum = heda_total + packaging_total
        total_unit_price = heda_unit + packaging_unit
        st.success(f"총 견적: {format_result(total_sum)}원")
        st.info(f"장당 총합 단가: {format_result(total_unit_price)}원")

# ---------------- TAB 3 ----------------
with tab3:
    st.markdown("### 📋 일반 / 완칼 / 작가 견적 계산기")

    # 📋 일반 견적 계산기
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
        if st.button("일반 견적 계산", key="btn_general"):
            row = general_data[(general_data["스티커용지"] == g_type) & (general_data["코팅필름"] == g_coating)]
            if not row.empty:
                base_price = row["재단있을때가격"].values[0] if g_cut == "있음" else row["재단없을때가격"].values[0]
                unit_price = base_price + (500 if g_coating in ["무광", "유광"] else 0)
                total_price = unit_price * g_qty
                st.success(f"✔️ 단가: {format_result(unit_price)}원")
                st.info(f"💰 총 가격: {format_result(total_price)}원")

    # 🧷 완칼 스티키
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
        if st.button("스티키 견적 계산", key="btn_sticky"):
            row = sticky_data[(sticky_data["용지"] == s_type) & (sticky_data["코팅"] == s_coating)]
            if not row.empty:
                base = row.iloc[0]["용지가격"] + row.iloc[0]["코팅가격"]
                unit_price = base - (500 if s_qty >= 125 else 300 if s_qty >= 62 else 200 if s_qty >= 31 else 0)
                total_price = unit_price * s_qty
                st.success(f"✔️ 단가: {format_result(unit_price)}원")
                st.info(f"💰 총 가격: {format_result(total_price)}원")

    # 🧲 완칼 아임
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
        if st.button("아임 견적 계산", key="btn_aim"):
            row = im_data[(im_data["용지"] == im_type) & (im_data["코팅"] == im_coating)]
            if not row.empty:
                base = row.iloc[0]["용지가격"] + row.iloc[0]["코팅가격"]
                unit_price = base - (700 if im_qty >= 100 else 400 if im_qty >= 70 else 200 if im_qty >= 30 else 0)
                total_price = unit_price * im_qty
                st.success(f"✔️ 단가: {format_result(unit_price)}원")
                st.info(f"💰 총 가격: {format_result(total_price)}원")

    # 🎨 작가 견적
    with st.expander("🎨 작가 견적 계산기"):
        sticker = st.selectbox("스티커 용지", ["유포지", "리무버블유포지", "아트지", "리무버블아트지", "모조지", "투명스티커", "마스킹씰"])
        fuji = st.selectbox("후지 종류", ["백색후지", "투명후지"])
        coating = st.selectbox("코팅 필름", ["무광", "유광", "씰크벨벳(무광)", "스파클(모래알)", "레인보우", "별빛", "샌드스타", "매트펄", "없음"])
        cutting = st.selectbox("재단 여부", ["있음", "없음"])
        qty = st.number_input("제작 수량", min_value=1, value=100)

        if st.button("작가 견적 계산", key="btn_artist"):
            base_price_map = {
                "유포지": 2900, "리무버블유포지": 3400, "아트지": 2800,
                "리무버블아트지": 3300, "모조지": 2800, "투명스티커": 3800, "마스킹씰": 4500
            }
            coating_price_map = {
                "무광": 500, "유광": 500, "씰크벨벳(무광)": 1000, "스파클(모래알)": 1000,
                "레인보우": 1000, "별빛": 1000, "샌드스타": 1000, "매트펄": 1300, "없음": 0
            }
            def fuji_adj(sticker_type, fuji_type):
                if fuji_type == "투명후지":
                    if sticker_type == "유포지": return 1100
                    elif sticker_type == "리무버블유포지": return 800
                return 0

            unit_price = base_price_map[sticker] + coating_price_map[coating] + fuji_adj(sticker, fuji)
            if qty >= 100: unit_price -= 300
            elif qty >= 70: unit_price -= 200
            elif qty >= 30: unit_price -= 100
            if cutting == "있음": unit_price += 500

            total_price = unit_price * qty
            st.success(f"✔️ 단가: {format_result(unit_price)}원")
            st.info(f"💰 총 가격: {format_result(total_price)}원")