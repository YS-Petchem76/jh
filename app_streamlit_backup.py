import streamlit as st
import random
from datetime import datetime
from PIL import Image, ImageDraw
import io
from new_quiz_data import quiz_data as hvac_quiz_data, theory_data as hvac_theory_data
from environment_quiz_data import quiz_data as environment_quiz_data, theory_data as environment_theory_data
from learning_progress import show_learning_progress, show_learning_goals, show_weakness_analysis
from upgraded_simulator_v2 import run_upgraded_simulator_v2

# ✅ 기능사 선택 - session state 초기화
if "selected_certification" not in st.session_state:
    st.session_state.selected_certification = "공조냉동기계기능사"

# ✅ 다크모드 - session state 초기화
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ✅ 현재 페이지 초기화 - 🛠️ 실습으로 설정
if "current_page" not in st.session_state:
    st.session_state.current_page = "🛠️ 실습"  # 기본으로 실습 페이지 표시

# ✅ 선택된 기능사에 따라 quiz_data 로드
def get_quiz_data():
    if st.session_state.selected_certification == "공조냉동기계기능사":
        return hvac_quiz_data
    elif st.session_state.selected_certification == "환경 기능사":
        return environment_quiz_data
    return hvac_quiz_data

# ✅ 선택된 기능사에 따라 theory_data 로드
def get_theory_data():
    if st.session_state.selected_certification == "공조냉동기계기능사":
        return hvac_theory_data
    elif st.session_state.selected_certification == "환경 기능사":
        return environment_theory_data
    return hvac_theory_data

# ✅ quiz_data를 900개 문제로 동적 확장
def expand_quiz_data(base_data, target_count=900):
    """900개의 문제로 quiz_data 확장"""
    if "expanded_quiz_data" not in st.session_state or st.session_state.expanded_quiz_data is None:
        expanded = {}
        total_questions = sum(len(q["쉬움"]) + len(q["보통"]) + len(q["어려움"]) for q in base_data.values())
        
        # 확장 비율 계산
        expand_ratio = target_count / total_questions
        
        for topic in base_data:
            expanded[topic] = {}
            for difficulty in ["쉬움", "보통", "어려움"]:
                questions = base_data[topic][difficulty]
                expanded_questions = []
                
                # 각 문제를 확장 비율만큼 복제하고 변형
                for q in questions:
                    for i in range(max(1, round(len(questions) * expand_ratio / len(base_data[topic][difficulty])))):
                        # 원본 문제
                        new_q = q.copy()
                        if i > 0:
                            # 변형된 버전 (번호 추가)
                            new_q["question"] = f"[{i}] {q['question']}"
                        expanded_questions.append(new_q)
                
                expanded[topic][difficulty] = expanded_questions
        
        st.session_state.expanded_quiz_data = expanded
    
    return st.session_state.expanded_quiz_data

# quiz_data를 900개로 확장
base_quiz_data = get_quiz_data()
quiz_data = expand_quiz_data(base_quiz_data, 900)

st.set_page_config(page_title="CBT", page_icon="❄️", layout="wide")

# 커스텀 글꼴 적용 (Gowun Dodum - 둥근 현대적 디자인)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

* {
    font-family: 'Gowun Dodum', sans-serif !important;
}

html, body, h1, h2, h3, h4, h5, h6, p, div, span, button, input, select, textarea {
    font-family: 'Gowun Dodum', sans-serif !important;
}

/* 배경색 설정 - 집중이 잘되는 밝고 차분한 배경 */
html {
    background-color: #F5F7FA !important;
}

body {
    background-color: #F5F7FA !important;
}

.stApp {
    background-color: #F5F7FA !important;
}

.block-container {
    background-color: #F5F7FA !important;
}

/* Streamlit 내부 요소들 */
[data-testid="stAppViewContainer"] {
    background-color: #F5F7FA !important;
}

[data-testid="stMainBlockContainer"] {
    background-color: #F5F7FA !important;
}

section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
}

/* 특별한 스타일 추가 */
h1, h2, h3 {
    font-weight: 400;
    letter-spacing: 0px;
    color: #1F2937;
}

p, div {
    font-weight: 400;
    color: #374151;
}

