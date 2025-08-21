import streamlit as st
import pandas as pd
from PIL import Image



if "report_log" not in st.session_state:
    st.session_state.report_log = []   # 신고 기록 리스트

if "last_detection" not in st.session_state:
    st.session_state.last_detection = None
    
    

## 타이틀
st.title('**AutocarZ - 자율주행 중 로드킬 안전 강화 및 자동 신고 서비스**')

## 사이드바

img_4 = Image.open('./logo.png')

st.sidebar.image(img_4)
st.sidebar.header('프로토타입')

select_side = st.sidebar.selectbox('프로토타입', 
                                    ['카메라', '객체 인식', '전광판', 'Map & 통계'])

img_1 = Image.open('./gorani.jpg')
img_2 = Image.open('./yolo.png')
img_3 = Image.open('./gorani_a.png')


## 페이지별 화면 구성
if select_side == '카메라':
    st.subheader('자율주행차의 카메라')
    st.write('자율주행차의 카메라로 도로 위 야생동물을 목격')
    st.image(img_1, width=700, caption='고라니는 로드킬을 가장 많이 당하는 동물 중 하나이다.')
    
elif select_side == '객체 인식':
    st.subheader('객체 인식 모델 - YOLO')
    col1, col2 = st.columns(2)
    with col1:
        st.image(img_2, width=200, caption='YOLO모델은 이미지를 한번만 보고 바로 물체를 검출하는 딥러닝 기술을 이용한 물체 검출 모델입니다.')
    with col2:
        #st.write('객체 인식 예시')
        st.image(img_3, width=700, caption='객체 인식 예시')
        
elif select_side == '전광판':
    st.subheader('도로 전광판 메시지(예시)')
    st.markdown(
        """
        <div style="
            background-color:black;
            color:white;
            font-size:32px;
            font-weight:bold;
            text-align:center;
            padding:40px;
            border-radius:10px;">
            전방 500m 야생동물 주의 ⚠️<br>
            고라니 출몰 구간, 서행하세요
        </div>
        """,
        unsafe_allow_html=True
    )
    
elif select_side == 'Map & 통계':
    st.subheader("야생동물 발견 지도 · 통계")

    # 테스트용 포인트 추가(선택)
    with st.expander("데이터가 없나요? 테스트용 포인트 추가하기"):
        col1, col2, col3 = st.columns(3)
        lat_in = col1.number_input("위도", value=37.5665, format="%.6f")
        lon_in = col2.number_input("경도", value=126.9780, format="%.6f")
        label_in = col3.text_input("종류", value="고라니")
        if st.button("테스트 포인트 추가"):
            st.session_state.report_log.append({
                "id": "TEST",
                "time": "2025-08-21 09:00:00",
                "lat": float(lat_in),
                "lon": float(lon_in),
                "label": label_in,
                "score": 0.9,
                "car_id": "DEMO-0000",
                "note": ""
            })
            try:
                st.rerun()
            except Exception:
                st.experimental_rerun()

    import pandas as pd
    df = pd.DataFrame(st.session_state.report_log)

    if df.empty:
        st.info("표시할 신고 데이터가 없습니다. '신고 & 지도'에서 한 건 이상 전송해 주세요.")
    else:
        # 1) 지도
        map_df = df.rename(columns={"lat": "latitude", "lon": "longitude"})
        st.map(map_df[["latitude", "longitude"]])

        st.markdown("### 통계")

        # 2) 통계 준비: 날짜/사건유형(event) 컬럼
        df["date"] = pd.to_datetime(df["time"], errors="coerce").dt.date
        df = df.dropna(subset=["date"])

        if "event" not in df.columns:
            # 간단 규칙: note/label에 사고 관련 키워드 있으면 '사고', 아니면 '출몰'
            def infer_event(row):
                txt = (str(row.get("note","")) + " " + str(row.get("label",""))).lower()
                keywords = ["사고", "충돌", "사체", "accident", "collision", "carcass"]
                return "사고" if any(k in txt for k in keywords) else "출몰"
            df["event"] = df.apply(infer_event, axis=1)

        # 3) 기간 필터(한 화면 공통으로 적용)
        min_d, max_d = df["date"].min(), df["date"].max()
        start_d, end_d = st.date_input("기간 선택", (min_d, max_d))
        # (스트림릿 버전에 따라 단일 날짜만 반환될 수 있어 방어)
        try:
            start, end = start_d, end_d
        except Exception:
            start, end = min_d, max_d

        fdf = df[(df["date"] >= start) & (df["date"] <= end)]

        # 4) 탭으로 보기: 일일 추이 / 빈도표 / 교차표
        tab1, tab2, tab3 = st.tabs(["일일 추이", "빈도표", "교차표"])

        with tab1:
            daily_all = fdf.groupby("date").size().reset_index(name="전체")
            st.caption("전체(출몰+사고) 일일 추이")
            if not daily_all.empty:
                st.line_chart(daily_all.set_index("date"))
            colA, colB = st.columns(2)
            with colA:
                daily_sight = fdf[fdf["event"]=="출몰"].groupby("date").size().reset_index(name="출몰")
                st.caption("출몰 일일 빈도")
                if not daily_sight.empty:
                    st.bar_chart(daily_sight.set_index("date"))
            with colB:
                daily_acc = fdf[fdf["event"]=="사고"].groupby("date").size().reset_index(name="사고")
                st.caption("사고 일일 빈도")
                if not daily_acc.empty:
                    st.bar_chart(daily_acc.set_index("date"))

        with tab2:
            st.caption("종류별 출몰 빈도")
            label_counts = fdf["label"].value_counts().reset_index(name="건수").rename(columns={"index": "종류"})
            st.dataframe(label_counts, use_container_width=True)

            st.caption("지점(격자)별 빈도")
            fdf["위도 & 경도"] = fdf.apply(lambda x: (round(float(x["lat"]), 3), round(float(x["lon"]), 3)), axis=1)
            cell_counts = fdf["위도 & 경도"].value_counts().reset_index(name="건수").rename(columns={"index": "(위도,경도)"})
            st.dataframe(cell_counts, use_container_width=True)

        with tab3:
            st.caption("일자별 야생동물 교차표")
            pivot = fdf.pivot_table(index="date", columns="label", values="id", aggfunc="count", fill_value=0)
            st.dataframe(pivot, use_container_width=True)
