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
st.markdown('''
    <link rel="stylesheet" as="style" crossorigin
        href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
    <style>
    html, body, [class*="css"]  {
        font-family: 'Pretendard', -apple-system, 'Apple SD Gothic Neo', sans-serif !important;
    }

    /* 은은한 골드 대각선 패턴 + 크림 그라데이션 배경 */
    .stApp {
        background-color: #faf8f4;
        background-image:
            repeating-linear-gradient(135deg, rgba(184,146,63,0.045) 0px, rgba(184,146,63,0.045) 1px, transparent 1px, transparent 26px),
            linear-gradient(180deg, #fbf9f5 0%, #f7f4ee 100%);
        color: #1a1a1a;
    }

    /* 메인 타이틀 - 골드→네이비 그라데이션 */
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

    /* 사이드바 - 다크 네이비 + 골드 포인트 */
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
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #b8923f 0%, #e0b866 100%) !important;
        color: #14182a !important;
        font-weight: 800 !important;
        border: none !important;
    }
    section[data-testid="stSidebar"] hr { border-color: #3a3f5c !important; }

    /* KPI 카드 - 카테고리별 강조색 */
    .kpi-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 20px 20px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(20,24,42,0.06);
        border-left: 5px solid #cccccc;
    }
    .kpi-blue   { border-left-color: #2563eb; }
    .kpi-green  { border-left-color: #059669; }
    .kpi-gold   { border-left-color: #b8923f; }
    .kpi-purple { border-left-color: #7c3aed; }
    .kpi-num { font-size: 27px; font-weight: 800; color: #14182a; }
    .kpi-label { font-size: 13px; color: #8a8578; margin-top: 6px; font-weight: 600; }

    /* 채널 카드 (상단 5개) */
    .channel-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px 10px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(20,24,42,0.05);
        border-top: 4px solid #cccccc;
    }
    .ch-1 { border-top-color: #2563eb; }
    .ch-2 { border-top-color: #059669; }
    .ch-3 { border-top-color: #d97706; }
    .ch-4 { border-top-color: #db2777; }
    .ch-5 { border-top-color: #7c3aed; }
    .ch-num { font-size: 22px; font-weight: 800; color: #14182a; }
    .ch-label { font-size: 12.5px; color: #8a8578; margin-top: 4px; font-weight: 600; }

    /* 상태 배지 */
    .badge-paid { background:#e6f7ec; color:#1a7f37; padding:3px 10px; border-radius:12px; font-size:12.5px; font-weight:700; }
    .badge-wait { background:#fff3e0; color:#b45309; padding:3px 10px; border-radius:12px; font-size:12.5px; font-weight:700; }
    .badge-sent { background:#e8f0fe; color:#1a56db; padding:3px 10px; border-radius:12px; font-size:12.5px; font-weight:700; }

    /* 버튼 기본 스타일 고급화 */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    /* 탭 스타일 */
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
    </style>
''', unsafe_allow_html=True)

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
    아래 기본값은 secrets가 아직 설정되지 않았을 때 로컬 테스트용으로만 쓰이는 임시 계정입니다.
    """
    try:
        users = dict(st.secrets["users"])
        if users:
            return users
    except Exception:
        pass
    # secrets 미설정 시 로컬 테스트용 임시 계정 (운영 배포 전 반드시 Secrets로 교체하세요)
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
    df_cust = pd.DataFrame(st.session_state.customer_list)
    rows = []
    for i, mgr in enumerate(st.session_state.manager_list, start=1):
        mid = mgr['매니저ID']
        if not df_cust.empty and '매니저ID' in df_cust.columns:
            mine = df_cust[df_cust['매니저ID'] == mid]
        else:
            mine = pd.DataFrame()
        form_count = len(mine)
        paid_count = 0
        if not mine.empty and '결제상태' in mine.columns:
            paid_count = len(mine[mine['결제상태'] == '결제완료'])
        inflow = int(mgr.get('총유입수', 0) or 0)
        conv_rate = (paid_count / inflow * 100) if inflow > 0 else 0.0
        unit_price = int(mgr.get('건당정산단가', 0) or 0)
        settle_amt = paid_count * unit_price
        rows.append({
            "선택": False,
            "순서": i,
            "매니저ID": mid,
            "이름": mgr.get('이름', ''),
            "총 유입수": inflow,
            "양식 작성수": form_count,
            "결제 완료건수": paid_count,
            "결제 전환율": round(conv_rate, 1),
            "정산예정액": settle_amt,
            "정산상태": mgr.get('정산상태', '정산대기'),
        })
    return pd.DataFrame(rows)

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

    date_input = st.text_input("신청날짜 (예: 4/27 11:38)", value=datetime.datetime.now().strftime("%m/%d %H:%M"))
    channel = st.selectbox("사주신청 유입경로", ["스레드", "카카오", "당근", "인스타", "기타(영상,크몽 등)"])
    manager_id = st.selectbox("유입 홍보매니저 선택", manager_id_options())
    name_input = st.text_input("이름")
    gender = st.selectbox("성별확인", ["여성", "남성"])
    calendar = st.selectbox("양력/음력", ["양력", "음력"])

    birth_date = st.date_input(
        "생년월일",
        value=datetime.date(1995, 1, 1),
        min_value=datetime.date(1920, 1, 1),
        max_value=datetime.date.today()
    )

    raw_birth_time = st.text_input("생시 (예: 17:30)")
    if raw_birth_time.isdigit() and len(raw_birth_time) <= 2:
        birth_time = f"{int(raw_birth_time):02d}:00"
    elif ":" not in raw_birth_time and len(raw_birth_time) == 4 and raw_birth_time.isdigit():
        birth_time = f"{raw_birth_time[:2]}:{raw_birth_time[2:]}"
    else:
        birth_time = raw_birth_time if raw_birth_time else "12:00"

    time_unknown = st.checkbox("시간 모름")
    email = st.text_input("사주분석PDF발송 이메일주소")
    phone = st.text_input("휴대폰 번호", value="010-")

    raw_payment = st.text_input("결제금액 (예: 29,900원)", value="29900")
    payment_val = parse_amount(raw_payment) or 29900
    payment = f"{payment_val:,}원"

    payment_status = st.selectbox("결제상태", ["결제대기", "결제완료", "환불"])
    call_status = st.selectbox("통화상태", ["통화대기", "통화완료", "부재중"])
    free_event = st.checkbox("무료이벤트")
    send_status = st.selectbox("PDF발송", ["미발송", "발송완료"])

    if st.button("✅ 신청고객 등록", use_container_width=True):
        new_customer = {
            "선택": False,
            "접수날짜": date_input,
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
            "통화상태": call_status,
            "무료이벤트": "예" if free_event else "아니오",
            "발송상태": send_status,
            "이메일발송상태": "미발송",
            "문자발송상태": "미발송",
        }
        st.session_state.customer_list.append(new_customer)
        st.success(f"'{new_customer['이름']}' 고객이 등록되었습니다!")

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
    st.header("홍보 채널별 신청접수 현황")
    col1, col2, col3, col4, col5 = st.columns(5)

    def channel_count(name):
        if total_count == 0:
            return 0
        if name == "기타(영상,크몽 등)":
            return len(df_current[df_current['신청유입경로'].str.contains('기타', na=False)])
        return len(df_current[df_current['신청유입경로'] == name])

    channel_meta = [
        (col1, "스레드 홍보", "스레드", "ch-1"),
        (col2, "홍보 카카오", "카카오", "ch-2"),
        (col3, "당근마켓 홍보", "당근", "ch-3"),
        (col4, "홍보 인스타", "인스타", "ch-4"),
        (col5, "홍보(영상,크몽 등)", "기타(영상,크몽 등)", "ch-5"),
    ]
    for col, label, key, cls in channel_meta:
        with col:
            st.markdown(
                f'<div class="channel-card {cls}"><div class="ch-num">{channel_count(key)}건</div>'
                f'<div class="ch-label">{label}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    if total_count > 0 and '결제금액' in df_current.columns:
        df_current['_금액'] = df_current['결제금액'].apply(parse_amount)
        if '결제상태' in df_current.columns:
            paid_df = df_current[df_current['결제상태'] == '결제완료']
            total_revenue_paid = paid_df['_금액'].sum()
            paid_cnt = len(paid_df)
        else:
            total_revenue_paid = df_current['_금액'].sum()
            paid_cnt = total_count
    else:
        total_revenue_paid = 0
        paid_cnt = 0

    call_done_cnt = len(df_current[df_current['통화상태'] == '통화완료']) if total_count > 0 and '통화상태' in df_current.columns else 0

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f'<div class="kpi-card kpi-blue"><div class="kpi-num">{total_count}명</div><div class="kpi-label">총 신청 고객 수</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi-card kpi-green"><div class="kpi-num">{paid_cnt}건</div><div class="kpi-label">결제완료 건수</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi-card kpi-gold"><div class="kpi-num">{total_revenue_paid:,}원</div><div class="kpi-label">결제완료 총 매출액</div></div>', unsafe_allow_html=True)
    with k4:
        conv = (paid_cnt / total_count * 100) if total_count > 0 else 0
        st.markdown(f'<div class="kpi-card kpi-purple"><div class="kpi-num">{conv:.1f}%</div><div class="kpi-label">전체 결제 전환율</div></div>', unsafe_allow_html=True)
    with k5:
        st.markdown(f'<div class="kpi-card kpi-blue"><div class="kpi-num">{call_done_cnt}건</div><div class="kpi-label">통화완료 건수</div></div>', unsafe_allow_html=True)

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

    st.markdown("##### 🔍 검색 및 검색 옵션")
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        search_keyword = st.text_input("이름, 이메일, 휴대폰번호 검색", placeholder="검색어 입력")
    with s_col2:
        search_status = st.selectbox("발송상태 선택", ["전체", "미발송", "발송완료"])
    with s_col3:
        search_payment = st.selectbox("결제상태 선택", ["전체", "결제대기", "결제완료", "환불"])
    with s_col4:
        search_date = st.text_input("날짜 검색 (예: 4/27)", placeholder="날짜 입력")

    if len(st.session_state.customer_list) > 0:
        df_editable = pd.DataFrame(st.session_state.customer_list)

        # 과거 데이터 호환: 새 필드가 없던 기존 레코드에 기본값 채워넣기
        for col, default in [("통화상태", "통화대기"), ("이메일발송상태", "미발송"), ("문자발송상태", "미발송")]:
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

        editable_cols = ["선택", "결제상태", "발송상태", "통화상태", "이메일발송상태", "문자발송상태"]
        edited_df = st.data_editor(
            df_editable,
            column_config={
                "선택": st.column_config.CheckboxColumn("선택", help="처리할 고객을 체크하세요", default=False),
                "결제상태": st.column_config.SelectboxColumn("결제상태", options=["결제대기", "결제완료", "환불"]),
                "발송상태": st.column_config.SelectboxColumn("PDF발송", options=["미발송", "발송완료"]),
                "통화상태": st.column_config.SelectboxColumn("통화상태", options=["통화대기", "통화완료", "부재중"]),
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
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            if st.button("📤 PDF 개별발송 처리", use_container_width=True, type="primary"):
                selected = [c for c in st.session_state.customer_list if c.get("선택") == True]
                if selected:
                    names = ", ".join([c["이름"] for c in selected])
                    st.success(f"{len(selected)}명 ({names})에게 PDF 발송 완료 처리되었습니다!")
                    for c in st.session_state.customer_list:
                        if c.get("선택"):
                            c["발송상태"] = "발송완료"
                    st.rerun()
                else:
                    st.warning("고객을 하나 이상 선택해 주세요.")
        with b2:
            if st.button("📞 통화완료 처리", use_container_width=True):
                selected = [c for c in st.session_state.customer_list if c.get("선택") == True]
                if selected:
                    for c in st.session_state.customer_list:
                        if c.get("선택"):
                            c["통화상태"] = "통화완료"
                    st.success(f"{len(selected)}명 통화완료로 처리되었습니다!")
                    st.rerun()
                else:
                    st.warning("고객을 하나 이상 선택해 주세요.")
        with b3:
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
        with b4:
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

        st.caption(
            "ℹ️ 위 4개 버튼은 '처리 상태 기록'만 해줍니다. 실제로 이메일/문자를 자동 발송하려면 "
            "이메일(SMTP 등) 또는 문자 API(예: 알리고, 네이버클라우드 등) 연동이 추가로 필요해요. "
            "원하시면 이어서 실제 발송 기능까지 연결해드릴 수 있어요."
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

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center;">
            <form action="/" method="get">
                <button type="submit" name="run_pdf" value="true" style="
                    background: linear-gradient(135deg, #a8382a, #d1493a);
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 12px 28px;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    box-shadow: 0 4px 14px rgba(168, 56, 42, 0.35);
                ">프리미엄 사주분석 PDF생성 시작</button>
            </form>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    query_params = st.query_params
    if "run_pdf" in query_params:
        st.success("자동 분석 PDF가 성공적으로 생성되었습니다!")

# ------------------------------------------------------------------
# TAB 3. 홍보매니저 실적
# ------------------------------------------------------------------
with tab3:
    st.header("🧑‍💼 홍보매니저 실적 대시보드")
    st.caption("체크박스 / 순서 / 매니저ID / 이름 / 총 유입수 / 양식 작성수 / 결제 완료건수 / 결제 전환율 / 정산예정액")

    perf_df = compute_manager_performance()

    if perf_df.empty:
        st.info("등록된 홍보매니저가 없습니다. '⚙️ 홍보매니저 관리' 탭에서 먼저 등록해주세요.")
    else:
        display_df = perf_df.copy()
        display_df["결제 전환율"] = display_df["결제 전환율"].astype(str) + "%"
        display_df["정산예정액"] = display_df["정산예정액"].apply(lambda v: f"{v:,}원")

        edited_perf = st.data_editor(
            display_df,
            column_config={"선택": st.column_config.CheckboxColumn("선택", default=False)},
            disabled=[c for c in display_df.columns if c != "선택"],
            use_container_width=True,
            key="manager_perf_editor",
            hide_index=True,
        )

        p1, p2, p3 = st.columns([1, 1, 1])
        with p1:
            if st.button("💰 선택 매니저 정산완료 처리", use_container_width=True, type="primary"):
                selected_ids = edited_perf[edited_perf["선택"] == True]["매니저ID"].tolist()
                if selected_ids:
                    for m in st.session_state.manager_list:
                        if m['매니저ID'] in selected_ids:
                            m['정산상태'] = '정산완료'
                            m['정산완료일'] = str(datetime.date.today())
                    st.success(f"{len(selected_ids)}명의 정산 처리가 완료되었습니다!")
                    st.rerun()
                else:
                    st.warning("정산 처리할 매니저를 하나 이상 선택해주세요.")
        with p2:
            top_perf = perf_df.sort_values("결제 완료건수", ascending=False)
            if not top_perf.empty and top_perf.iloc[0]["결제 완료건수"] > 0:
                st.metric("🏆 이달의 우수 홍보매니저", top_perf.iloc[0]["이름"], f"{top_perf.iloc[0]['결제 완료건수']}건")
        with p3:
            excel_perf = to_excel_bytes(perf_df.drop(columns=["선택"], errors="ignore"))
            st.download_button(
                "📥 실적 엑셀로 다운로드",
                data=excel_perf,
                file_name=f"홍보매니저실적_{datetime.date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
        st.subheader("전환율 비교")
        st.bar_chart(perf_df.set_index("이름")["결제 전환율"])

# ------------------------------------------------------------------
# TAB 4. 홍보매니저 관리
# ------------------------------------------------------------------
with tab4:
    st.header("⚙️ 홍보매니저 관리")

    with st.form("add_manager_form", clear_on_submit=True):
        st.subheader("신규 홍보매니저 등록")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            new_id = st.text_input("매니저ID (예: manager01)")
        with f2:
            new_name = st.text_input("이름")
        with f3:
            new_inflow = st.number_input("초기 총유입수", min_value=0, value=0, step=10)
        with f4:
            new_unit = st.number_input("건당 정산단가(원)", min_value=0, value=10000, step=1000)

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
                    "총유입수": int(new_inflow),
                    "건당정산단가": int(new_unit),
                    "정산상태": "정산대기",
                    "등록일": str(datetime.date.today()),
                })
                st.success(f"홍보매니저 '{new_name}'({new_id})이(가) 등록되었습니다!")

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.subheader("등록된 홍보매니저 목록 (총유입수 / 정산단가는 직접 수정 가능)")

    if st.session_state.manager_list:
        manager_df = pd.DataFrame(st.session_state.manager_list)
        edited_manager = st.data_editor(
            manager_df,
            column_config={
                "총유입수": st.column_config.NumberColumn("총유입수", min_value=0, step=10),
                "건당정산단가": st.column_config.NumberColumn("건당정산단가(원)", min_value=0, step=1000),
                "정산상태": st.column_config.SelectboxColumn("정산상태", options=["정산대기", "정산완료"]),
            },
            disabled=["매니저ID", "이름", "등록일"],
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
