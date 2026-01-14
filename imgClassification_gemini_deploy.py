import os
from PIL import Image
import google.genai as genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def classify_image(prompt, image, model = "gemini-2.0-flash"):
    response = client.models.generate_content(
        model=model, 
        contents=[prompt, image]
    )
    return response.text

#모델이 이미지 분류 요청 함수 정의하기
#GPT에게 보낼 프롬프트 정의
prompt = """
영상을 보고 다음 보기 내용이 포함되면 1, 포함되지 않으면 0으로 분류해줘.
보기 = [건축물, 바다, 산]
JSON format으로 키는 'building', 'sea', 'mountain'으로 하고 각각 건축물, 바다, 산에 대응되도록 출력해줘.
자연 이외의 건축물이 조금이라도 존재하면 'building'을 1로, 물이 조금이라도 존재하면 'sea'을 1로, 산이 조금이라도 보이면 'mountain'을 1로 설정해줘.
markdown format은 포함하지 말아줘.
"""

import streamlit as st

st.set_page_config(
    page_title="Image Classification - Gemini",
    page_icon="🖥",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("이미지 분류기 - Gemini")
#1) model 선택하기 : st.sidebar / st.selectbox
with st.sidebar:
    model = st.selectbox("모델 선택",
                         options = ["gemini-2.0-flash"],
                         index = 0)
#2) prompt 작성하기 : st.text_area
prompt = """
영상을 보고 다음 보기 내용이 포함되면 1, 포함되지 않으면 0으로 분류해줘.
보기 = [건축물, 바다, 산]
JSON format으로 키는 'building', 'sea', 'mountain'으로 하고 각각 건축물, 바다, 산에 대응되도록 출력해줘.
자연 이외의 건축물이 조금이라도 존재하면 'building'을 1로, 물이 조금이라도 존재하면 'sea'을 1로, 산이 조금이라도 보이면 'mountain'을 1로 설정해줘.
markdown format은 포함하지 말아줘.
"""
st.text_area("프롬프트 입력", value = prompt, height = 200)
#3) 이미지 업로드 하기 : st.file_uploader
uploaded_file = st.file_uploader ("이미지 업로드", type = ["jpe", "jpeg", "png"])
#4) 업로드한 이미지 보여주기 : st.image
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption = "업로드한 이미지", width = "stretch")
#5) 분류 실행하기 : st.button / st.spinner
    if st.button("분류 실행"):
        with st.spinner("분류중..."):
            response = classify_image(prompt, img, model = model)
#6) 결과 출력하기 : st.write / st.code
        st.subheader("분류 결과 : ")
        st.code(response) # st.write or st.code