import streamlit as st

#checkbox
active = st.checkbox('I agree')
if active:
  st.text('Welcome....')
  
#함수, on_change=checkbox_write
def checkbox_write():
    st.write('뭐먹을래?')

st.checkbox('배고파', on_change=checkbox_write)

## 세션-상태 값에 저장
if 'checkbox_state' not in st.session_state:
  st.session_state.checkbox_state = False
  
def checkbox_write1():
    st.session_state.checkbox_state = True

if st.session_state.checkbox_state :
  st.write('응...')
      
st.checkbox('진짜 누를래???', on_change=checkbox_write1)

st.divider()
# 토글 버튼

selected = st.toggle('Turn on the switch!!')
if selected:
  st.text('turn on!')
else:
  st.text('turn off')
  
# selectbox 선택지
option = st.selectbox(
  '점심메뉴고르기',
  options=['김밥', '떡볶이', '우동', '쫄면'],
  index=None,
  placeholder='네 개 중 하나만 골라야돼 '
)
st.text(f'오늘의 점심메뉴는 : {option}')

# radio
genre = st.radio(
  '무슨 영화를 좋아하세요', ['멜로', '스릴러', '판타지'],
  captions=['봄날은 간다', '트리거', '웬즈데이같은']
)
st.text(f'당신이 좋아하는 장르는 {genre}')

#multiselect
menus = st.multiselect(
  '먹고 싶은 다 골라', ['김밥', '떡볶이', '우동', '쫄면'],
)
st.text(f'내가 선택한 메뉴는 {menus}')

#slider
score = st.slider('내 점수 선택', 0, 100, 10) #start, end, init-value
st.text(f'score : {score}')

from datetime import time
st_time, end_time = st.slider(
  '공부시간 선택',
  min_value = time(0), max_value=time(11),
  value=(time(9), time(18)),
  format='HH:mm'
)
st.text(f'공부시간 : {st_time} ~ {end_time}')

# text_input
txt1 = st.text_input('영화제목', placeholder='제목을 입력하세요')
txt2 = st.text_input('비밀번호', placeholder='비밀번호를 입력하세요', type='password')
st.text(f'텍스트 입력 결과 : {txt1} , {txt2}')

import pandas as pd

# 파일업로더
# 업로드한 파일은 사용자의 세션에 있습니다. 화면을 갱신하면 사라집니다.
# 서버에 저장하려면 별도로 구현해야 합니다.
# 데이터베이스에 저장하는 로직도 구현할 수 있습니다.

file = st.file_uploader(
  '파일 선택', type='csv', accept_multiple_files=False
)
if file is not None:
  df = pd.read_csv(file)
  st.write(df)
  
  with open(file.name, 'wb') as out:
    out.write(file.getbuffer())
  
