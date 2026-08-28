"""
공조냉동 기능사 실습 시뮬레이터 - 업그레이드 버전
3D 시뮬레이션과 2D 시뮬레이션을 통합한 하이브리드 환경
"""

import streamlit as st
from PIL import Image, ImageDraw
import io
import time
from datetime import datetime

# ============================================================
# 3D 시뮬레이션 임베드
# ============================================================
def show_3d_simulator():
    """3D 실습 시뮬레이터 표시"""
    st.subheader("🎯 3D 인터랙티브 실습")
    st.markdown("**Three.js 기반 완전한 3D 환경에서 실습을 진행하세요!**")

    try:
        with open('hvac_practice_3d.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        try:
            st.html(html_content)
        except:
            st.components.v1.html(html_content, height=900)
    except FileNotFoundError:
        st.error("3D 시뮬레이션 파일을 찾을 수 없습니다. hvac_practice_3d.html 파일을 확인하세요.")

    st.markdown("---")
    st.info("""
    **3D 시뮬레이션 사용법:**
    1. 왼쪽 패널에서 작업을 선택하세요
    2. 각 작업이 자동으로 진행됩니다
    3. 오른쪽 패널에서 진행 상황을 확인하세요
    4. 중앙의 3D 환경에서 생성된 부품을 볼 수 있습니다
    """)

# ============================================================
# 2D 시뮬레이션 (Streamlit 기반)
# ============================================================
def draw_copper_tube(length: int) -> Image.Image:
    """동관 이미지 그리기"""
    width = 400
    height = 100
    img = Image.new("RGB", (width, height), color=(240, 245, 250))
    draw = ImageDraw.Draw(img)

    tube_width = min(length * 1.2, 350)
    tube_height = 40
    x_start = (width - tube_width) / 2
    y_start = (height - tube_height) / 2

    draw.rectangle(
        [x_start, y_start, x_start + tube_width, y_start + tube_height],
        fill=(184, 115, 51),  # 동색
        outline=(139, 69, 19),
        width=3
    )

    draw.text((10, 10), f"길이: {length}mm", fill=(0, 0, 0))
    return img

def show_2d_simulator():
    """2D 시뮬레이터 표시"""
    st.subheader("📋 2D 학습 환경")
    st.markdown("**단계별 작업을 직관적인 UI로 진행합니다.**")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("**작업 선택**")
        task_type = st.radio(
            "수행할 작업:",
            ["동관 자르기", "파이프 드릴링", "용접", "밴딩"],
            horizontal=True
        )

        if task_type == "동관 자르기":
            st.write("**규격 설정 (최대 350mm)**")
            length = st.slider("동관 길이", 50, 350, 150, step=10)
            quantity = st.number_input("수량", min_value=1, max_value=10, value=1)

            if st.button("🔪 자르기 시작"):
                with st.spinner("동관을 자르는 중..."):
                    progress_bar = st.progress(0)
                    for i in range(101):
                        progress_bar.progress(i)
                        time.sleep(0.01)

                st.success(f"✅ 동관 {length}mm × {quantity}개 자르기 완료!")
                if "inventory_2d" not in st.session_state:
                    st.session_state.inventory_2d = {}
                key = f"동관_{length}mm"
                st.session_state.inventory_2d[key] = st.session_state.inventory_2d.get(key, 0) + quantity

        elif task_type == "파이프 드릴링":
            st.write("**파이프 규격**")
            st.write("• 지름: 3cm, 길이: 10cm")

            if st.button("🔧 드릴링 시작"):
                with st.spinner("파이프에 구멍을 뚫는 중..."):
                    progress_bar = st.progress(0)
                    for i in range(101):
                        progress_bar.progress(i)
                        time.sleep(0.015)

                st.success("✅ 파이프 드릴링 완료!")
                if "inventory_2d" not in st.session_state:
                    st.session_state.inventory_2d = {}
                st.session_state.inventory_2d["드릴링된_파이프"] = st.session_state.inventory_2d.get("드릴링된_파이프", 0) + 1

        elif task_type == "용접":
            st.write("**황동용접**")
            st.write("⏱️ 용접 시간: 9초")

            if st.button("🔥 용접 시작"):
                with st.spinner("용접을 진행 중..."):
                    progress_bar = st.progress(0)
                    for i in range(91):
                        progress_bar.progress(i)
                        time.sleep(0.1)

                st.success("✅ 황동용접 완료!")
                st.balloons()

        elif task_type == "밴딩":
            st.write("**밴딩 작업**")
            angle = st.slider("밴딩 각도", 0, 180, 90, step=15)

            if st.button("📐 밴딩 시작"):
                with st.spinner("밴딩을 진행 중..."):
                    progress_bar = st.progress(0)
                    for i in range(81):
                        progress_bar.progress(i)
                        time.sleep(0.02)

                st.success(f"✅ {angle}° 각도로 밴딩 완료!")

    with col2:
        st.write("**📦 인벤토리**")
        if "inventory_2d" in st.session_state and st.session_state.inventory_2d:
            for item, count in st.session_state.inventory_2d.items():
                if count > 0:
                    st.write(f"• {item}: **{count}**")
        else:
            st.info("부품이 없습니다")

        if st.button("인벤토리 초기화"):
            st.session_state.inventory_2d = {}
            st.rerun()

# ============================================================
# 이론 및 참고 자료
# ============================================================
def show_theory_section():
    """실습 이론 및 참고 자료"""
    st.subheader("📚 실습 이론")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander("🔪 동관 자르기"):
            st.write("""
            **목적**: 규격에 맞는 동관 준비

            **절차**:
            1. 규격 확인 (최대 350mm)
            2. 절단선 표시
            3. 정확하게 자르기
            4. 가장자리 정리

            **주의사항**:
            - 안전장비 착용 필수
            - 정확한 길이 측정
            - 버(edge) 제거
            """)

    with col2:
        with st.expander("🔧 파이프 드릴링"):
            st.write("""
            **목적**: 파이프 중앙에 정확한 구멍 뚫기

            **절차**:
            1. 파이프 중심 표시
            2. 드릴 위치 맞추기
            3. 안정적으로 드릴링
            4. 구멍 크기 확인

            **팁**:
            - 드릴 속도 조절 중요
            - 파이프 안정화 필수
            - 정확한 중심 위치
            """)

    with col3:
        with st.expander("🔥 황동용접"):
            st.write("""
            **목적**: 동관과 파이프 접합

            **절차**:
            1. 부품 정렬
            2. 용접봉 준비
            3. 정확한 온도 유지
            4. 9초 이상 가열

            **안전**:
            - 보호 장비 필수
            - 적절한 환기
            - 냉각 절차 준수
            """)

# ============================================================
# 성취도 및 통계
# ============================================================
def show_achievements():
    """성취도 및 마일스톤 표시"""
    st.subheader("🏆 성취도 추적")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("완료한 작업", 0, "/ 7")

    with col2:
        st.metric("학습 진도", 0, "%")

    with col3:
        st.metric("예상 완료", "-", "시간")

    st.markdown("---")

    st.write("**🎯 마일스톤**")
    milestones = [
        ("동관 자르기 습득", False),
        ("파이프 드릴링 습득", False),
        ("연결 기술 습득", False),
        ("용접 기술 습득", False),
        ("냉각 절차 학습", False),
        ("밴딩 기술 습득", False),
        ("플레어링 기술 습득", False),
    ]

    for milestone, completed in milestones:
        if completed:
            st.success(f"✅ {milestone}")
        else:
            st.info(f"⬜ {milestone}")

# ============================================================
# 메인 함수
# ============================================================
def run_upgraded_simulator():
    """업그레이드된 실습 시뮬레이터 메인"""
    st.title("🛠️ 공조냉동 실습 시뮬레이터 - 하이브리드 버전")
    st.markdown("**3D + 2D 통합 실습 환경**")

    # 세션 상태 초기화
    if "inventory_2d" not in st.session_state:
        st.session_state.inventory_2d = {}

    # 탭 구성
    tab_3d, tab_2d, tab_theory, tab_stats = st.tabs([
        "🎮 3D 시뮬레이션",
        "📊 2D 학습",
        "📚 이론",
        "🏆 성취도"
    ])

    with tab_3d:
        show_3d_simulator()

    with tab_2d:
        show_2d_simulator()

    with tab_theory:
        show_theory_section()

    with tab_stats:
        show_achievements()

    # 사이드바 정보
    with st.sidebar:
        st.markdown("### 💡 팁")
        st.write("""
        • **3D 버전**: 완전한 3D 환경에서 실습
        • **2D 버전**: 단계별 학습
        • **이론 탭**: 각 작업의 이론 학습
        • **성취도**: 진행 상황 확인
        """)

        st.markdown("### 🎓 난이도")
        difficulty = st.radio("선택하신 난이도:", ["초급 🟢", "중급 🟡", "고급 🔴"])
        if difficulty:
            st.success(f"선택됨: {difficulty}")
