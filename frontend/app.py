import os
import random

import pandas as pd
import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
BACKEND_ERROR = "백엔드 서버(8000번)에 연결할 수 없습니다. BE 터미널이 켜져 있는지 확인하세요."

st.set_page_config(page_title="우리 지역 체크인", page_icon="📍", layout="wide")
st.title("위치 기반 랜덤 데이터 시각화")

try:
    locations = requests.get(f"{BACKEND_URL}/locations", timeout=5).json()
except requests.exceptions.RequestException as e:
    st.error(f"백엔드 연결 실패: {e}")
    st.stop()

with st.sidebar:
    st.subheader("검색 조건")
    filter_region = st.selectbox("지역", ["전체"] + list(locations.keys()))
    filter_min_score = st.slider("최소 만족도", 1, 5, 1)
    filter_keyword = st.text_input("메모 검색")

params = {}
if filter_region != "전체":
    params["region"] = filter_region
if filter_min_score > 1:
    params["min_score"] = filter_min_score
if filter_keyword:
    params["keyword"] = filter_keyword

tab_write, tab_my, tab_all = st.tabs(["기록 남기기", "내 기록", "전체 현황"])

with tab_write:
    st.caption("이름·지역·만족도·메모를 입력해 방문 기록을 남기는 탭입니다.")

    with st.form("record_form"):
        record_name = st.text_input("이름")
        record_region = st.selectbox("지역", list(locations.keys()))
        record_score = st.slider("만족도", 1, 5, 3)
        record_memo = st.text_input("한 줄 메모")
        submitted = st.form_submit_button("기록 저장")

    if submitted:
        if not record_name:
            st.warning("이름을 입력해주세요")
        else:
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/records",
                    json={
                        "user_name": record_name,
                        "region": record_region,
                        "score": record_score,
                        "memo": record_memo,
                    },
                    timeout=5,
                )
                if resp.status_code == 201:
                    st.success(f"저장 완료! (id: {resp.json()['id']})")
                else:
                    st.error(resp.json().get("detail"))
            except requests.exceptions.RequestException:
                st.error(BACKEND_ERROR)

with tab_my:
    st.caption("이름으로 내 기록을 조회하고, 잘못 남긴 기록을 삭제하는 탭입니다.")

    query_name = st.text_input("조회할 이름")
    if st.button("내 기록 보기"):
        st.session_state["query_name"] = query_name

    if st.session_state.get("query_name"):
        try:
            user_resp = requests.get(f"{BACKEND_URL}/records/user/{st.session_state['query_name']}", timeout=5).json()
            if user_resp["count"] == 0:
                st.info(f"'{st.session_state['query_name']}' 이름으로 남긴 기록이 없습니다.")
            else:
                mcol1, mcol2 = st.columns(2)
                mcol1.metric("내 기록 수", user_resp["count"])
                mcol2.metric("평균 만족도", user_resp["avg_score"])
                st.dataframe(pd.DataFrame(user_resp["records"]))

                options = {
                    f"{r['id']} · {r['region']} · {r['score']} · {r['memo']}": r["id"]
                    for r in user_resp["records"]
                }
                selected_label = st.selectbox("삭제할 기록 선택", list(options.keys()))
                if st.button("선택한 기록 삭제"):
                    try:
                        del_resp = requests.delete(f"{BACKEND_URL}/records/{options[selected_label]}", timeout=5)
                        if del_resp.status_code == 200:
                            st.success("삭제했습니다")
                            st.rerun()
                        else:
                            st.error(del_resp.json().get("detail"))
                    except requests.exceptions.RequestException:
                        st.error(BACKEND_ERROR)
        except requests.exceptions.RequestException:
            st.error(BACKEND_ERROR)

with tab_all:
    st.caption("전체 통계, 검색 필터가 적용된 전체 기록 표, CSV 다운로드를 볼 수 있는 탭입니다.")

    st.subheader("전체 현황")
    try:
        stats_resp = requests.get(f"{BACKEND_URL}/stats", timeout=5).json()
        scol1, scol2, scol3 = st.columns(3)
        scol1.metric("총 기록 수", stats_resp["total"])
        scol2.metric("참여자 수", stats_resp["user_count"])
        scol3.metric("전체 평균 만족도", stats_resp["overall_avg"])
        if stats_resp["by_region"]:
            region_df = pd.DataFrame(stats_resp["by_region"]).set_index("region")
            st.bar_chart(region_df["avg_score"])
    except requests.exceptions.RequestException:
        st.error(BACKEND_ERROR)

    st.subheader("전체 기록")
    try:
        records_resp = requests.get(f"{BACKEND_URL}/records", params=params, timeout=5).json()
        with st.sidebar:
            st.write(f"조건에 맞는 기록: {records_resp['count']}건")
        if records_resp["count"] == 0:
            st.warning("조건에 맞는 기록이 없습니다. 조건을 완화해보세요.")
        else:
            st.dataframe(pd.DataFrame(records_resp["records"]))
            csv_resp = requests.get(f"{BACKEND_URL}/records/export.csv", params=params, timeout=5)
            st.download_button(
                "CSV로 내려받기",
                data=csv_resp.content,
                file_name="records.csv",
                mime="text/csv",
            )
    except requests.exceptions.RequestException:
        st.error(BACKEND_ERROR)

    st.caption("실습 시작 코드에 있던 데모 지도입니다. 저장된 기록과는 무관하게 랜덤 좌표를 표시합니다.")

    city = st.selectbox("지역 선택", list(locations.keys()))
    n_points = st.slider("랜덤 포인트 개수", 10, 200, 50)

    center = locations[city]

    random.seed()
    df = pd.DataFrame(
        {
            "lat": [center["lat"] + random.uniform(-0.02, 0.02) for _ in range(n_points)],
            "lon": [center["lon"] + random.uniform(-0.02, 0.02) for _ in range(n_points)],
            "value": [random.randint(1, 100) for _ in range(n_points)],
        }
    )

    col1, col2 = st.columns([2, 1])

    print("hi")
    with col1:
        st.subheader(f"{city} 지도")
        st.map(df, latitude="lat", longitude="lon", size="value")

    with col2:
        st.subheader("값 분포")
        st.bar_chart(df["value"])

    st.subheader("원본 데이터")
    st.dataframe(df)
