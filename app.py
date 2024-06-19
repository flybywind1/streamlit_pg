import streamlit as st
import pandas as pd
from pykrx import stock
from datetime import datetime

# Streamlit 앱 제목
st.title("재무정보 상위 종목")

# 오늘 날짜를 기준으로 데이터 가져오기
today = datetime.today().strftime('%Y%m%d')

# 모든 종목의 재무 정보를 가져오기
financial_df = stock.get_market_fundamental_by_ticker(date=today, market="KOSPI")

# 종목 코드를 인덱스에서 컬럼으로 변환
financial_df.reset_index(inplace=True)

# 종목 이름을 가져와서 추가하기
financial_df['종목명'] = financial_df['티커'].apply(lambda x: stock.get_market_ticker_name(x))

# 종목명을 첫 번째 열로 이동
def move_stock_name_to_front(df):
    cols = ['종목명'] + [col for col in df.columns if col != '종목명']
    return df[cols]

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["PER 상위 종목", "PBR 상위 종목", "EPS 상위 종목", "중복 종목"])

with tab1:
    st.header("PER 상위 종목")
    num_per = st.number_input("PER 상위 몇 개 종목을 보시겠습니까?", min_value=1, max_value=100, value=30, key="num_per")
    top_per = financial_df.sort_values(by='PER', ascending=False).head(num_per)
    top_per = move_stock_name_to_front(top_per)
    st.dataframe(top_per)

with tab2:
    st.header("PBR 상위 종목")
    num_pbr = st.number_input("PBR 상위 몇 개 종목을 보시겠습니까?", min_value=1, max_value=100, value=30, key="num_pbr")
    top_pbr = financial_df.sort_values(by='PBR', ascending=False).head(num_pbr)
    top_pbr = move_stock_name_to_front(top_pbr)
    st.dataframe(top_pbr)

with tab3:
    st.header("EPS 상위 종목")
    num_eps = st.number_input("EPS 상위 몇 개 종목을 보시겠습니까?", min_value=1, max_value=100, value=30, key="num_eps")
    top_eps = financial_df.sort_values(by='EPS', ascending=False).head(num_eps)
    top_eps = move_stock_name_to_front(top_eps)
    st.dataframe(top_eps)

with tab4:
    st.header("중복 종목")
    # 중복 항목 찾기
    common_stocks = set(top_per['종목명']).intersection(set(top_pbr['종목명'])).intersection(set(top_eps['종목명']))
    
    # 중복 종목 데이터프레임 생성
    common_df = financial_df[financial_df['종목명'].isin(common_stocks)]
    common_df = move_stock_name_to_front(common_df)
    
    st.dataframe(common_df)
