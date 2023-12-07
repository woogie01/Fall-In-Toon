import pickle
import streamlit as st
import webbrowser


def get_recommendations(webtoon_title):
    # 웹툰 제목을 통해서 전체 데이터 기준 그 영화의 인덱스 값을 얻기.
    # 인덱스 값이 하나만 있어도 배열로 전환 : [0] 처리
    idx = webtoons[webtoons["title"] == webtoon_title].index[0]

    # 코사인 유사도 Matrix idx 데이터를 (idx, cosine_sim) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 코사인 유사도 기준 내림차순 정렬
    # 람다식 활용 - 리스트의 2번째 정보 추출
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 자기 자신을 제외한 20개의 추천 웹툰 가져오기
    sim_scores = sim_scores[1:21]

    # 추천 웹툰 목록 20개의 인덱스 정보를 추출
    webtoon_indices = [i[0] for i in sim_scores]

    # 인덱스 정보를 통해 영화 이미지, 제목 추출
    images = []
    titles = []
    page_url = []
    for i in webtoon_indices:
        webtoon_title = webtoons["title"].iloc[i]
        image_path = webtoons["thumbnail_url"].iloc[i]
        webtoon_url = webtoons["webtoon_url"].iloc[i]

        images.append(image_path)
        titles.append(webtoon_title)
        page_url.append(webtoon_url)

    return images, titles, page_url


# 이미지 클릭 시 해당 웹툰 사이트로 이동하는 함수
def open_webtoon_site(url):
    webbrowser.open(url)


webtoons = pickle.load(open("modeling/webtoon.pickle", "rb"))
cosine_sim = pickle.load(open("modeling/cosine_sim_pickle", "rb"))

st.set_page_config(layout="wide")
st.header("Introduction to Naver Webtoon")

webtoon_list = webtoons["title"].values
title = st.selectbox("Choose The Webtoon You Saw", webtoon_list)

if st.button("Recommend"):
    with st.spinner("Please Wait..."):
        images, titles, urls = get_recommendations(title)

        idx = 0
        for i in range(0, 4):
            cols = st.columns(5)
            for col in cols:
                # 이미지 클릭 시 해당 웹툰 사이트로 이동하는 링크 생성
                webtoon_url = urls[idx]
                markdown_link = f'<a href="{webtoon_url}"><img src="{images[idx]}" alt="{titles[idx]}" width="100%"></a>'
                col.markdown(markdown_link, unsafe_allow_html=True)
                idx += 1
