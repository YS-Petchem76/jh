# 🎓 공조냉동기계기능사 시험 플랫폼

2014-2020 기출 문제 기반 온라인 CBT 시험 플랫폼

## 🌟 주요 기능

- **📝 필기 시험** - 2014-2020 기출 문제 (객관식)
- **✍️ 실기 필답형** - 주관식 단답형 문제 + 자동 채점
- **🛠️ 실기 시뮬레이션** - 동관 절단/플레어링 실습
- **📊 점수 분석** - 과목별 약점 분석 및 오답노트
- **🎨 현대적 디자인** - 세련된 UI/UX

## 📋 시스템 요구사항

- Python 3.8+
- Flask 2.3.0
- 최신 웹 브라우저 (Chrome, Firefox, Safari, Edge)

## 🚀 설치 및 실행

### 1단계: 코드 다운로드
```bash
git clone https://github.com/YOUR_USERNAME/hvac-exam-platform.git
cd hvac-exam-platform
```

### 2단계: 가상환경 생성
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# 또는
source .venv/bin/activate  # Mac/Linux
```

### 3단계: 의존성 설치
```bash
pip install -r requirements.txt
```

### 4단계: 앱 실행
```bash
python app.py
```

### 5단계: 브라우저에서 접속
- 로컬: http://localhost:5000
- 같은 네트워크: http://YOUR_PC_IP:5000

## 📄 페이지 구조

| URL | 설명 |
|-----|------|
| `/` | 홈페이지 (시작하기) |
| `/menu` | 시험 메뉴 선택 |
| `/exam/<exam_type>/<year>` | 시험 응시 |

## 🧪 시험 종류

- **WRITTEN**: 필기 시험 (객관식 60문제)
- **PRACTICAL_WRITTEN**: 실기 필답형 (주관식 8문제)
- **PRACTICAL_WORK**: 실기 시뮬레이션 (8개 작업)

## 📊 주요 파일

- `app.py` - Flask 메인 애플리케이션
- `requirements.txt` - Python 의존성
- `.gitignore` - Git 제외 파일

## 🎯 학습 권장 순서

1. 필기 시험 (WRITTEN) - 이론 학습
2. 실기 필답형 (PRACTICAL_WRITTEN) - 실기 이론
3. 실기 시뮬레이션 (PRACTICAL_WORK) - 실습

## 🔧 네트워크 공유 설정

같은 네트워크에서 다른 사람이 접속하려면:

1. `app.py`에서 다음 줄을 수정:
   ```python
   app.run(host='0.0.0.0', port=5000, debug=True)
   ```

2. Windows 방화벽에서 5000 포트 허용

3. 같은 네트워크의 다른 PC에서 접속:
   ```
   http://YOUR_PC_IP:5000
   ```

## 📝 라이선스

MIT License

## 👨‍💻 기여

Pull Request는 언제든 환영합니다!

│   └── generate_quiz.py         # 일회용 도구
└── 📁 __pycache__/              # Python 캐시
```

## 🚀 실행 방법

### 1단계: 의존성 설치
```bash
pip install -r requirements.txt
```

### 2단계: Streamlit 앱 실행
```bash
streamlit run app.py
```

### 3단계: 브라우저 접속
```
http://localhost:8501
```

## 📚 주요 기능

### 🎮 메인 메뉴 (10개)
1. **🏠 홈** - 앱 소개 및 기능 개요
2. **📖 이론** - 9개 주제별 학습 콘텐츠
3. **✏️ 문제풀기** - 난이도별 900개 문제
4. **🛠️ 실습** - 하이브리드 3D+2D 시뮬레이터 ⭐
5. **🎯 시험모드** - 60문제 모의고사
6. **📊 시험결과** - 성적 통계 & 기록
7. **🗒️ 오답노트** - 오답 정리
8. **📈 진도** - 학습 진도 추적
9. **💡 목표** - 학습 계획 수립
10. **📊 분석** - 약점 분석

### 🛠️ 실습 시뮬레이터 (4탭)
1. **🎮 3D 시뮬레이션** - Three.js 기반
   - 7가지 작업 시뮬레이션
   - 실시간 3D 객체 렌더링
   - 인벤토리 관리

2. **📊 2D 학습** - Streamlit UI
   - 라디오 기반 작업 선택
   - 슬라이더로 파라미터 조절
   - 진행 애니메이션

3. **📚 이론** - 교육 콘텐츠
   - 동관 자르기 이론
   - 파이프 드릴링 이론
   - 황동용접 이론

4. **🏆 성취도** - 진도 추적
   - 7개 마일스톤 추적
   - 통계 데이터 표시

## 🔧 기술 스택

- **Frontend**: Streamlit 1.39.0
- **3D Graphics**: Three.js r128
- **Backend**: Python 3.x
- **Image Processing**: PIL/Pillow
- **Rendering**: HTML5 Canvas

## 📦 의존성

```
streamlit==1.39.0
streamlit-drawable-canvas==0.9.3
```

## 🎯 학습 목표

- ✅ 냉동 사이클의 기본 원리 이해
- ✅ 냉동 장비의 구조 및 기능 파악
- ✅ 실습을 통한 실무 능력 배양
- ✅ 자격증 취득 준비

## 📝 파일 역할

| 파일 | 용도 | 상태 |
|------|------|------|
| app.py | 메인 Streamlit 앱 | ✅ 활성 |
| upgraded_simulator.py | 3D+2D 하이브리드 시뮬레이터 | ✅ 활성 |
| learning_progress.py | 진도 추적 모듈 | ✅ 활성 |
| new_quiz_data.py | 퀴즈 데이터 | ✅ 필수 |
| environment_quiz_data.py | 환경 퀴즈 | ✅ 선택 |
| hvac_practice_3d.html | Three.js 3D 환경 | ✅ 필수 |
| requirements.txt | 의존성 | ✅ 필수 |

## ⚙️ 설정

### Streamlit 설정 (.streamlit/config.toml)
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[logger]
level = "info"
```

## 🔐 보안

- 로컬 실행만 지원
- 세션 기반 데이터 관리
- HTTPS 미지원 (로컬 개발용)

## 📞 지원

문제 발생 시:
1. `.streamlit/config.toml` 재설정
2. `.venv` 재생성
3. `pip install --upgrade streamlit`

## 📄 라이선스

교육용 자료

---

**개발일**: 2026-08-27  
**버전**: 1.0.0 (안정 버전)