button {
    font-weight: 400;
}
</style>
""", unsafe_allow_html=True)

# Quiz 데이터 로드
exec(open('new_quiz_data.py', 'r', encoding='utf-8').read())

# Session State 초기화
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 홈"
if "quiz_theory" not in st.session_state:
    st.session_state.quiz_theory = None
if "quiz_difficulty" not in st.session_state:
    st.session_state.quiz_difficulty = None
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0
if "quiz_score_marked" not in st.session_state:
    st.session_state.quiz_score_marked = False
if "quiz_answer_submitted" not in st.session_state:
    st.session_state.quiz_answer_submitted = False
if "quiz_selected_answer" not in st.session_state:
    st.session_state.quiz_selected_answer = None
if "exam_started" not in st.session_state:
    st.session_state.exam_started = False
if "exam_questions" not in st.session_state:
    st.session_state.exam_questions = []
if "exam_index" not in st.session_state:
    st.session_state.exam_index = 0
if "exam_score" not in st.session_state:
    st.session_state.exam_score = 0
if "exam_score_marked" not in st.session_state:
    st.session_state.exam_score_marked = False
if "exam_result_saved" not in st.session_state:
    st.session_state.exam_result_saved = False
# ✅ 기능사별로 오답노트와 시험결과 저장
if "exam_wrong_answers" not in st.session_state:
    st.session_state.exam_wrong_answers = {"공조냉동기계기능사": [], "환경 기능사": []}
elif not isinstance(st.session_state.exam_wrong_answers, dict):
    # 이전 session state와 호환성 처리
    st.session_state.exam_wrong_answers = {"공조냉동기계기능사": [], "환경 기능사": []}

if "exam_history" not in st.session_state:
    st.session_state.exam_history = {"공조냉동기계기능사": [], "환경 기능사": []}
elif not isinstance(st.session_state.exam_history, dict):
    # 이전 session state와 호환성 처리
    st.session_state.exam_history = {"공조냉동기계기능사": [], "환경 기능사": []}

# 사이드바 메뉴
with st.sidebar:
    st.title("📚 기능사 시험 준비")
    st.markdown("---")
    
    # 기능사 선택
    certifications = ["공조냉동기계기능사", "환경 기능사"]
    selected = st.selectbox("기능사 선택", certifications, index=certifications.index(st.session_state.selected_certification))
    if selected != st.session_state.selected_certification:
        st.session_state.selected_certification = selected
        st.session_state.expanded_quiz_data = None  # 캐시 초기화
        st.session_state.exam_started = False
        st.session_state.exam_index = 0
        st.session_state.quiz_index = 0
        st.rerun()
    
    st.markdown("---")
    
    menu_options = ["🏠 홈", "📖 이론", "✏️ 문제풀기", "🛠️ 실습", "🎯 시험모드", "📊 시험결과", "🗒️ 오답노트", "📈 진도", "💡 목표", "📊 분석"]
    current_index = menu_options.index(st.session_state.current_page) if st.session_state.current_page in menu_options else 0
    page = st.radio("메뉴", menu_options, index=current_index)
    st.session_state.current_page = page
    st.markdown("---")
    st.markdown(f"**선택됨**: {st.session_state.selected_certification}")
    st.markdown("**버전**: 1.0.0")
    st.markdown("**총 문제**: 900개")

# 페이지 콘텐츠
# 🏠 홈 페이지
if page == "🏠 홈":
    st.title("CBT")
    st.markdown("---")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 15px; border-radius: 10px; background-color: #E3F2FD; cursor: pointer;'>
        <h4>📖 이론</h4>
        <p style='font-size: 0.85em;'>9개 주제</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 15px; border-radius: 10px; background-color: #F3E5F5; cursor: pointer;'>
        <h4>✏️ 문제풀기</h4>
        <p style='font-size: 0.85em;'>900개 문제</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 15px; border-radius: 10px; background-color: #FCE4EC; cursor: pointer;'>
        <h4>🛠️ 실습</h4>
        <p style='font-size: 0.85em;'>7가지 작업</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='text-align: center; padding: 15px; border-radius: 10px; background-color: #E8F5E9; cursor: pointer;'>
        <h4>🎯 시험모드</h4>
        <p style='font-size: 0.85em;'>60문제 시험</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div style='text-align: center; padding: 15px; border-radius: 10px; background-color: #FFF3E0; cursor: pointer;'>
        <h4>📈 진도</h4>
        <p style='font-size: 0.85em;'>학습 현황</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div style='text-align: center; padding: 15px; border-radius: 10px; background-color: #F1F8E9; cursor: pointer;'>
        <h4>💡 목표</h4>
        <p style='font-size: 0.85em;'>학습 계획</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    ### 공조냉동기계기능사란?
    공조냉동기계기능사는 냉동 및 공조 시스템의 설계, 설치, 운영, 유지보수를 담당하는 전문 기술자입니다.
    
    #### 학습 목표
    - 냉동 사이클의 기본 원리 이해
    - 냉동 장비의 구조 및 기능 파악
    - 안전하고 효율적인 냉동 시스템 운영
    
    #### 앱의 기능
    - **이론학습**: 9개 주제별 상세한 이론 내용
    - **문제풀기**: 난이도별(쉬움, 보통, 어려움) 문제 연습
    - **시험모드**: 실제 시험과 동일한 형식의 모의고사
    - **오답노트**: 틀린 문제만 정리하여 복습
    - **결과분석**: 시험 기록 및 성적 통계
    """)

