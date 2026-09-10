import streamlit as st
import pandas as pd
import datetime
import io
import json
import re

# ==================================================================
# 페이지 설정
# ==================================================================
st.set_page_config(page_title="운명사주 아우라 대시보드", layout="wide", page_icon="🔮")

# ==================================================================
# 프리미엄 디자인 (폰트 / 배경 / 색상 시스템)
# ==================================================================
st.markdown(
    '<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />',
    unsafe_allow_html=True
)

_RAW_CSS = '''
html, body, [class*="css"]  {
    font-family: 'Pretendard', -apple-system, 'Apple SD Gothic Neo', sans-serif !important;
}

.stApp {
    background-color: #faf8f4;
    background-image:
        repeating-linear-gradient(135deg, rgba(184,146,63,0.045) 0px, rgba(184,146,63,0.045) 1px, transparent 1px, transparent 26px),
        linear-gradient(180deg, #fbf9f5 0%, #f7f4ee 100%);
    color: #1a1a1a;
}

.main-title {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(100deg, #8a6a1f 0%, #1f2a44 65%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 2px;
}
.sub-title {
    font-size: 1.05rem;
    color: #6b6558;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.gold-divider {
    height: 2px;
    background: linear-gradient(90deg, #b8923f 0%, rgba(184,146,63,0.05) 100%);
    border: none;
    margin: 22px 0 26px 0;
}

h2, h3 { color: #1f2a44 !important; font-weight: 800 !important; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14182a 0%, #1c2138 100%);
}
section[data-testid="stSidebar"] * {
    color: #ecebe6 !important;
}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color: #e0b866 !important;
}
section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select {
    background-color: #232842 !important;
    color: #f4eedd !important;
    border: 1px solid #3a3f5c !important;
}
section[data-testid="stSidebar"] [data-testid="stDateInput"] input,
section[data-testid="stSidebar"] [data-testid="stDateInput"] div[data-baseweb="input"],
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #232842 !important;
    color: #f4eedd !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #b8923f 0%, #e0b866 100%) !important;
    color: #14182a !important;
    font-weight: 800 !important;
    border: none !important;
}
section[data-testid="stSidebar"] hr { border-color: #3a3f5c !important; }

.kpi-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 22px 18px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(20,24,42,0.06);
    border-left: 6px solid #cccccc;
}
.kpi-blue   { border-left-color: #2563eb; }
.kpi-green  { border-left-color: #059669; }
.kpi-red    { border-left-color: #dc2626; }
.kpi-gold   { border-left-color: #b8923f; }
.kpi-purple { border-left-color: #7c3aed; }
.kpi-num { font-size: 50px; font-weight: 800; color: #14182a; line-height: 1.1; }
.kpi-label { font-size: 22px; color: #8a8578; margin-top: 8px; font-weight: 700; }

.channel-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 18px 8px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(20,24,42,0.05);
    border-top: 5px solid #cccccc;
}
.ch-1 { border-top-color: #2563eb; }
.ch-2 { border-top-color: #059669; }
.ch-3 { border-top-color: #d97706; }
.ch-4 { border-top-color: #db2777; }
.ch-5 { border-top-color: #7c3aed; }
.ch-6 { border-top-color: #0d9488; }
.ch-7 { border-top-color: #64748b; }
.ch-num { font-size: 40px; font-weight: 800; color: #14182a; line-height: 1.1; }
.ch-label { font-size: 22px; color: #8a8578; margin-top: 6px; font-weight: 700; }

.badge-paid { background:#e6f7ec; color:#1a7f37; padding:3px 10px; border-radius:12px; font-size:12.5px; font-weight:700; }
.badge-wait { background:#fff3e0; color:#b45309; padding:3px 10px; border-radius:12px; font-size:12.5px; font-weight:700; }
.badge-sent { background:#e8f0fe; color:#1a56db; padding:3px 10px; border-radius:12px; font-size:12.5px; font-weight:700; }

div.stButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab-list"] { gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background-color: #f0ece2;
    border-radius: 10px 10px 0 0;
    padding: 10px 18px;
    font-weight: 700;
    color: #6b6558;
}
.stTabs [aria-selected="true"] {
    background-color: #ffffff !important;
    color: #b8923f !important;
    border-bottom: 3px solid #b8923f !important;
}

.month-star-banner {
    background: linear-gradient(100deg, #b8923f 0%, #e0b866 50%, #b8923f 100%);
    color: #14182a;
    font-size: 24px;
    font-weight: 800;
    text-align: center;
    padding: 20px;
    border-radius: 14px;
    margin: 10px 0 20px 0;
    box-shadow: 0 6px 20px rgba(184,146,63,0.35);
}
'''

