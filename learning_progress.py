"""
학습 진도 추적 및 통계 모듈
"""

import streamlit as st
from datetime import datetime
import json

# ============================================================
# 학습 진도 추적
# ============================================================
def init_progress_tracking():
    """학습 진도 추적 초기화"""
    if "learning_progress" not in st.session_state:
        st.session_state.learning_progress = {
            "theory_completed": [],
            "practice_completed": [],
            "exam_completed": 0,
            "total_study_time": 0,
            "last_study_date": None,
            "study_streak": 0
        }
    
    if "daily_study_log" not in st.session_state:
        st.session_state.daily_study_log = {}

def log_learning_activity(activity_type, details):
    """학습 활동 기록"""
    init_progress_tracking()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    if activity_type == "theory":
        if details not in st.session_state.learning_progress["theory_completed"]:
            st.session_state.learning_progress["theory_completed"].append(details)
    
    elif activity_type == "practice":
        if details not in st.session_state.learning_progress["practice_completed"]:
            st.session_state.learning_progress["practice_completed"].append(details)
    
    elif activity_type == "exam":
        st.session_state.learning_progress["exam_completed"] += 1
    
    # 일일 기록 업데이트
    if today not in st.session_state.daily_study_log:
        st.session_state.daily_study_log[today] = {"activities": 0, "duration": 0}
    
    st.session_state.daily_study_log[today]["activities"] += 1

def show_learning_progress():
    """학습 진도 표시"""
    st.title("📈 학습 진도")
    st.markdown("---")
    
    init_progress_tracking()
    
    progress = st.session_state.learning_progress
    
    # 통계 카드
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("완료한 이론", len(progress["theory_completed"]))
    
    with col2:
        st.metric("완료한 실습", len(progress["practice_completed"]))
    
    with col3:
        st.metric("본 시험", progress["exam_completed"])
    
    with col4:
        total_days = len(st.session_state.daily_study_log)
        st.metric("학습 일수", total_days)
    
    st.markdown("---")
    
    # 진도 바
    st.subheader("🎯 학습 목표 진도")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**이론 학습 진도**")
        theory_progress = len(progress["theory_completed"]) / 9
        st.progress(min(theory_progress, 1.0))
        st.write(f"{len(progress['theory_completed'])} / 9 주제")
    
    with col2:
        st.write("**시험 응시 목표**")
        exam_progress = progress["exam_completed"] / 5
        st.progress(min(exam_progress, 1.0))
        st.write(f"{progress['exam_completed']} / 5회")
    
    st.markdown("---")
    
    # 완료한 항목 표시
    st.subheader("✅ 완료한 항목")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**완료한 이론**")
        if progress["theory_completed"]:
            for theory in progress["theory_completed"]:
                st.write(f"✓ {theory}")
        else:
            st.info("아직 완료한 이론이 없습니다.")
    
    with col2:
        st.write("**완료한 실습**")
        if progress["practice_completed"]:
            for practice in progress["practice_completed"]:
                st.write(f"✓ {practice}")
        else:
            st.info("아직 완료한 실습이 없습니다.")
    
    st.markdown("---")
    
    # 일일 학습 히스토리
    st.subheader("📅 일일 학습 기록")
    
    if st.session_state.daily_study_log:
        for date in sorted(st.session_state.daily_study_log.keys(), reverse=True)[:7]:  # 최근 7일
            activities = st.session_state.daily_study_log[date]["activities"]
            st.write(f"**{date}**: {activities}개 활동 완료")
    else:
        st.info("아직 학습 기록이 없습니다.")
    
    st.markdown("---")
    
    # 추천 학습 계획
    st.subheader("💡 추천 학습 계획")
    
    if len(progress["theory_completed"]) < 9:
        st.info("📚 이론 학습을 더 진행해보세요!")
    
    if progress["exam_completed"] < 3:
        st.info("📝 시험모드로 실제 시험을 연습해보세요!")
    
    if len(progress["practice_completed"]) < 5:
        st.info("🛠️ 실습 시뮬레이션으로 실무 스킬을 키워보세요!")

