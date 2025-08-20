import streamlit as st

#layout 요소
# columns 는 요소를 왼쪽->오른쪽으로 배치할 수 있다

col1, col2 = st.columns(2)

with col1:
  st.metric(
    '오늘의 날씨',
    value='35도',
    delta='+3',
  )
  
with col2:
  st.metric(
    '오늘의 미세먼지',
    value='좋음',
    delta='-30',
    delta_color='inverse'
  )
  
##
st.markdown('---') 
 
data = {
   '이름': ['홍길동','김길동','박길동'],
   '나이': [10,20,30]
 }
import pandas as pd
df = pd.DataFrame(data)
st.dataframe(df)

st.divider()

st.table(df)

st.divider()

st.json(data)