_CSS_FLAT = " ".join(line.strip() for line in _RAW_CSS.strip().splitlines())
st.markdown(f"<style>{_CSS_FLAT}</style>", unsafe_allow_html=True)

# ==================================================================
# 로그인 게이트
# ==================================================================
def get_registered_users():
    """
    Streamlit Cloud의 Secrets(App settings > Secrets)에 아래 형식으로 등록하세요:

    [users]
    admin = "여기에_원하는_비밀번호"
    manager1 = "매니저1의_비밀번호"

    ⚠️ 이 파일(app.py)에는 절대 실제 비밀번호를 적지 마세요. 저장소가 Public이라 누구나 볼 수 있습니다.
    """
    try:
        users = dict(st.secrets["users"])
        if users:
            return users
    except Exception:
        pass
    return {"admin": "changeme1234"}

def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        return True

    st.markdown('<div class="main-title" style="text-align:center;">🔮 운명사주 아우라</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title" style="text-align:center;">관리자 로그인이 필요합니다</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        with st.form("login_form"):
            username = st.text_input("아이디")
            password = st.text_input("비밀번호", type="password")
            submitted = st.form_submit_button("🔐 로그인", use_container_width=True, type="primary")
            if submitted:
                users = get_registered_users()
                if username in users and password == users[username]:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
    return False

if not check_login():
    st.stop()

# ==================================================================
# 상수
# ==================================================================
CHANNELS = ["스레드", "크몽·숨고", "인스타", "페북", "릴스·틱톡·쇼츠", "당근·카카오", "기타"]
PAYMENT_OPTIONS = ["무료이벤트", "19,900원", "29,900원", "39,900원"]
COMMISSION_PER_SALE = 10000       # 매니저 건당 수당
WITHHOLDING_TAX_RATE = 0.033      # 3.3% 원천징수

# ==================================================================
# 세션 상태 초기화
# ==================================================================
if 'customer_list' not in st.session_state:
    st.session_state.customer_list = []
if 'manager_list' not in st.session_state:
    st.session_state.manager_list = []

# ==================================================================
# 헬퍼 함수
# ==================================================================
def parse_amount(payment_str):
    if not payment_str:
        return 0
    digits = re.sub(r'[^\d]', '', str(payment_str))
    return int(digits) if digits else 0

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def manager_id_options():
    ids = [m['매니저ID'] for m in st.session_state.manager_list]
    return ["직접유입(매니저없음)"] + ids

def compute_manager_performance() -> pd.DataFrame:
    """홍보매니저 실적 (순위용 원본 데이터)"""
    df_cust = pd.DataFrame(st.session_state.customer_list)
    rows = []
    for mgr in st.session_state.manager_list:
        mid = mgr['매니저ID']
        if not df_cust.empty and '매니저ID' in df_cust.columns:
            mine = df_cust[df_cust['매니저ID'] == mid]
        else:
            mine = pd.DataFrame()
        form_count = len(mine)
        paid_count = 0
        total_amt = 0
        if not mine.empty and '결제상태' in mine.columns:
            paid_df = mine[mine['결제상태'] == '결제완료']
            paid_count = len(paid_df)
            if not paid_df.empty:
                total_amt = int(paid_df['결제금액'].apply(parse_amount).sum())
        inflow = int(mgr.get('총유입수', 0) or 0)
        rows.append({
            "선택": False,
            "매니저ID": mid,
            "이름": mgr.get('이름', ''),
            "총 유입수": inflow,
            "양식 작성수": form_count,
            "결제 완료건수": paid_count,
            "총 결제금액(누적)": total_amt,
        })
    return pd.DataFrame(rows)

def compute_manager_payout() -> pd.DataFrame:
    """매니저 실적 및 지급현황 (건당 수당 - 3.3% 공제)"""
    df_cust = pd.DataFrame(st.session_state.customer_list)
    rows = []
    for mgr in st.session_state.manager_list:
        mid = mgr['매니저ID']
        if not df_cust.empty and '매니저ID' in df_cust.columns:
            mine = df_cust[df_cust['매니저ID'] == mid]
        else:
            mine = pd.DataFrame()
        recv_count = len(mine)
        paid_count = 0
        if not mine.empty and '결제상태' in mine.columns:
            paid_count = len(mine[mine['결제상태'] == '결제완료'])
        settle_amt = paid_count * COMMISSION_PER_SALE
        net_pay = int(round(settle_amt * (1 - WITHHOLDING_TAX_RATE)))
        rows.append({
            "매니저ID": mid,
            "이름": mgr.get('이름', ''),
            "실시간 접수건수": recv_count,
            "누적 정산금액": settle_amt,
            "지급급여": net_pay,
        })
    return pd.DataFrame(rows)

def next_tuesday(from_date=None):
    d = from_date or datetime.date.today()
    days_ahead = (1 - d.weekday()) % 7  # 화요일 weekday()==1
    return d + datetime.timedelta(days=days_ahead)

def get_prev_month_range(today=None):
    today = today or datetime.date.today()
    first_this_month = today.replace(day=1)
    last_prev_month = first_this_month - datetime.timedelta(days=1)
    first_prev_month = last_prev_month.replace(day=1)
    return first_prev_month, last_prev_month

def compute_month_top_manager():
    """전월(1일~말일) 결제완료 매출 1위 매니저"""
    df_cust = pd.DataFrame(st.session_state.customer_list)
    if df_cust.empty or '매니저ID' not in df_cust.columns or '접수날짜' not in df_cust.columns or '결제상태' not in df_cust.columns:
        return None
    df_cust = df_cust.copy()
    df_cust['_dt'] = pd.to_datetime(df_cust['접수날짜'], format="%Y-%m-%d %H:%M", errors='coerce')
    df_cust = df_cust.dropna(subset=['_dt'])
    if df_cust.empty:
        return None
    start, end = get_prev_month_range()
    mask = (df_cust['_dt'].dt.date >= start) & (df_cust['_dt'].dt.date <= end) & (df_cust['결제상태'] == '결제완료')
    filtered = df_cust[mask]
    if filtered.empty:
        return None
    filtered = filtered.copy()
    filtered['_amt'] = filtered['결제금액'].apply(parse_amount)
    grouped = filtered.groupby('매니저ID')['_amt'].sum().sort_values(ascending=False)
    if grouped.empty or grouped.iloc[0] <= 0:
        return None
    top_id = grouped.index[0]
    top_amt = int(grouped.iloc[0])
    name_map = {m['매니저ID']: m['이름'] for m in st.session_state.manager_list}
    return {"id": top_id, "name": name_map.get(top_id, top_id), "amount": top_amt}

# ==================================================================
# 헤더
# ==================================================================
st.markdown('<div class="main-title">🔮 운명사주 아우라 (AURA)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">사주분석 통합 관리 대시보드 · PREMIUM EDITION</div>', unsafe_allow_html=True)
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ==================================================================
# 사이드바: 고객 등록
# ==================================================================
with st.sidebar:
    st.markdown(f"👤 **{st.session_state.username}** 님으로 로그인됨")
    if st.button("🚪 로그아웃", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    st.markdown("---")
    st.header("📋 사주분석 신청 등록")
    st.caption("접수시간은 등록 버튼을 누르는 순간 자동으로 기록됩니다.")

    st.subheader("홍보 유입경로")
    channel = st.selectbox("유입경로 선택", CHANNELS)
    manager_id = st.selectbox("유입 홍보매니저 선택", manager_id_options())

    name_input = st.text_input("이름")
    gender = st.selectbox("성별확인", ["여성", "남성"])
    calendar = st.selectbox("양력/음력", ["양력", "음력"])

    birth_date = st.date_input(
        "생년월일",
        value=datetime.date(1995, 1, 1),
        min_value=datetime.date(1930, 1, 1),
        max_value=datetime.date.today()
    )

    raw_birth_time = st.text_input("태어난 시간 (예: 17:30)")
    if raw_birth_time.isdigit() and len(raw_birth_time) <= 2:
        birth_time = f"{int(raw_birth_time):02d}:00"
    elif ":" not in raw_birth_time and len(raw_birth_time) == 4 and raw_birth_time.isdigit():
        birth_time = f"{raw_birth_time[:2]}:{raw_birth_time[2:]}"
    else:
        birth_time = raw_birth_time if raw_birth_time else "12:00"

    time_unknown = st.checkbox("시간 모름")
    email = st.text_input("사주분석발송 본인 이메일주소")
    phone = st.text_input("휴대폰 번호", value="010-")

    payment_choice = st.selectbox("결제금액 선택", PAYMENT_OPTIONS)
    payment_status = st.selectbox("결제상태", ["결제대기", "결제완료", "환불"])

    if st.button("📋 신청고객 직접등록하기", use_container_width=True):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if payment_choice == "무료이벤트":
            payment = "0원"
            free_flag = "예"
        else:
            payment = payment_choice
            free_flag = "아니오"

        new_customer = {
            "선택": False,
            "접수날짜": now_str,
            "신청유입경로": channel,
            "매니저ID": manager_id,
            "이름": name_input if name_input else "이름없음",
            "성별": gender,
            "양력/음력": calendar,
            "생년월일": str(birth_date),
            "생시": "모름" if time_unknown else birth_time,
            "이메일": email,
            "휴대폰": phone,
            "결제금액": payment,
            "결제상태": payment_status,
            "무료이벤트": free_flag,
            "발송상태": "미발송",
            "이메일발송상태": "미발송",
            "문자발송상태": "미발송",
        }
        st.session_state.customer_list.append(new_customer)
        st.success(f"'{new_customer['이름']}' 고객이 등록되었습니다! (접수시각: {now_str})")

    st.markdown("---")
    st.caption("💾 데이터가 사라지는 게 걱정되면 '데이터 백업' 탭에서 주기적으로 백업해두세요.")

# ==================================================================
# 탭 구성
# ==================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 전체 현황", "👥 고객 리스트", "🧑‍💼 홍보매니저 실적", "⚙️ 홍보매니저 관리", "💾 데이터 백업"
])

