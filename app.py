import streamlit as st
from datetime import date
import os
import json
from PIL import Image

# 페이지 정보
st.set_page_config(
    page_title="KS_Library"
)

# 앱 제목 설정
st.title("Daily Photo Upload")

# 현재 날짜 표시
today = date.today()
st.write(f"Today's date: {today}")

# 파일 업로드
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
description = st.text_input("Enter a description for the image")

if uploaded_file is not None and description:
    # 디렉토리 생성
    upload_dir = os.path.join("uploaded_photos", str(today))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # 파일 저장
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 설명 저장
    desc_file_path = os.path.join(upload_dir, f"{uploaded_file.name}.json")
    with open(desc_file_path, "w") as f:
        json.dump({"description": description}, f)
    
    # 이미지 및 설명 표시
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    st.write("Image and description uploaded successfully!")
    st.write(f"Saved as: {file_path}")

# 갤러리 표시
st.write("## Gallery")
root_dir = "uploaded_photos"
for dirpath, dirnames, filenames in os.walk(root_dir):
    for dirname in sorted(dirnames):
        st.write(f"### {dirname}")
        dir_full_path = os.path.join(dirpath, dirname)
        images = sorted([f for f in os.listdir(dir_full_path) if not f.endswith('.json')])
        for image_name in images:
            image_path = os.path.join(dir_full_path, image_name)
            image = Image.open(image_path)

            # 설명 읽기
            desc_file_path = os.path.join(dir_full_path, f"{image_name}.json")
            if os.path.exists(desc_file_path):
                with open(desc_file_path, "r") as f:
                    description = json.load(f)["description"]
            else:
                description = "No description available."

            st.image(image, caption=description, use_column_width=True)

            # 컬럼을 사용하여 가운데 정렬
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                delete_button = st.button(f"Delete {image_name}", key=f"delete_button_{image_path}")
                if delete_button:
                    st.session_state[f"confirm_delete_{image_path}"] = True

            # 삭제 확인 절차
            if st.session_state.get(f"confirm_delete_{image_path}", False):
                st.warning(f"Are you sure you want to delete {image_name}?")
                confirm_button = st.button(f"Yes, delete {image_name}", key=f"confirm_button_{image_path}")
                cancel_button = st.button("Cancel", key=f"cancel_button_{image_path}")

                if confirm_button:
                    os.remove(image_path)
                    if os.path.exists(desc_file_path):
                        os.remove(desc_file_path)
                    del st.session_state[f"confirm_delete_{image_path}"]
                    st.experimental_rerun()

                if cancel_button:
                    del st.session_state[f"confirm_delete_{image_path}"]
