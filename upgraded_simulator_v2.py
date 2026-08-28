"""
공조냉동 기능사 실습 시뮬레이터 - 업그레이드 V2
3D 시뮬레이션과 고급 2D 학습 환경 (게임화 + 단계별 튜토리얼)
"""

import streamlit as st
from PIL import Image, ImageDraw
import io
import time
from datetime import datetime

# ============================================================
# 세션 상태 초기화
# ============================================================
def init_session_state():
    """게임 상태 초기화"""
    if "points" not in st.session_state:
        st.session_state.points = 0
    if "level" not in st.session_state:
        st.session_state.level = 1
    if "badges" not in st.session_state:
        st.session_state.badges = []
    if "inventory_2d" not in st.session_state:
        st.session_state.inventory_2d = {}
    if "completed_tasks" not in st.session_state:
        st.session_state.completed_tasks = []
    if "current_step" not in st.session_state:
        st.session_state.current_step = {}

# ============================================================
# 포인트/뱃지 시스템
# ============================================================
def add_points(amount: int, reason: str = ""):
    """포인트 추가"""
    st.session_state.points += amount
    
    # 레벨 업 체크 (100포인트당 레벨업)
    new_level = (st.session_state.points // 100) + 1
    if new_level > st.session_state.level:
        st.session_state.level = new_level
        st.balloons()
        st.success(f"🎉 레벨 {new_level}으로 승격!")
    
    if reason:
        st.info(f"✨ +{amount} 포인트 ({reason})")

def add_badge(badge_name: str, description: str):
    """뱃지 획득"""
    if badge_name not in st.session_state.badges:
        st.session_state.badges.append(badge_name)
        st.success(f"🏅 새로운 뱃지 획득: {badge_name} - {description}")

# ============================================================
# 3D 시뮬레이션 임베드
# ============================================================
def show_3d_simulator():
    """3D 실습 시뮬레이터 표시"""
    st.subheader("🎯 3D 인터랙티브 실습")
    st.markdown("**Three.js 기반 완전한 3D 환경에서 실습을 진행하세요!**")

    try:
        with open('hvac_advanced.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        try:
            with open('hvac_practice_3d.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            st.error("3D 시뮬레이션 파일을 찾을 수 없습니다.")
            return

    try:
        st.html(html_content, height=900)
    except:
        st.components.v1.html(html_content, height=900)

    st.markdown("---")
    st.info("""
    **3D 시뮬레이션 사용법:**
    1. 왼쪽 패널에서 작업을 선택하세요
    2. 각 작업이 자동으로 진행됩니다
    3. 오른쪽 패널에서 진행 상황을 확인하세요
    4. 중앙의 3D 환경에서 생성된 부품을 볼 수 있습니다
    """)

# ============================================================
# 2D 고급 학습 시스템
# ============================================================
def draw_step_visual(task_name: str, step: int, total_steps: int) -> Image.Image:
    """단계별 시각화 생성"""
    width = 500
    height = 300
    img = Image.new("RGB", (width, height), color=(245, 245, 250))
    draw = ImageDraw.Draw(img)
    
    # 배경 그라데이션 효과 (텍스트 레이어)
    draw.rectangle([0, 0, width, height], fill=(240, 248, 255), outline=(100, 149, 237), width=3)
    
    # 단계 표시
    draw.text((20, 20), f"📍 {task_name}", fill=(0, 0, 0))
    draw.text((20, 60), f"Step {step}/{total_steps}", fill=(70, 130, 180))
    
    # 진행 바
    bar_width = width - 40
    bar_height = 20
    progress = (step / total_steps) * 100
    filled_width = (bar_width * step) / total_steps
    
    draw.rectangle([20, 100, width-20, 120], outline=(100, 149, 237), width=2)
    draw.rectangle([20, 100, 20 + filled_width, 120], fill=(100, 149, 237))
    draw.text((width//2 - 20, 125), f"{int(progress)}%", fill=(0, 0, 0))
    
    # 작업 설명 영역
    descriptions = {
        "동관 자르기": [
            "1️⃣ 규격 확인: 150mm",
            "2️⃣ 절단선 표시",
            "3️⃣ 안전장비 착용",
            "4️⃣ 정확하게 절단",
            "5️⃣ 가장자리 정리"
        ],
        "파이프 드릴링": [
            "1️⃣ 파이프 고정",
            "2️⃣ 중심 표시",
            "3️⃣ 드릴 위치 맞추기",
            "4️⃣ 드릴링 시작",
            "5️⃣ 구멍 크기 확인"
        ],
        "부품 연결": [
            "1️⃣ 부품 정렬",
            "2️⃣ 연결점 확인",
            "3️⃣ 정렬 고정",
            "4️⃣ 안정성 테스트",
            "5️⃣ 완료 확인"
        ],
        "황동 용접": [
            "1️⃣ 부품 준비",
            "2️⃣ 용접봉 장착",
            "3️⃣ 온도 설정",
            "4️⃣ 9초 가열",
            "5️⃣ 냉각 대기"
        ],
    }
    
    if task_name in descriptions:
        y = 170
        for desc in descriptions[task_name][:3]:
            draw.text((20, y), desc, fill=(50, 50, 50))
            y += 30
    
    return img

def show_2d_advanced_simulator():
    """고급 2D 학습 시뮬레이터"""
    st.subheader("📋 2D 고급 학습 (게임화 버전)")
    
    # 상단 통계 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⭐ 레벨", st.session_state.level)
    with col2:
        st.metric("🎯 포인트", st.session_state.points)
    with col3:
        st.metric("🏅 뱃지", len(st.session_state.badges))
    with col4:
        st.metric("✅ 완료", len(st.session_state.completed_tasks))
    
    st.markdown("---")
    
    # 난이도 선택
    col_diff1, col_diff2 = st.columns([3, 1])
    with col_diff1:
        difficulty = st.radio(
            "난이도 선택:",
            ["초급 🟢", "중급 🟡", "고급 🔴"],
            horizontal=True,
            key="difficulty_selector"
        )
    
    # 작업 선택
    st.write("**📌 수행할 작업 선택**")
    
    col_task1, col_task2, col_task3, col_task4 = st.columns(4)
    
    with col_task1:
        if st.button("🔪 동관 자르기", use_container_width=True, key="task_cut"):
            st.session_state.current_task = "동관 자르기"
    
    with col_task2:
        if st.button("🔧 파이프 드릴링", use_container_width=True, key="task_drill"):
            st.session_state.current_task = "파이프 드릴링"
    
    with col_task3:
        if st.button("🔗 부품 연결", use_container_width=True, key="task_connect"):
            st.session_state.current_task = "부품 연결"
    
    with col_task4:
        if st.button("🔥 황동 용접", use_container_width=True, key="task_weld"):
            st.session_state.current_task = "황동 용접"
    
    if "current_task" not in st.session_state:
        st.session_state.current_task = None
    
    if st.session_state.current_task:
        st.markdown("---")
        show_task_tutorial(st.session_state.current_task, difficulty)

def show_task_tutorial(task_name: str, difficulty: str):
    """단계별 작업 튜토리얼"""
    st.subheader(f"📚 {task_name} - 튜토리얼")
    
    # 난이도별 단계 수 결정
    if "초급" in difficulty:
        steps = 3
        time_per_step = 0.5
    elif "중급" in difficulty:
        steps = 5
        time_per_step = 1.0
    else:  # 고급
        steps = 7
        time_per_step = 1.5
    
    # 단계별 설명
    task_details = {
        "동관 자르기": {
            "steps": [
                "🔍 단계 1: 규격 확인 (150mm)",
                "📏 단계 2: 절단선 표시 (정확히 중앙)",
                "🛡️ 단계 3: 안전장비 착용 (장갑, 고글)",
                "✂️ 단계 4: 정확하게 절단 (수직 절단)",
                "🧹 단계 5: 가장자리 정리 (버 제거)",
                "📦 단계 6: 부품 검사",
                "✅ 단계 7: 인벤토리 등록"
            ],
            "icon": "🔪",
            "reward_points": 100,
            "reward_badge": "완벽한 절단! 🎯"
        },
        "파이프 드릴링": {
            "steps": [
                "🔩 단계 1: 파이프 고정 (클램프 사용)",
                "🎯 단계 2: 중심점 표시 (정확히)",
                "🔧 단계 3: 드릴 위치 맞추기",
                "⚡ 단계 4: 드릴링 시작 (저속에서 시작)",
                "📊 단계 5: 구멍 크기 확인 (지름 확인)",
                "🧽 단계 6: 칩 제거",
                "✅ 단계 7: 품질 검사"
            ],
            "icon": "🔧",
            "reward_points": 150,
            "reward_badge": "정밀 드릴링! ⚙️"
        },
        "부품 연결": {
            "steps": [
                "🧩 단계 1: 부품 준비 (모두 준비)",
                "📐 단계 2: 부품 정렬 (수평 확인)",
                "🔗 단계 3: 연결점 확인 (정확히)",
                "🔨 단계 4: 연결 진행 (부드럽게)",
                "⚖️ 단계 5: 안정성 테스트",
                "👀 단계 6: 최종 검사",
                "✅ 단계 7: 완료 처리"
            ],
            "icon": "🔗",
            "reward_points": 120,
            "reward_badge": "완벽한 조립! 🎁"
        },
        "황동 용접": {
            "steps": [
                "🛡️ 단계 1: 안전 준비 (보호장비 착용)",
                "🔥 단계 2: 용접기 준비",
                "🧲 단계 3: 부품 고정 (자석 사용)",
                "🌡️ 단계 4: 온도 설정 (800°C)",
                "⏱️ 단계 5: 9초 가열 (정확히)",
                "❄️ 단계 6: 냉각 (물에 담그기)",
                "✅ 단계 7: 품질 검사"
            ],
            "icon": "🔥",
            "reward_points": 200,
            "reward_badge": "마스터 용접공! 🏆"
        }
    }
    
    if task_name not in task_details:
        st.error("존재하지 않는 작업입니다")
        return
    
    details = task_details[task_name]
    
    # 현재 진행 상황 표시
    progress_col1, progress_col2 = st.columns([3, 1])
    with progress_col1:
        step_progress = st.progress(0)
    with progress_col2:
        st.markdown(f"**0/{len(details['steps'])}**")
    
    # 각 단계별 버튼
    st.write("**📍 단계별 진행:**")
    
    for idx, step_desc in enumerate(details['steps'], 1):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(step_desc)
        
        with col2:
            if st.button("▶️ 진행", key=f"step_{idx}_{task_name}"):
                with st.spinner(f"진행 중... ({idx}/{len(details['steps'])})"):
                    # 진행 시뮬레이션
                    for i in range(101):
                        step_progress.progress(i / 100)
                        time.sleep(0.01)
                    
                    # 단계 완료
                    progress_col1.progress(idx / len(details['steps']))
                    progress_col2.metric("진행", f"{idx}/{len(details['steps'])}")
                    
                    st.success(f"✅ {step_desc} 완료!")
                    
                    # 마지막 단계이면 작업 완료
                    if idx == len(details['steps']):
                        complete_task(task_name, details)
                        return
        
        with col3:
            difficulty_level = "🟢" if "초급" in difficulty else ("🟡" if "중급" in difficulty else "🔴")
            st.write(difficulty_level)
    
    # 한 번에 모두 수행 버튼
    st.markdown("---")
    if st.button(f"⚡ 전체 {task_name} 빠르게 완료", use_container_width=True):
        with st.spinner("작업 진행 중..."):
            progress_bar = st.progress(0)
            for i in range(len(details['steps'])):
                for j in range(101):
                    progress_bar.progress((i * 100 + j) / (len(details['steps']) * 100))
                    time.sleep(0.005)
            progress_bar.progress(1.0)
        
        complete_task(task_name, details)

def complete_task(task_name: str, details: dict):
    """작업 완료 처리"""
    if task_name not in st.session_state.completed_tasks:
        st.session_state.completed_tasks.append(task_name)
    
    # 포인트 추가
    add_points(details["reward_points"], f"{task_name} 완료!")
    
    # 뱃지 추가
    add_badge(task_name, details["reward_badge"])
    
    # 인벤토리에 부품 추가
    if "inventory_2d" not in st.session_state:
        st.session_state.inventory_2d = {}
    
    if task_name == "동관 자르기":
        st.session_state.inventory_2d["동관(150mm)"] = st.session_state.inventory_2d.get("동관(150mm)", 0) + 1
    elif task_name == "파이프 드릴링":
        st.session_state.inventory_2d["드릴링된_파이프"] = st.session_state.inventory_2d.get("드릴링된_파이프", 0) + 1
    elif task_name == "부품 연결":
        st.session_state.inventory_2d["연결된_부품"] = st.session_state.inventory_2d.get("연결된_부품", 0) + 1
    elif task_name == "황동 용접":
        st.session_state.inventory_2d["용접된_조립"] = st.session_state.inventory_2d.get("용접된_조립", 0) + 1
    
    # 성공 메시지
    st.balloons()
    st.success(f"""
    🎉 **{task_name} 완료!**
    
    ✨ +{details['reward_points']} 포인트 획득!
    🏅 뱃지: {details['reward_badge']}
    """)

# ============================================================
# 이론 및 참고 자료
# ============================================================
def show_theory_section():
    """실습 이론 및 참고 자료"""
    st.subheader("📚 실습 이론")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.expander("🔪 동관 자르기"):
            st.write("""
            **목적**: 규격에 맞는 동관 준비

            **중요 포인트**:
            - 정확한 길이 측정 필수
            - 수직 절단이 중요
            - 버(edge) 완벽 제거
            - 안전장비 필수

            **팁**:
            - 절단선을 펜으로 표시
            - 천천히 진행
            - 절단 후 세척 필수
            """)

    with col2:
        with st.expander("🔧 파이프 드릴링"):
            st.write("""
            **목적**: 파이프에 정확한 구멍 뚫기

            **중요 포인트**:
            - 중심점 정확히 표시
            - 저속에서 시작
            - 파이프 안정화 필수
            - 칩 제거 중요

            **팁**:
            - 클램프로 고정
            - 냉각 오일 사용
            - 천천히 진행
            """)

    with col3:
        with st.expander("🔗 부품 연결"):
            st.write("""
            **목적**: 부품들을 정확히 연결

            **중요 포인트**:
            - 정렬 정확도 매우 중요
            - 수평 유지 필수
            - 부드럽게 진행
            - 최종 검사 필수

            **팁**:
            - 정렬 도구 사용
            - 힘 가하지 말 것
            - 여러 번 확인
            """)

    with col4:
        with st.expander("🔥 황동 용접"):
            st.write("""
            **목적**: 부품들을 용접으로 접합

            **중요 포인트**:
            - 정확한 온도 유지
            - 9초 이상 가열
            - 냉각 절차 중요
            - 보호장비 필수

            **팁**:
            - 온도계 사용
            - 천천히 냉각
            - 통풍 필수
            """)

# ============================================================
# 성취도 및 통계
# ============================================================
def show_achievements():
    """성취도 및 마일스톤 표시"""
    st.subheader("🏆 성취도 추적 및 통계")
    
    # 주요 통계
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 총 포인트", st.session_state.points, f"{st.session_state.level} 레벨")
    
    with col2:
        completion_rate = (len(st.session_state.completed_tasks) / 4) * 100
        st.metric("📊 완료율", f"{int(completion_rate)}%", f"{len(st.session_state.completed_tasks)}/4")
    
    with col3:
        st.metric("🏅 뱃지", len(st.session_state.badges), "개 획득")
    
    with col4:
        if st.session_state.points > 0:
            hours_to_complete = max(1, (1000 - st.session_state.points) / 100)
            st.metric("⏱️ 예상 시간", f"{hours_to_complete:.1f}", "시간")
    
    st.markdown("---")
    
    # 획득한 뱃지 표시
    st.write("**🏅 획득한 뱃지**")
    if st.session_state.badges:
        cols = st.columns(len(st.session_state.badges))
        for idx, badge in enumerate(st.session_state.badges):
            with cols[idx]:
                st.success(f"✅ {badge}")
    else:
        st.info("아직 뱃지를 획득하지 않았습니다")
    
    st.markdown("---")
    
    # 마일스톤
    st.write("**🎯 마일스톤**")
    milestones = [
        ("동관 자르기 습득", "동관 자르기" in st.session_state.completed_tasks),
        ("파이프 드릴링 습득", "파이프 드릴링" in st.session_state.completed_tasks),
        ("부품 연결 기술 습득", "부품 연결" in st.session_state.completed_tasks),
        ("황동 용접 기술 습득", "황동 용접" in st.session_state.completed_tasks),
    ]

    for milestone, completed in milestones:
        if completed:
            st.success(f"✅ {milestone}")
        else:
            st.info(f"⬜ {milestone}")
    
    st.markdown("---")
    
    # 학습 진도 차트
    st.write("**📈 학습 진도**")
    progress_data = {
        "동관 자르기": 100 if "동관 자르기" in st.session_state.completed_tasks else 30,
        "파이프 드릴링": 100 if "파이프 드릴링" in st.session_state.completed_tasks else 20,
        "부품 연결": 100 if "부품 연결" in st.session_state.completed_tasks else 15,
        "황동 용접": 100 if "황동 용접" in st.session_state.completed_tasks else 10,
    }
    
    for task, progress in progress_data.items():
        st.progress(progress / 100, f"{task}: {progress}%")

# ============================================================
# 인벤토리 표시
# ============================================================
def show_inventory():
    """인벤토리 표시"""
    st.subheader("📦 인벤토리")
    
    if st.session_state.inventory_2d:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**보유 부품:**")
            for item, count in st.session_state.inventory_2d.items():
                if count > 0:
                    st.write(f"• **{item}**: {count}개")
        
        with col2:
            st.write("**전체 부품 수:**")
            total = sum(st.session_state.inventory_2d.values())
            st.metric("보유 총 부품", total, "개")
        
        if st.button("🗑️ 인벤토리 초기화"):
            st.session_state.inventory_2d = {}
            st.rerun()
    else:
        st.info("💭 아직 부품이 없습니다. 작업을 완료해보세요!")

# ============================================================
# 메인 함수
# ============================================================
def run_upgraded_simulator_v2():
    """업그레이드된 실습 시뮬레이터 V2 메인"""
    st.title("🛠️ 공조냉동 실습 시뮬레이터 - 고급 버전")
    st.markdown("**3D 시뮬레이션 + 게임화된 2D 학습 환경**")

    # 세션 상태 초기화
    init_session_state()

    # 탭 구성
    tab_3d, tab_2d_advanced, tab_theory, tab_stats, tab_inventory = st.tabs([
        "🎮 3D 시뮬레이션",
        "📊 2D 고급 학습",
        "📚 이론",
        "🏆 성취도",
        "📦 인벤토리"
    ])

    with tab_3d:
        show_3d_simulator()

    with tab_2d_advanced:
        show_2d_advanced_simulator()

    with tab_theory:
        show_theory_section()

    with tab_stats:
        show_achievements()

    with tab_inventory:
        show_inventory()

    # 사이드바
    with st.sidebar:
        st.markdown("### 🎮 게임 상태")
        st.write(f"**레벨**: {st.session_state.level} ⭐")
        st.write(f"**포인트**: {st.session_state.points} 🎯")
        st.write(f"**뱃지**: {len(st.session_state.badges)} 🏅")
        st.write(f"**완료 작업**: {len(st.session_state.completed_tasks)} ✅")
        
        st.markdown("---")
        
        st.markdown("### 💡 학습 팁")
        tips = [
            "각 작업을 단계별로 천천히 진행하세요",
            "3D와 2D를 함께 활용하면 더 효과적입니다",
            "모든 작업을 완료하면 마스터 레벨에 도달합니다!",
            "뱃지를 모두 모으는 것이 목표입니다"
        ]
        for i, tip in enumerate(tips, 1):
            st.info(f"**{i}. {tip}**")
        
        st.markdown("---")
        
        st.markdown("### 🎓 난이도별 특징")
        with st.expander("초급 🟢"):
            st.write("3단계 작업, 기본 개념 학습")
        with st.expander("중급 🟡"):
            st.write("5단계 작업, 심화 학습")
        with st.expander("고급 🔴"):
            st.write("7단계 작업, 전문가 레벨")