df_current = pd.DataFrame(st.session_state.customer_list) if st.session_state.customer_list else pd.DataFrame()
total_count = len(df_current)

# ------------------------------------------------------------------
# TAB 1. 전체 현황
# ------------------------------------------------------------------
with tab1:
    st.header("홍보 유입경로별 접수 현황")

    def channel_count(name):
        if total_count == 0:
            return 0
        return len(df_current[df_current['신청유입경로'] == name])

    row1 = st.columns(4)
    row2 = st.columns(3)
    channel_meta = [
        (row1[0], "스레드", "ch-1"),
        (row1[1], "크몽·숨고", "ch-2"),
        (row1[2], "인스타", "ch-3"),
        (row1[3], "페북", "ch-4"),
        (row2[0], "릴스·틱톡·쇼츠", "ch-5"),
        (row2[1], "당근·카카오", "ch-6"),
        (row2[2], "기타", "ch-7"),
    ]
    for col, label, cls in channel_meta:
        with col:
            st.markdown(
                f'<div class="channel-card {cls}"><div class="ch-num">{channel_count(label)}건</div>'
                f'<div class="ch-label">{label}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.subheader("📈 핵심 지표")

    if total_count > 0 and '결제금액' in df_current.columns:
        df_current['_금액'] = df_current['결제금액'].apply(parse_amount)
        if '결제상태' in df_current.columns:
            paid_df = df_current[df_current['결제상태'] == '결제완료']
            refund_df = df_current[df_current['결제상태'] == '환불']
            total_revenue_paid = paid_df['_금액'].sum()
            paid_cnt = len(paid_df)
            refund_cnt = len(refund_df)
        else:
            total_revenue_paid = df_current['_금액'].sum()
            paid_cnt = total_count
            refund_cnt = 0
    else:
        total_revenue_paid = 0
        paid_cnt = 0
        refund_cnt = 0

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f'<div class="kpi-card kpi-blue"><div class="kpi-num">{total_count}명</div><div class="kpi-label">총 신청 고객 수</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card kpi-green"><div class="kpi-num">{paid_cnt}건</div><div class="kpi-label">결제완료 건수</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card kpi-red"><div class="kpi-num">{refund_cnt}건</div><div class="kpi-label">환불건수</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi-card kpi-gold"><div class="kpi-num">{total_revenue_paid:,}원</div><div class="kpi-label">결제완료 총 매출액</div></div>', unsafe_allow_html=True)
    with k5:
        conv = (paid_cnt / total_count * 100) if total_count > 0 else 0
        st.markdown(f'<div class="kpi-card kpi-purple"><div class="kpi-num">{conv:.1f}%</div><div class="kpi-label">전체 결제 전환율</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    if total_count > 0:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("채널별 유입 현황")
            channel_counts = df_current['신청유입경로'].value_counts()
            st.bar_chart(channel_counts)
        with c2:
            st.subheader("홍보매니저별 실적 비교")
            perf_df = compute_manager_performance()
            if not perf_df.empty:
                st.bar_chart(perf_df.set_index('이름')['결제 완료건수'])
            else:
                st.info("등록된 홍보매니저가 없습니다. '홍보매니저 관리' 탭에서 추가해주세요.")
    else:
        st.info("아직 등록된 신청 고객이 없습니다.")

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    if st.button("🔄 새로고침"):
        st.rerun()

# ------------------------------------------------------------------
# TAB 2. 고객 리스트
# ------------------------------------------------------------------
with tab2:
    st.header("사주분석 신청고객 리스트")
    st.caption("⚠️ 이 리스트는 이 대시보드에서 직접 등록하거나 불러온 고객만 표시됩니다. 별도의 랜딩페이지와 실시간으로 연동하려면 공용 데이터베이스/API 연결이 추가로 필요합니다.")

    st.markdown("##### 🔍 검색 및 검색 옵션")
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        search_keyword = st.text_input("이름, 이메일, 휴대폰번호 검색", placeholder="검색어 입력")
    with s_col2:
        search_status = st.selectbox("발송상태 선택", ["전체", "미발송", "발송완료"])
    with s_col3:
        search_payment = st.selectbox("결제상태 선택", ["전체", "결제대기", "결제완료", "환불"])
    with s_col4:
        search_date = st.text_input("날짜 검색 (예: 2026-09)", placeholder="날짜 입력")

    if len(st.session_state.customer_list) > 0:
        df_editable = pd.DataFrame(st.session_state.customer_list)

        for col, default in [("이메일발송상태", "미발송"), ("문자발송상태", "미발송")]:
            if col not in df_editable.columns:
                df_editable[col] = default

        if search_keyword:
            df_editable = df_editable[
                df_editable['이름'].str.contains(search_keyword, na=False) |
                df_editable['이메일'].str.contains(search_keyword, na=False) |
                df_editable['휴대폰'].str.contains(search_keyword, na=False)
            ]
        if search_status != "전체":
            df_editable = df_editable[df_editable['발송상태'] == search_status]
        if search_payment != "전체" and '결제상태' in df_editable.columns:
            df_editable = df_editable[df_editable['결제상태'] == search_payment]
        if search_date:
            df_editable = df_editable[df_editable['접수날짜'].str.contains(search_date, na=False)]

        sel1, sel2 = st.columns(2)
        with sel1:
            if st.button("☑️ 현재 목록 전체 선택", use_container_width=True):
                for idx in df_editable.index:
                    st.session_state.customer_list[idx]["선택"] = True
                st.rerun()
        with sel2:
            if st.button("⬜ 현재 목록 전체 해제", use_container_width=True):
                for idx in df_editable.index:
                    st.session_state.customer_list[idx]["선택"] = False
                st.rerun()

        editable_cols = ["선택", "결제상태", "발송상태", "이메일발송상태", "문자발송상태"]
        edited_df = st.data_editor(
            df_editable,
            column_config={
                "선택": st.column_config.CheckboxColumn("선택", help="처리할 고객을 체크하세요", default=False),
                "결제상태": st.column_config.SelectboxColumn("결제상태", options=["결제대기", "결제완료", "환불"]),
                "발송상태": st.column_config.SelectboxColumn("PDF발송", options=["미발송", "발송완료"]),
                "이메일발송상태": st.column_config.SelectboxColumn("이메일발송", options=["미발송", "발송완료"]),
                "문자발송상태": st.column_config.SelectboxColumn("문자발송", options=["미발송", "발송완료"]),
            },
            disabled=[c for c in df_editable.columns if c not in editable_cols],
            use_container_width=True,
            key="customer_data_editor"
        )

        for idx, row in edited_df.iterrows():
            orig_idx = row.name
            for col in editable_cols:
                st.session_state.customer_list[orig_idx][col] = row[col]

        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("📧 이메일 발송완료 처리", use_container_width=True):
                selected = [c for c in st.session_state.customer_list if c.get("선택") == True]
                if selected:
                    for c in st.session_state.customer_list:
                        if c.get("선택"):
                            c["이메일발송상태"] = "발송완료"
                    st.success(f"{len(selected)}명 이메일 발송완료로 처리되었습니다!")
                    st.rerun()
                else:
                    st.warning("고객을 하나 이상 선택해 주세요.")
        with b2:
            if st.button("💬 문자 발송완료 처리", use_container_width=True):
                selected = [c for c in st.session_state.customer_list if c.get("선택") == True]
                if selected:
                    for c in st.session_state.customer_list:
                        if c.get("선택"):
                            c["문자발송상태"] = "발송완료"
                    st.success(f"{len(selected)}명 문자 발송완료로 처리되었습니다!")
                    st.rerun()
                else:
                    st.warning("고객을 하나 이상 선택해 주세요.")
        with b3:
            if st.button("🪄 사주분석 직접생성", use_container_width=True, type="primary"):
                selected = [c for c in st.session_state.customer_list if c.get("선택") == True]
                if selected:
                    names = ", ".join([c["이름"] for c in selected])
                    st.success(f"{len(selected)}명 ({names})의 사주분석 PDF가 생성·발송 처리되었습니다!")
                    for c in st.session_state.customer_list:
                        if c.get("선택"):
                            c["발송상태"] = "발송완료"
                    st.rerun()
                else:
                    st.warning("고객을 하나 이상 선택해 주세요.")

        st.caption(
            "ℹ️ 위 3개 버튼은 '처리 상태 기록'만 해줍니다. 실제로 이메일/문자/PDF를 자동 생성·발송하려면 "
            "이메일(SMTP 등), 문자 API(예: 알리고), PDF 생성 엔진 연동이 추가로 필요해요."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        excel_data = to_excel_bytes(df_editable.drop(columns=["선택"], errors="ignore"))
        st.download_button(
            "📥 현재 목록 엑셀로 다운로드",
            data=excel_data,
            file_name=f"고객리스트_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.info("아직 등록된 신청 고객이 없습니다. 왼쪽 사이드바에서 등록해주세요.")

# ------------------------------------------------------------------
# TAB 3. 홍보매니저 실적
# ------------------------------------------------------------------
with tab3:
    st.header("🧑‍💼 홍보매니저 실적 대시보드")
    st.caption("체크박스 / 순위 / 매니저ID / 이름 / 총 유입수 / 양식 작성수 / 결제 완료건수 / 총 결제금액(누적)")

    top_mgr = compute_month_top_manager()
    if top_mgr:
        st.markdown(
            f'<div class="month-star-banner">🌟 이달의 운명매니저 &nbsp; <b>{top_mgr["name"]}</b> &nbsp; ({top_mgr["amount"]:,}원)</div>',
            unsafe_allow_html=True
        )
    else:
        st.info("전월(1일~말일) 결제완료 실적 기준으로 선정됩니다. 아직 집계된 실적이 없습니다.")
    st.caption("⏱️ 매달 1일 00시 기준 자동 산정 · 전월 1일~말일 결제 매출 1위 매니저")

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    perf_df = compute_manager_performance()

    if perf_df.empty:
        st.info("등록된 홍보매니저가 없습니다. '⚙️ 홍보매니저 관리' 탭에서 먼저 등록해주세요.")
    else:
        display_df = perf_df.sort_values("총 결제금액(누적)", ascending=False).reset_index(drop=True)
        display_df.insert(1, "순위", display_df.index + 1)
        display_df["총 결제금액(누적)"] = display_df["총 결제금액(누적)"].apply(lambda v: f"{v:,}원")

        edited_perf = st.data_editor(
            display_df,
            column_config={"선택": st.column_config.CheckboxColumn("선택", default=False)},
            disabled=[c for c in display_df.columns if c != "선택"],
            use_container_width=True,
            key="manager_perf_editor",
            hide_index=True,
        )

        p1, p2 = st.columns(2)
        with p1:
            selected_ids = edited_perf[edited_perf["선택"] == True]["매니저ID"].tolist()
            export_df = perf_df[perf_df["매니저ID"].isin(selected_ids)] if selected_ids else perf_df
            excel_perf = to_excel_bytes(export_df.drop(columns=["선택"], errors="ignore"))
            st.download_button(
                "📥 실적 엑셀로 다운로드 (선택 시 선택분만)",
                data=excel_perf,
                file_name=f"홍보매니저실적_{datetime.date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        with p2:
            st.bar_chart(perf_df.set_index("이름")["총 결제금액(누적)"])

# ------------------------------------------------------------------
# TAB 4. 홍보매니저 관리
# ------------------------------------------------------------------
with tab4:
    st.header("⚙️ 홍보매니저 관리")

    with st.form("add_manager_form", clear_on_submit=True):
        st.subheader("신규 홍보매니저 등록")
        f1, f2, f3 = st.columns(3)
        with f1:
            new_id = st.text_input("매니저ID (예: manager01)")
            new_name = st.text_input("이름")
        with f2:
            new_phone = st.text_input("연락처", placeholder="010-0000-0000")
            new_address = st.text_input("주소")
        with f3:
            new_account = st.text_input("계좌번호", placeholder="은행명 000-000-000000")
            new_contract_date = st.date_input("계약작성일", value=datetime.date.today())

        submitted = st.form_submit_button("➕ 홍보매니저 등록", use_container_width=True, type="primary")
        if submitted:
            if not new_id or not new_name:
                st.warning("매니저ID와 이름은 필수입니다.")
            elif any(m['매니저ID'] == new_id for m in st.session_state.manager_list):
                st.warning("이미 존재하는 매니저ID입니다.")
            else:
                st.session_state.manager_list.append({
                    "매니저ID": new_id,
                    "이름": new_name,
                    "연락처": new_phone,
                    "주소": new_address,
                    "계좌번호": new_account,
                    "계약작성일": str(new_contract_date),
                    "총유입수": 0,
                    "등록일": str(datetime.date.today()),
                })
                st.success(f"홍보매니저 '{new_name}'({new_id})이(가) 등록되었습니다!")

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.subheader("등록된 홍보매니저 목록")

    if st.session_state.manager_list:
        manager_df = pd.DataFrame(st.session_state.manager_list)
        edited_manager = st.data_editor(
            manager_df,
            column_config={
                "총유입수": st.column_config.NumberColumn(
                    "총유입수(수동보정)", min_value=0, step=10,
                    help="실제 링크 클릭수 등 외부 트래픽 데이터가 있다면 직접 입력해 조정할 수 있습니다."
                ),
            },
            disabled=["매니저ID", "이름", "연락처", "주소", "계좌번호", "계약작성일", "등록일"],
            use_container_width=True,
            key="manager_manage_editor",
            hide_index=True,
        )
        st.session_state.manager_list = edited_manager.to_dict("records")

        del_col1, del_col2 = st.columns([3, 1])
        with del_col2:
            del_target = st.selectbox("삭제할 매니저ID", ["선택안함"] + [m['매니저ID'] for m in st.session_state.manager_list])
            if st.button("🗑️ 홍보매니저 삭제", use_container_width=True):
                if del_target != "선택안함":
                    st.session_state.manager_list = [m for m in st.session_state.manager_list if m['매니저ID'] != del_target]
                    st.success(f"'{del_target}'가 삭제되었습니다.")
                    st.rerun()
    else:
        st.info("등록된 홍보매니저가 없습니다. 위 양식으로 첫 홍보매니저를 등록해보세요.")

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.subheader("💰 매니저 실적 및 지급현황")

    nt = next_tuesday()
    weekday_kr = ['월', '화', '수', '목', '금', '토', '일'][nt.weekday()]
    st.caption(
        f"매주 화요일 자동 정산 · 다음 정산일: {nt.strftime('%Y-%m-%d')} ({weekday_kr}요일) · "
        f"건당 수당 {COMMISSION_PER_SALE:,}원 → 3.3% 원천징수 공제 후 지급"
    )

    payout_df = compute_manager_payout()
    if payout_df.empty:
        st.info("등록된 홍보매니저가 없습니다.")
    else:
        display_payout = payout_df.copy()
        display_payout["누적 정산금액"] = display_payout["누적 정산금액"].apply(lambda v: f"{v:,}원")
        display_payout["지급급여"] = display_payout["지급급여"].apply(lambda v: f"{v:,}원")
        st.dataframe(display_payout, use_container_width=True, hide_index=True)

        excel_payout = to_excel_bytes(payout_df)
        st.download_button(
            "📥 지급현황 엑셀로 다운로드",
            data=excel_payout,
            file_name=f"매니저지급현황_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# ------------------------------------------------------------------
# TAB 5. 데이터 백업
# ------------------------------------------------------------------
with tab5:
    st.header("💾 데이터 백업 및 복원")
    st.caption("Streamlit 앱은 새로고침·재배포 시 데이터가 초기화될 수 있습니다. 작업 후 주기적으로 백업해두는 것을 권장합니다.")

    backup_data = {
        "customer_list": st.session_state.customer_list,
        "manager_list": st.session_state.manager_list,
        "backup_date": str(datetime.datetime.now()),
    }
    backup_json = json.dumps(backup_data, ensure_ascii=False, indent=2)

    st.download_button(
        "📥 전체 데이터 백업 다운로드 (JSON)",
        data=backup_json,
        file_name=f"aura_backup_{datetime.date.today()}.json",
        mime="application/json",
        use_container_width=True
    )

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.subheader("백업 파일로 복원하기")
    uploaded = st.file_uploader("백업했던 JSON 파일을 업로드하세요", type=["json"])
    if uploaded is not None:
        try:
            loaded = json.load(uploaded)
            if st.button("⚠️ 이 파일로 현재 데이터를 덮어쓰기", use_container_width=True):
                st.session_state.customer_list = loaded.get("customer_list", [])
                st.session_state.manager_list = loaded.get("manager_list", loaded.get("staff_list", []))
                st.success("데이터가 복원되었습니다!")
                st.rerun()
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
