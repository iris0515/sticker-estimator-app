import streamlit as st
import math
import pandas as pd

def format_number(n):
    return format(n, ",").replace(",", ".")

def number_to_korean(num):
    digits = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
    units = ["", "십", "백", "천"]
    big_units = ["", "만", "억", "조", "경"]
    result = ""
    group = 0
    while num > 0:
        part = num % 10000
        num //= 10000
        part_str = ""
        for i in range(4):
            d = part % 10
            part //= 10
            if d != 0:
                if i > 0 and d == 1:
                    part_str = units[i] + part_str
                else:
                    part_str = digits[d] + units[i] + part_str
        if part_str:
            result = part_str + big_units[group] + result
        group += 1
    return result

def format_result(n):
    formatted = format_number(n)
    return f"{formatted} ({number_to_korean(n)})"

st.title(":memo: 스티커 견적 계산기")

# 면적 계산기
st.header("1. 면적 계산기")
col1, col2, col3 = st.columns(3)
with col1:
    width = st.number_input("가로(mm)", min_value=1.0, step=1.0, value=50.0)
with col2:
    height = st.number_input("세로(mm)", min_value=1.0, step=1.0, value=50.0)
with col3:
    quantity = st.number_input("총 수량", min_value=1, step=1, value=100)
sheet_type = st.selectbox("기본 용지 사이즈 선택", ["270x400mm", "280x400mm"])
if st.button("면적 계산"):
    max_width, max_height = (270, 400) if sheet_type == "270x400mm" else (280, 400)
    num_width = math.floor(max_width / width)
    num_height = math.floor(max_height / height)
    total = num_width * num_height
    divided_ceil = math.ceil(quantity / total)
    im_qty = math.ceil(quantity / 20) if total >= 20 else divided_ceil
    sticky_qty = math.ceil(quantity / 16) if total >= 16 else divided_ceil
    st.success(f"총 {format_result(total)}개 들어갈 수 있습니다.")
    st.info(f"기본 수량: {format_result(divided_ceil)}개")
    st.write(f"완칼격적(아임): {format_result(im_qty)}개")
    st.write(f"완칼(스티키): {format_result(sticky_qty)}개")

# (다른 견적 기능들은 여기에 추가해 주세요)