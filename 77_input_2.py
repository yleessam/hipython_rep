import streamlit as st

#checkbox
active = st.checkbox('I agree')
if active:
  st.text('Welcome....')
  
#함수, on_change=checkbox_write