# ============================================================
# 학습 목표 설정
# ============================================================
def show_learning_goals():
    """학습 목표 설정 페이지"""
    st.title("🎯 학습 목표")
    st.markdown("---")
    
    st.subheader("월간 학습 목표")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        theory_goal = st.number_input("완료할 이론 수", 0, 9, 5)
    
    with col2:
        practice_goal = st.number_input("완료할 실습 수", 0, 10, 5)
    
    with col3:
        exam_goal = st.number_input("응시할 시험 수", 0, 20, 5)
    
    st.markdown("---")
    
    if st.button("목표 저장"):
        if "learning_goals" not in st.session_state:
            st.session_state.learning_goals = {}
        
        st.session_state.learning_goals = {
            "theory": theory_goal,
            "practice": practice_goal,
            "exam": exam_goal,
            "set_date": datetime.now().isoformat()
        }
        st.success("목표가 저장되었습니다!")
    
    st.markdown("---")
    
    st.subheader("목표 달성 현황")
    
    if "learning_goals" in st.session_state:
        goals = st.session_state.learning_goals
        progress = st.session_state.learning_progress if "learning_progress" in st.session_state else None
        
        if progress:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                theory_rate = (len(progress["theory_completed"]) / goals["theory"] * 100) if goals["theory"] > 0 else 0
                st.metric(f"이론 진도", f"{theory_rate:.0f}%")
                st.progress(min(theory_rate / 100, 1.0))
            
            with col2:
                practice_rate = (len(progress["practice_completed"]) / goals["practice"] * 100) if goals["practice"] > 0 else 0
                st.metric(f"실습 진도", f"{practice_rate:.0f}%")
                st.progress(min(practice_rate / 100, 1.0))
            
            with col3:
                exam_rate = (progress["exam_completed"] / goals["exam"] * 100) if goals["exam"] > 0 else 0
                st.metric(f"시험 진도", f"{exam_rate:.0f}%")
                st.progress(min(exam_rate / 100, 1.0))
    else:
        st.info("먼저 목표를 설정해주세요!")

# ============================================================
# 약점 분석
# ============================================================
def show_weakness_analysis():
    """약점 분석 페이지"""
    st.title("📊 약점 분석")
    st.markdown("---")
    
    if "exam_wrong_answers" not in st.session_state:
        st.info("아직 틀린 문제가 없습니다!")
        return
    
    all_wrong = st.session_state.exam_wrong_answers.get(st.session_state.selected_certification, [])
    
    if not all_wrong:
        st.success("완벽합니다! 틀린 문제가 없어요!")
        return
    
    st.subheader(f"틀린 문제: {len(all_wrong)}개")
    
    # 주제별 오답 분석
    topic_wrong_count = {}
    for wrong in all_wrong:
        topic = wrong.get("theory", "기타")
        if topic not in topic_wrong_count:
            topic_wrong_count[topic] = 0
        topic_wrong_count[topic] += 1
    
    st.markdown("---")
    st.subheader("주제별 오답률")
    
    for topic, count in sorted(topic_wrong_count.items(), key=lambda x: x[1], reverse=True):
        st.write(f"**{topic}**: {count}개")
        st.progress(count / len(all_wrong))
    
    st.markdown("---")
    
    # 강화 학습 제안
    st.subheader("💪 강화 학습 제안")
    
    if topic_wrong_count:
        worst_topic = max(topic_wrong_count.items(), key=lambda x: x[1])[0]
        st.info(f"📚 '{worst_topic}' 주제의 이론을 다시 공부한 후 문제를 풀어보세요!")
    
    # 오답 다시 풀기
    st.markdown("---")
    st.subheader("🔄 오답 복습")
    
    if st.button("오답 문제 다시 풀기"):
        st.session_state.current_page = "🗒️ 오답노트"
        st.rerun()
