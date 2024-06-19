import streamlit as st
import pandas as pd
from pykrx import stock
from datetime import datetime, timedelta

# Streamlit 앱 제목
st.title("재무정보 상위 종목")

# 오늘 날짜를 기준으로 데이터 가져오기
today = datetime.today().strftime('%Y%m%d')

# 모든 종목의 재무 정보를 가져오기
try:
    financial_df = stock.get_market_fundamental_by_ticker(date=today, market="KOSPI")
    financial_df.reset_index(inplace=True)
    financial_df['종목명'] = financial_df['티커'].apply(lambda x: stock.get_market_ticker_name(x))
except Exception as e:
    st.error(f"재무 정보를 가져오는 중 오류가 발생했습니다: {e}")

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
    common_stocks = set(top_per['종목명']).intersection(set(top_pbr['종목명'])).intersection(set(top_eps['종목명']))
    common_df = financial_df[financial_df['종목명'].isin(common_stocks)]
    common_df = move_stock_name_to_front(common_df)
    st.dataframe(common_df)


st.title("종목별 세부사항 조회")

# 사용자로부터 티커 입력 받기
ticker = st.text_input("티커를 입력하세요 (예: 005930)", value="005930")

# 사용자로부터 날짜 범위 입력 받기
start_date = st.date_input("시작 날짜", value=datetime.today() - timedelta(days=30))
end_date = st.date_input("종료 날짜", value=datetime.today())

# 날짜 형식 변환
start_date = start_date.strftime('%Y%m%d')
end_date = end_date.strftime('%Y%m%d')

try:
    ohlcv_df = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)
    ohlcv_df.reset_index(inplace=True)
    ohlcv_df['날짜'] = pd.to_datetime(ohlcv_df['날짜'])
except Exception as e:
    st.error(f"OHLCV 데이터를 가져오는 중 오류가 발생했습니다: {e}")

try:
    finance_df = stock.get_market_fundamental_by_date(start_date, end_date, ticker)
    finance_df.reset_index(inplace=True)
    finance_df['날짜'] = pd.to_datetime(finance_df['날짜'])
except Exception as e:
    st.error(f"DIV/BPS/PER/EPS 데이터를 가져오는 중 오류가 발생했습니다: {e}")

try:
    trading_value_df = stock.get_market_trading_value_by_date(start_date, end_date, ticker)
    trading_value_df.reset_index(inplace=True)
    trading_value_df['날짜'] = pd.to_datetime(trading_value_df['날짜'])
except Exception as e:
    st.error(f"거래대금 데이터를 가져오는 중 오류가 발생했습니다: {e}")

try:
    trading_volume_df = stock.get_market_trading_volume_by_date(start_date, end_date, ticker)
    trading_volume_df.reset_index(inplace=True)
    trading_volume_df['날짜'] = pd.to_datetime(trading_volume_df['날짜'])
except Exception as e:
    st.error(f"거래량 데이터를 가져오는 중 오류가 발생했습니다: {e}")

tab5, tab6, tab7, tab8 = st.tabs(["OHLCV", "DIV/BPS/PER/EPS", "거래실적 추이 (거래대금)", "거래실적 추이 (거래량)"])

with tab5:
    st.subheader("기간 내 OHLCV")
    st.line_chart(ohlcv_df.set_index('날짜')[['시가', '고가', '저가', '종가', '거래량']])

with tab6:
    st.header("기간 내 DIV/BPS/PER/EPS")
    st.line_chart(finance_df.set_index('날짜')[['DIV', 'BPS', 'PER', 'EPS']])

with tab7:
    st.header("기간 내 거래실적 추이 (거래대금)")
    st.line_chart(trading_value_df.set_index('날짜')[['기관합계','기타법인','개인','외국인합계','전체']])

with tab8:
    st.header("기간 내 거래실적 추이 (거래량)")
    st.line_chart(trading_volume_df.set_index('날짜')[['기관합계','기타법인','개인','외국인합계','전체']])