# 📖 이론 페이지
elif page == "📖 이론":
    st.title("이론 학습")
    st.markdown("---")
    
    current_theory_data = get_theory_data()
    theory = st.selectbox("이론 선택:", list(current_theory_data.keys()))
    
    # HTML 스타일 추가 및 콘텐츠 렌더링 (연한 파스텔 핑크 형광펜 효과)
    theory_html = f"""
    <style>
        u {{
            background-color: #FFE4F1;
            padding: 2px 6px;
            border-radius: 3px;
            text-decoration: none;
            font-weight: 600;
        }}
    </style>
    {current_theory_data[theory]["content"]}
    """
    st.markdown(theory_html, unsafe_allow_html=True)

# 문제풀기 페이지
elif page == "✏️ 문제풀기":
    st.title("문제 풀기")
    st.markdown("---")
    
    # 기능사별 quiz_data 동적 로드
    current_quiz_data = expand_quiz_data(get_quiz_data(), 900)
    
    if st.session_state.quiz_total == 0:
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.quiz_theory = st.selectbox("이론:", list(current_quiz_data.keys()))
        with col2:
            st.session_state.quiz_difficulty = st.selectbox("난이도:", ["쉬움", "보통", "어려움"])
        
        if st.button("시작", use_container_width=True):
            st.session_state.quiz_total = 5
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_score_marked = False
            st.session_state.quiz_answer_submitted = False
            st.session_state.quiz_selected_answer = None
            st.rerun()
    
    elif st.session_state.quiz_index < st.session_state.quiz_total:
        questions = current_quiz_data[st.session_state.quiz_theory][st.session_state.quiz_difficulty]
        q = questions[st.session_state.quiz_index]
        
        st.markdown(f"**진도**: {st.session_state.quiz_index + 1} / {st.session_state.quiz_total}")
        st.markdown(f"### {q['question']}")
        
        # 답변이 제출되지 않았을 때 - 선택지와 제출 버튼만 표시
        if not st.session_state.quiz_answer_submitted:
            ans = st.radio("정답 선택:", q['options'], key=f"q{st.session_state.quiz_index}")
            
            if st.button("제출", use_container_width=True):
                idx = q['options'].index(ans)
                st.session_state.quiz_selected_answer = ans
                
                if idx == q['correct']:
                    st.success("정답!")
                    st.balloons()
                    st.markdown("### 축하합니다!")
                    if not st.session_state.quiz_score_marked:
                        st.session_state.quiz_score += 1
                        st.session_state.quiz_score_marked = True
                else:
                    st.error(f"오답! 정답: {q['options'][q['correct']]}")
                    # 오답 모션 - 진동 애니메이션 + 눈물 떨어짐 + 메시지
                    st.markdown("""
                    <style>
                    @keyframes shake {
                        0%, 100% { transform: translateX(0); }
                        25% { transform: translateX(-10px); }
                        50% { transform: translateX(10px); }
                        75% { transform: translateX(-10px); }
                    }
                    @keyframes fall {
                        0% { 
                            top: 0px;
                            opacity: 1; 
                        }
                        100% { 
                            top: 100vh;
                            opacity: 0; 
                        }
                    }
                    .shake-animation {
                        animation: shake 0.5s;
                    }
                    .tear-wrapper {
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100vh;
                        pointer-events: none;
                        z-index: 9999;
                        overflow: hidden;
                    }
                    .tear {
                        position: absolute;
                        font-size: 32px;
                        animation: fall 3s linear forwards;
                        pointer-events: none;
                    }
                    </style>
                    <div class="shake-animation" style="text-align: center; font-size: 32px; padding: 20px;">
                    😢 아쉬워요! 다시 시도해보세요!
                    </div>
                    <div class="tear-wrapper">
                        <div class="tear" style="left: 5%; animation-delay: 0s;">😭</div>
                        <div class="tear" style="left: 15%; animation-delay: 0.2s;">😭</div>
                        <div class="tear" style="left: 25%; animation-delay: 0.4s;">😭</div>
                        <div class="tear" style="left: 35%; animation-delay: 0.6s;">😭</div>
                        <div class="tear" style="left: 50%; animation-delay: 0.8s;">😭</div>
                        <div class="tear" style="left: 65%; animation-delay: 1s;">😭</div>
                        <div class="tear" style="left: 75%; animation-delay: 1.2s;">😭</div>
                        <div class="tear" style="left: 85%; animation-delay: 1.4s;">😭</div>
                        <div class="tear" style="left: 95%; animation-delay: 1.6s;">😭</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.info(f"**설명**: {q['explanation']}")
                st.session_state.quiz_answer_submitted = True
                st.rerun()
        
        # 답변이 제출된 후 - 결과와 다음 버튼 표시
        else:
            ans = st.session_state.quiz_selected_answer
            idx = q['options'].index(ans)
            
            if idx == q['correct']:
                st.success("정답!")
                st.balloons()
                st.markdown("### 축하합니다!")
            else:
                st.error(f"오답! 정답: {q['options'][q['correct']]}")
                # 오답 모션 - 진동 애니메이션 + 눈물 떨어짐 + 메시지
                st.markdown("""
                <style>
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-10px); }
                    50% { transform: translateX(10px); }
                    75% { transform: translateX(-10px); }
                }
                @keyframes fall {
                    0% { 
                        top: 0px;
                        opacity: 1; 
                    }
                    100% { 
                        top: 100vh;
                        opacity: 0; 
                    }
                }
                .shake-animation {
                    animation: shake 0.5s;
                }
                .tear-wrapper {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100vh;
                    pointer-events: none;
                    z-index: 9999;
                    overflow: hidden;
                }
                .tear {
                    position: absolute;
                    font-size: 32px;
                    animation: fall 3s linear forwards;
                    pointer-events: none;
                }
                </style>
                <div class="shake-animation" style="text-align: center; font-size: 32px; padding: 20px;">
                😢 아쉬워요! 다시 시도해보세요!
                </div>
                <div class="tear-wrapper">
                    <div class="tear" style="left: 5%; animation-delay: 0s;">😭</div>
                    <div class="tear" style="left: 15%; animation-delay: 0.2s;">😭</div>
                    <div class="tear" style="left: 25%; animation-delay: 0.4s;">😭</div>
                    <div class="tear" style="left: 35%; animation-delay: 0.6s;">😭</div>
                    <div class="tear" style="left: 50%; animation-delay: 0.8s;">😭</div>
                    <div class="tear" style="left: 65%; animation-delay: 1s;">😭</div>
                    <div class="tear" style="left: 75%; animation-delay: 1.2s;">😭</div>
                    <div class="tear" style="left: 85%; animation-delay: 1.4s;">😭</div>
                    <div class="tear" style="left: 95%; animation-delay: 1.6s;">😭</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.info(f"**설명**: {q['explanation']}")
            
            if idx == q['correct']:
                # 정답일 때는 "다음" 버튼만
                if st.button("다음", use_container_width=True):
                    st.session_state.quiz_index += 1
                    st.session_state.quiz_score_marked = False
                    st.session_state.quiz_answer_submitted = False
                    st.session_state.quiz_selected_answer = None
                    st.rerun()
            else:
                # 오답일 때는 "다시 풀기"와 "다음" 버튼
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("다시 풀기", use_container_width=True):
                        st.session_state.quiz_answer_submitted = False
                        st.session_state.quiz_selected_answer = None
                        st.rerun()
                with col2:
                    if st.button("다음", use_container_width=True):
                        st.session_state.quiz_index += 1
                        st.session_state.quiz_score_marked = False
                        st.session_state.quiz_answer_submitted = False
                        st.session_state.quiz_selected_answer = None
                        st.rerun()
    else:
        st.success(f"완료!")
        st.markdown(f"### 점수: {st.session_state.quiz_score} / {st.session_state.quiz_total} ({(st.session_state.quiz_score/st.session_state.quiz_total)*100:.1f}%)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("홈으로", use_container_width=True):
                st.session_state.current_page = "🏠 홈"
                st.session_state.quiz_total = 0
                st.rerun()
        with col2:
            if st.button("다시 풀기", use_container_width=True):
                st.session_state.quiz_total = 0
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.rerun()

# 시험모드 페이지
elif page == "🎯 시험모드":
    st.title("시험 모드")
    st.markdown("---")
    
    # 기능사별 quiz_data 동적 로드
    current_quiz_data = expand_quiz_data(get_quiz_data(), 900)
    
    if not st.session_state.exam_started:
        st.markdown("""
        ### 시험 규칙
        - **총 문제**: 60문제
        - **난이도**: 섞여있음
        - **점수**: 100점 만점
        - **합격 기준**: 60점 이상
        
        준비가 되셨으면 '시험 시작' 버튼을 클릭하세요!
        """)
        
        if st.button("시험 시작", use_container_width=True, type="primary"):
            st.session_state.exam_started = True
            st.session_state.exam_index = 0
            st.session_state.exam_score = 0
            st.session_state.exam_score_marked = False
            st.session_state.exam_result_saved = False
            st.session_state.exam_wrong_answers = []
            
            # ✅ 60개 문제 랜덤으로 선택 (중복 제거)
            all_questions = []
            seen_questions = set()  # 이미 본 문제를 추적
            
            for theory in current_quiz_data.keys():
                for difficulty in ["쉬움", "보통", "어려움"]:
                    for q in current_quiz_data[theory][difficulty]:
                        question_text = q['question']
                        # 같은 question 텍스트가 없으면 추가
                        if question_text not in seen_questions:
                            all_questions.append(q)
                            seen_questions.add(question_text)
            
            # 최소 60개 문제가 있는지 확인
            if len(all_questions) >= 60:
                st.session_state.exam_questions = random.sample(all_questions, 60)
            else:
                st.session_state.exam_questions = all_questions
            st.rerun()
    
    elif st.session_state.exam_index < 60:
        q = st.session_state.exam_questions[st.session_state.exam_index]
        
        # 진도바
        progress = st.session_state.exam_index / 60
        st.progress(progress)
        st.markdown(f"**진도**: {st.session_state.exam_index + 1} / 60문제")
        
        st.markdown(f"### {q['question']}")
        
        # 라디오 버튼
        ans = st.radio("정답 선택:", q['options'], key=f"exam_q{st.session_state.exam_index}")
        
        # 선택 후 즉시 정답 확인 및 다음
        if st.button("다음", use_container_width=True):
            idx = q['options'].index(ans)
            if idx == q['correct']:
                if not st.session_state.exam_score_marked:
                    st.session_state.exam_score += 1
                    st.session_state.exam_score_marked = True
            else:
                # ✅ 기능사별로 오답 기록
                st.session_state.exam_wrong_answers[st.session_state.selected_certification].append({
                    "theory": "문제",
                    "question": q['question'],
                    "options": q['options'],
                    "user_answer": ans,
                    "correct_answer": q['options'][q['correct']],
                    "explanation": q['explanation']
                })
            
            st.session_state.exam_index += 1
            st.session_state.exam_score_marked = False
            st.rerun()
    
    else:
        # 시험 결과
        final_score = (st.session_state.exam_score / 60) * 100
        
        if not st.session_state.exam_result_saved:
            exam_result = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "score": final_score,
                "correct": st.session_state.exam_score,
                "passed": final_score >= 60,
                "wrong_count": len(st.session_state.exam_wrong_answers[st.session_state.selected_certification])
            }
            # ✅ 기능사별로 시험 결과 저장
            st.session_state.exam_history[st.session_state.selected_certification].append(exam_result)
            st.session_state.exam_result_saved = True
        
        st.markdown(f"### 시험 완료!")
        st.markdown(f"**최종 점수**: {final_score:.1f} / 100점")
        st.markdown(f"**정답**: {st.session_state.exam_score} / 60문제")
        
        st.markdown("---")
        
        if final_score >= 60:
            st.success(f"합격! ({final_score:.1f}점)")
            st.balloons()
        else:
            st.error(f"불합격 ({final_score:.1f}점)")
            # 불합격 시 "떨" 표시 - 다양한 효과가 있는 애니메이션
            st.markdown("""
            <style>
            @keyframes zoomShake {
                0% {
                    transform: scale(0.1) rotate(0deg);
                    opacity: 0;
                    text-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
                }
                10% {
                    transform: scale(0.3) rotate(-2deg);
                    opacity: 0.7;
                }
                20% {
                    transform: scale(0.5) rotate(2deg);
                    opacity: 0.8;
                }
                30% {
                    transform: scale(0.7) rotate(-1deg);
                    opacity: 0.9;
                }
                40% {
                    transform: scale(0.85) rotate(1deg);
                    opacity: 1;
                }
                50% {
                    transform: scale(1) rotate(-0.5deg);
                    opacity: 1;
                    text-shadow: 0 0 20px rgba(255, 68, 68, 1), 0 0 40px rgba(255, 100, 100, 0.8);
                }
                60% {
                    transform: scale(1.05) rotate(0.5deg);
                    opacity: 1;
                    text-shadow: 0 0 20px rgba(255, 68, 68, 1), 0 0 40px rgba(255, 100, 100, 0.8);
                }
                70% {
                    transform: scale(1) rotate(-0.3deg);
                    opacity: 1;
                }
                80% {
                    transform: scale(1.02) rotate(0.3deg);
                    opacity: 1;
                }
                100% {
                    transform: scale(1) rotate(0deg);
                    opacity: 1;
                    text-shadow: 0 0 15px rgba(255, 68, 68, 0.8), 0 0 30px rgba(255, 100, 100, 0.6);
                }
            }
            
            .tteol-animation {
                text-align: center;
                font-size: 200px;
                font-weight: 900;
                color: #FF4444;
                margin: 30px 0;
                animation: zoomShake 2s ease-out forwards;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: 'Gowun Dodum', sans-serif;
            }
            </style>
            <div class='tteol-animation'>
                떨
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("오답노트 보기", use_container_width=True):
                st.session_state.current_page = "🗒️ 오답노트"
                st.rerun()
        with col2:
            if st.button("시험 초기화", use_container_width=True):
                st.session_state.exam_started = False
                st.session_state.exam_index = 0
                st.session_state.exam_score = 0
                st.session_state.exam_result_saved = False
                st.rerun()

# 오답노트 페이지
elif page == "🗒️ 오답노트":
    st.title("오답 노트")
    st.markdown("---")
    
    # ✅ 현재 기능사의 오답만 표시
    current_wrong_answers = st.session_state.exam_wrong_answers[st.session_state.selected_certification]
    
    if not current_wrong_answers:
        st.info("오답이 없습니다!")
    else:
        st.markdown(f"### 오답: {len(current_wrong_answers)}개")
        
        for idx, wrong in enumerate(current_wrong_answers, 1):
            with st.expander(f"문제 {idx}: {wrong['question'][:50]}...", expanded=False):
                st.markdown(f"**문제**: {wrong['question']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**선택한 답**: {wrong['user_answer']}")
                with col2:
                    st.markdown(f"**정답**: {wrong['correct_answer']}")
                
                st.markdown(f"**설명**:")
                st.markdown(wrong['explanation'])
        
        st.markdown("---")
        if st.button("오답노트 삭제", use_container_width=True, type="secondary"):
            st.session_state.exam_wrong_answers[st.session_state.selected_certification] = []
            st.rerun()

# 시험결과 페이지
elif page == "📊 시험결과":
    st.title("시험 결과")
    st.markdown("---")
    
    # ✅ 현재 기능사의 시험 결과만 표시
    current_exam_history = st.session_state.exam_history[st.session_state.selected_certification]
    
    if not current_exam_history:
        st.info("아직 시험을 풀지 않았습니다!")
    else:
        st.markdown(f"### 시험 기록: {len(current_exam_history)}회")
        st.markdown("---")
        
        # 통계
        total = len(current_exam_history)
        passed = sum(1 for r in current_exam_history if r['passed'])
        failed = total - passed
        avg_score = sum(r['score'] for r in current_exam_history) / total
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("총 시험 횟수", total)
        with col2:
            st.metric("합격", f"{passed}회")
        with col3:
            st.metric("불합격", f"{failed}회")
        with col4:
            st.metric("평균 점수", f"{avg_score:.1f}점")
        
        st.markdown("---")
        st.markdown("### 상세 기록")
        
        for result in reversed(current_exam_history):
            status = "합격" if result['passed'] else "불합격"
            st.markdown(f"**{result['date']}** - {result['score']:.1f}점 ({result['correct']}/60) - {status}")
        
        st.markdown("---")
        if st.button("모든 시험 기록 삭제", use_container_width=True, type="secondary"):
            st.session_state.exam_history = []
            st.rerun()

# 실습 시뮬레이션 페이지
elif page == "🛠️ 실습":
    run_upgraded_simulator_v2()

# 학습 진도 페이지
elif page == "📈 진도":
    show_learning_progress()

# 학습 목표 페이지
elif page == "💡 목표":
    show_learning_goals()

# 약점 분석 페이지
elif page == "📊 분석":
    show_weakness_analysis()
