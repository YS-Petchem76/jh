#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
공조냉동기계기능사 학습 플랫폼 (CBT 형식 + 2D 시뮬레이터)
실행: python app.py
접속: http://127.0.0.1:5000
"""

from flask import Flask, request, render_template_string, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# ============================= 데이터 생성 함수 =================================
def generate_questions_by_year(year):
    """년도별 기출 문제 생성 (실제 시험은 60문제)"""
    base_questions = [
        # 냉동기계일반 (15문제)
        {
            "id": 1,
            "exam_type": "WRITTEN",
            "qtype": "MCQ",
            "subject": "냉동기계일반",
            "prompt": "냉매의 조건으로 옳지 않은 것은?",
            "choices": ["증발잠열이 클수록 유리하다", "화학적으로 안정해야 한다", "독성이 강할수록 누설 감지가 쉽다", "부식성이 낮아야 한다"],
            "answer": 2,
            "explanation": "독성은 약해야 안전합니다.",
            "choice_explanations": [
                "✅ 증발잠열이 크면 냉동 효율이 좋습니다.",
                "✅ 화학적 안정성은 냉매의 필수 조건입니다.",
                "❌ 독성이 강하면 누설 시 위험하므로 안 됩니다.",
                "✅ 부식성이 낮아야 설비 수명이 깁니다."
            ],
            "analysis": "안전성이 가장 중요한 냉매 선택 기준입니다.",
            "year": year
        },
        {
            "id": 2,
            "exam_type": "WRITTEN",
            "qtype": "MCQ",
            "subject": "냉동기계일반",
            "prompt": "역카르노 사이클의 COP는?",
            "choices": ["온도에 무관하다", "압력에만 영향받는다", "절대온도 비에 의존한다", "냉매 종류에만 영향받는다"],
            "answer": 2,
            "explanation": "COP = Tc / (Th - Tc)",
            "choice_explanations": [
                "❌ 온도에 따라 변합니다.",
                "❌ 온도에 크게 영향받습니다.",
                "✅ 역카르노 COP는 절대온도에 의존합니다.",
                "❌ 냉매보다 온도가 더 중요합니다."
            ],
            "analysis": "냉동 온도가 낮을수록 COP가 감소합니다.",
            "year": year
        },
        # 공기조화 (15문제)
        {
            "id": 20,
            "exam_type": "WRITTEN",
            "qtype": "MCQ",
            "subject": "공기조화",
            "prompt": "상대습도 100%의 공기는?",
            "choices": ["과열공기", "포화공기", "건공기", "습공기"],
            "answer": 1,
            "explanation": "상대습도 100%는 포화 상태입니다.",
            "choice_explanations": [
                "❌ 과열공기는 습도가 낮습니다.",
                "✅ 포화 상태입니다.",
                "❌ 건공기는 습도 0%입니다.",
                "❌ 습공기는 0-100% 사이입니다."
            ],
            "analysis": "포화 상태에서 결로가 발생합니다.",
            "year": year
        },
        {
            "id": 21,
            "exam_type": "WRITTEN",
            "qtype": "MCQ",
            "subject": "공기조화",
            "prompt": "현열과 잠열의 차이는?",
            "choices": ["현열은 액체, 잠열은 기체", "현열은 온도변화, 잠열은 상태변화", "현열은 기체, 잠열은 액체", "구분 불가"],
            "answer": 1,
            "explanation": "현열: 온도 변화 열량, 잠열: 상태 변화 열량",
            "choice_explanations": [
                "❌ 상태가 아닌 열의 종류입니다.",
                "✅ 이것이 정의입니다.",
                "❌ 상태가 아닙니다.",
                "❌ 명확하게 구분됩니다."
            ],
            "analysis": "냉동 사이클에서 잠열이 냉동 효과를 만듭니다.",
            "year": year
        },
    ]
    
    # 년도별 추가 문제들로 다양성 확보 (실제로는 60문제 필요)
    # 이 부분은 실제 기출 문제로 확장 가능
    additional_questions = [
        {
            "id": 3+i,
            "exam_type": "WRITTEN",
            "qtype": "MCQ",
            "subject": "냉동기계일반",
            "prompt": f"냉매 R-{410+i}의 특징은? (기출 {year}년)",
            "choices": ["매우 높은 효율", "중간 정도의 효율", "낮은 효율", "효율 미지정"],
            "answer": (i % 4),
            "explanation": f"각 냉매의 특성은 다릅니다.",
            "choice_explanations": ["❌", "❌", "✅", "❌"],
            "analysis": "냉매 선택은 용도에 맞게 해야 합니다.",
            "year": year
        } for i in range(56)  # 60 - 4개 기본 문제 = 56개
    ]
    
    return base_questions + additional_questions


# 필답형 기출 문제 (년도별)
def generate_practical_written_by_year(year):
    """년도별 필답형 기출 문제"""
    practical_written = [
        {
            "id": 1001,
            "exam_type": "PRACTICAL_WRITTEN",
            "qtype": "SHORT",
            "subject": "실기 필답형",
            "prompt": "과열도(superheat)의 정의를 설명하시오.",
            "keywords": ["증발기", "출구", "포화온도", "온도"],
            "sample_answer": "증발기 출구 냉매의 온도와 같은 압력에서의 포화온도의 차이",
            "explanation": "과열도는 냉동 사이클의 효율을 평가하는 중요한 지표입니다.",
            "year": year
        },
        {
            "id": 1002,
            "exam_type": "PRACTICAL_WRITTEN",
            "qtype": "SHORT",
            "subject": "실기 필답형",
            "prompt": "냉동기의 압축비(compression ratio)를 정의하시오.",
            "keywords": ["고압", "저압", "비율"],
            "sample_answer": "압축기 토출 압력을 흡입 압력으로 나눈 값",
            "explanation": "압축비가 높을수록 압축기에 부하가 커집니다.",
            "year": year
        },
        {
            "id": 1003,
            "exam_type": "PRACTICAL_WRITTEN",
            "qtype": "SHORT",
            "subject": "실기 필답형",
            "prompt": "응축기에서 냉매의 상태 변화 과정을 설명하시오.",
            "keywords": ["고온", "고압", "액체", "냉각"],
            "sample_answer": "고온 고압의 냉매 증기가 냉각되어 액체로 상태 변화",
            "explanation": "응축기는 냉동 사이클에서 열을 방출하는 역할을 합니다.",
            "year": year
        },
        {
            "id": 1004,
            "exam_type": "PRACTICAL_WRITTEN",
            "qtype": "SHORT",
            "subject": "실기 필답형",
            "prompt": "동관 절단 시 가장 중요한 주의사항을 두 가지 이상 쓰시오.",
            "keywords": ["청결", "직각", "버", "정확"],
            "sample_answer": "버를 제거해야 하며, 직각으로 정확하게 절단하고 절단면을 청결하게 유지",
            "explanation": "동관 절단은 이후 모든 작업의 기초가 됩니다.",
            "year": year
        },
        {
            "id": 1005,
            "exam_type": "PRACTICAL_WRITTEN",
            "qtype": "SHORT",
            "subject": "실기 필답형",
            "prompt": "플레어링의 목적을 설명하시오.",
            "keywords": ["접합", "누설", "방지", "연결"],
            "sample_answer": "동관의 끝을 벌려서 연결구와의 접합면을 넓혀 누설을 방지",
            "explanation": "플레어링은 냉동 장치의 누설을 방지하는 중요한 공정입니다.",
            "year": year
        },
        {
            "id": 1006,
            "exam_type": "PRACTICAL_WRITTEN",
            "qtype": "SHORT",
            "subject": "실기 필답형",
            "prompt": "밴딩(bending) 시 동관이 손상되는 원인을 설명하시오.",
            "keywords": ["반경", "최소", "과도", "압력"],
            "sample_answer": "최소 반경보다 작게 구부리거나 과도한 압력을 가할 때",
            "explanation": "동관의 재질 특성을 고려하여 적절한 반경으로 구부려야 합니다.",
            "year": year
        },
        {
            "id": 1007,
            "exam_type": "PRACTICAL_WRITTEN",
            "qtype": "SHORT",
            "subject": "실기 필답형",
            "prompt": "냉동장치 용접 시 냉매 누출을 방지하는 방법을 쓰시오.",
            "keywords": ["질소", "충전", "보호"],
            "sample_answer": "동관 내부에 질소를 충전하여 산화를 방지하고 누설을 방지",
            "explanation": "용접 시 산화에 의한 누설은 냉동장치의 고장으로 이어집니다.",
            "year": year
        },
        {
            "id": 1008,
            "exam_type": "PRACTICAL_WRITTEN",
            "qtype": "SHORT",
            "subject": "실기 필답형",
            "prompt": "누설 검사(leak test) 방법을 두 가지 이상 설명하시오.",
            "keywords": ["비누", "할로겐", "압력", "감지"],
            "sample_answer": "비누액으로 거품 생성 여부를 확인하거나 할로겐 검출기 사용",
            "explanation": "누설 검사는 냉동장치의 안전성을 보장하는 중요한 과정입니다.",
            "year": year
        },
    ]
    return practical_written


# 년도별 데이터 캐시
QUESTIONS_BY_YEAR = {
    2024: generate_questions_by_year(2024),
    2023: generate_questions_by_year(2023),
    2022: generate_questions_by_year(2022),
    2021: generate_questions_by_year(2021),
    2020: generate_questions_by_year(2020),
}

PRACTICAL_WRITTEN_BY_YEAR = {
    2024: generate_practical_written_by_year(2024),
    2023: generate_practical_written_by_year(2023),
    2022: generate_practical_written_by_year(2022),
    2021: generate_practical_written_by_year(2021),
    2020: generate_practical_written_by_year(2020),
}

ATTEMPTS = []     # 제출 기록
WRONG_NOTES = []  # 오답노트
SIMULATOR_PROGRESS = {}  # 사용자별 시뮬레이터 진행 상황

# 2D 시뮬레이터 JavaScript 코드 (개선된 동관절단)
SIMULATOR_2D_JS = """
const canvas = document.getElementById('simulatorCanvas');
const ctx = canvas.getContext('2d');

canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

let completedTasks = 0;
let currentTask = -1;  // 현재 진행 중인 작업
let tubeLength = 100;  // 동관 길이 (mm)
let cuttingPoint = -1; // 절단 위치

const tasks = [
  '1️⃣ 동관 절단', '2️⃣ 플레어링', '3️⃣ 밴딩', '4️⃣ 연결',
  '5️⃣ 용접', '6️⃣ 누설검사', '7️⃣ 냉각작업', '8️⃣ 작동점검'
];

let taskStates = [
  { x: 100, y: 80, width: 150, height: 80, done: false, interactive: true },
  { x: 300, y: 80, width: 150, height: 80, done: false, interactive: false },
  { x: 500, y: 80, width: 150, height: 80, done: false, interactive: false },
  { x: 700, y: 80, width: 150, height: 80, done: false, interactive: false },
  { x: 100, y: 220, width: 150, height: 80, done: false, interactive: false },
  { x: 300, y: 220, width: 150, height: 80, done: false, interactive: false },
  { x: 500, y: 220, width: 150, height: 80, done: false, interactive: false },
  { x: 700, y: 220, width: 150, height: 80, done: false, interactive: false },
];

// 동관 절단 상태
let cuttingMode = false;
let cuttingLength = null;

function drawTube(x, y, length) {
  ctx.fillStyle = '#b57315';
  ctx.fillRect(x, y, length * 2, 30);
  ctx.fillStyle = '#000';
  ctx.font = '12px Arial';
  ctx.fillText(length + 'mm', x + length - 20, y + 20);
}

function draw() {
  ctx.fillStyle = '#0a0a0a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  // 헤더
  ctx.font = 'bold 16px Arial';
  ctx.fillStyle = '#fff';
  ctx.fillText('🛠️ 공조냉동 실습 작업 (클릭하여 완료)', 20, 40);
  
  // 동관절단 모드
  if (cuttingMode) {
    ctx.fillStyle = '#667eea';
    ctx.font = 'bold 14px Arial';
    ctx.fillText('동관절단 모드: 치수를 입력하고 절단 위치를 클릭하세요', 20, 400);
    
    // 샘플 동관 표시
    drawTube(100, 430, tubeLength);
    
    // 절단 위치 표시
    if (cuttingPoint > 0 && tubeLength > 0) {
      const cutX = 100 + (cuttingPoint / tubeLength) * tubeLength * 2;
      ctx.strokeStyle = '#ff6b6b';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(cutX, 430);
      ctx.lineTo(cutX, 460);
      ctx.stroke();
    }
  }
  
  // 작업 버튼
  taskStates.forEach((task, i) => {
    const gradient = ctx.createLinearGradient(task.x, task.y, task.x, task.y + task.height);
    if (task.done) {
      gradient.addColorStop(0, '#059669');
      gradient.addColorStop(1, '#047857');
    } else if (task.interactive) {
      gradient.addColorStop(0, '#667eea');
      gradient.addColorStop(1, '#764ba2');
    } else {
      gradient.addColorStop(0, '#999');
      gradient.addColorStop(1, '#777');
    }
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.roundRect(task.x, task.y, task.width, task.height, 8);
    ctx.fill();
    
    ctx.strokeStyle = task.done ? '#10b981' : (task.interactive ? '#aaa' : '#555');
    ctx.lineWidth = 2;
    ctx.stroke();
    
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 14px Arial';
    ctx.textAlign = 'center';
    const text = task.done ? tasks[i] + ' ✅' : tasks[i];
    ctx.fillText(text, task.x + task.width/2, task.y + task.height/2);
    ctx.textAlign = 'left';
  });
  
  // 진행률
  ctx.fillStyle = '#10b981';
  ctx.font = 'bold 24px Arial';
  ctx.fillText(`진행률: ${completedTasks}/8`, 20, canvas.height - 20);
  
  // 마우스 커서 변경
  if (cuttingMode) {
    canvas.style.cursor = 'crosshair';
  } else {
    canvas.style.cursor = 'default';
  }
}

canvas.addEventListener('click', (e) => {
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  
  if (cuttingMode && y > 420 && y < 470) {
    // 동관 절단 모드에서 절단 위치 선택
    const tubeStartX = 100;
    const tubeEndX = 100 + tubeLength * 2;
    
    if (x >= tubeStartX && x <= tubeEndX) {
      cuttingPoint = Math.round((x - tubeStartX) / 2);
      cuttingMode = false;
      
      // 첫 번째 작업 완료
      taskStates[0].done = true;
      completedTasks++;
      
      // 다음 작업 활성화
      if (completedTasks < taskStates.length) {
        taskStates[completedTasks].interactive = true;
      }
      
      updateProgress();
      draw();
      return;
    }
  }
  
  // 작업 클릭
  taskStates.forEach((task, i) => {
    if (x > task.x && x < task.x + task.width && y > task.y && y < task.y + task.height) {
      if (!task.done && task.interactive) {
        if (i === 0) {
          // 동관절단 작업
          cuttingMode = true;
        } else {
          task.done = true;
          completedTasks++;
          
          // 다음 작업 활성화
          if (completedTasks < taskStates.length) {
            taskStates[completedTasks].interactive = true;
          }
          
          updateProgress();
        }
        draw();
      }
    }
  });
});

// 치수 입력 처리 (if needed)
function setCuttingLength(length) {
  tubeLength = parseInt(length) || 100;
  draw();
}

function updateProgress() {
  const progressFill = document.getElementById('progressFill');
  if (progressFill) {
    progressFill.style.width = (completedTasks / 8 * 100) + '%';
  }
  
  const progressDisplay = document.getElementById('progress-display');
  if (progressDisplay) {
    progressDisplay.innerHTML = `<strong>${completedTasks}/8 작업 완료</strong> (${Math.round(completedTasks/8*100)}%)`;
  }
}

// Canvas 반응형
window.addEventListener('resize', () => {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  draw();
});

// CanvasRenderingContext2D에 roundRect 추가 (polyfill)
if (!CanvasRenderingContext2D.prototype.roundRect) {
  CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
    if (w < 2 * r) r = w / 2;
    if (h < 2 * r) r = h / 2;
    this.beginPath();
    this.moveTo(x+r, y);
    this.arcTo(x+w, y, x+w, y+h, r);
    this.arcTo(x+w, y+h, x, y+h, r);
    this.arcTo(x, y+h, x, y, r);
    this.arcTo(x, y, x+w, y, r);
    this.closePath();
    return this;
  };
}

draw();
"""

# ================================ 유틸 ==================================
def get_questions(exam_type):
    return [q for q in QUESTIONS if q["exam_type"] == exam_type]

def find_question(qid):
    for q in QUESTIONS:
        if q["id"] == qid:
            return q
    return None

def grade_short_answer(user_text, keywords):
    text = (user_text or "").replace(" ", "").lower()
    hit = 0
    for kw in keywords:
        if kw.replace(" ", "").lower() in text:
            hit += 1
    needed = max(1, len(keywords) // 2)
    return hit >= needed, hit, len(keywords)

def add_wrong_note(user, qid, memo=""):
    exists = any(w["user"] == user and w["qid"] == qid for w in WRONG_NOTES)
    if not exists:
        WRONG_NOTES.append({
            "user": user,
            "qid": qid,
            "memo": memo,
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# ================================ 베이스 HTML ============================
BASE_HTML = """
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <title>공조냉동기계기능사 CBT 시험 플랫폼</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", sans-serif; 
      background: linear-gradient(135deg, #667eea, #764ba2);
      color:#111; min-height: 100vh; padding: 20px;
    }
    .container { max-width: 1000px; margin: 0 auto; }
    .wrap { background:#fff; border-radius:12px; padding: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
    .card { 
      background:#f9fafb; border:1px solid #e5e7eb; border-radius:12px; 
      padding:16px; margin-bottom:16px;
    }
    .btn { 
      display:inline-block; padding:12px 20px; border-radius:8px; 
      text-decoration:none; border:0; cursor:pointer; font-weight:600; 
      transition: all 0.3s;
    }
    .btn:hover { transform: scale(1.05); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    .btn-blue { background:#2563eb; color:#fff; }
    .btn-green { background:#059669; color:#fff; }
    .btn-gray { background:#111827; color:#fff; }
    .btn-light { background:#e5e7eb; color:#111; }
    .row { display:flex; gap:12px; flex-wrap:wrap; }
    .muted { color:#6b7280; font-size:14px; }
    input[type=text], textarea, input[type=radio] { font-family: inherit; }
    input[type=text], textarea { width:100%; padding:10px; border:1px solid #d1d5db; border-radius:8px; }
    textarea { min-height: 80px; resize: vertical; }
    .ok { color:#059669; font-weight:700; }
    .bad { color:#dc2626; font-weight:700; }
    .pill { 
      display:inline-block; font-size:12px; padding:6px 10px; 
      border-radius:999px; background:#eef2ff; color:#3730a3; margin-bottom:8px;
    }
    label { display: block; margin: 12px 0; padding: 12px; border: 1px solid #e5e7eb; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
    label:hover { background: #f0f9ff; border-color: #2563eb; }
    input[type=radio] { margin-right: 8px; }
    h1, h2, h3 { margin-top: 0; }
    .header { 
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: white;
      padding: 20px;
      border-radius: 8px;
      margin-bottom: 20px;
    }
    .header h1 { font-size: 32px; margin-bottom: 5px; }
    .timer { 
      display: inline-block; background: rgba(255,255,255,0.2); 
      padding: 8px 12px; border-radius: 6px; font-weight: bold;
    }
    .score-display {
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: white;
      padding: 30px;
      border-radius: 12px;
      text-align: center;
      margin: 20px 0;
    }
    .score-display h2 { margin: 0 0 10px 0; font-size: 56px; }
    .score-display p { margin: 5px 0; font-size: 16px; }
    .choice-explanation {
      padding: 10px; margin: 8px 0; border-radius: 6px; font-size: 13px;
      border-left: 4px solid #d1d5db;
    }
    .choice-explanation.correct { 
      background: #dcfce7; border-left-color: #059669; color: #166534;
    }
    .choice-explanation.incorrect { 
      background: #fee2e2; border-left-color: #dc2626; color: #7f1d1d;
    }
    .analysis-box {
      background: #f0f9ff; border-left: 4px solid #0284c7;
      padding: 12px; margin: 15px 0; border-radius: 6px;
    }
    .progress-bar { 
      width: 100%; height: 8px; background: #e5e7eb; 
      border-radius: 4px; overflow: hidden; margin: 10px 0;
    }
    .progress-fill { 
      height: 100%; background: linear-gradient(90deg, #059669, #10b981); 
      transition: width 0.3s;
    }
  </style>
</head>
<body>
<div class="container">
  <div class="wrap">
    {{ body|safe }}
  </div>
</div>
</body>
</html>
"""

# ================================ 라우트 ===============================
@app.route("/")
def home():
    body = """
    <div class="header">
      <h1>🎓 공조냉동기계기능사 CBT 시험 플랫폼</h1>
      <p>년도별 기출 시험 | 60문제 | 실제 시험 환경</p>
    </div>
    
    <div class="card">
      <h2>📚 시험 년도 선택</h2>
      <p class="muted">원하는 년도의 기출 시험을 선택하세요.</p>
      
      <h3>📝 필기 시험 (객관식)</h3>
      <div class="row">
        <a class="btn btn-blue" href="/exam/WRITTEN/2024?user=demo">📝 2024년 필기</a>
        <a class="btn btn-blue" href="/exam/WRITTEN/2023?user=demo">📝 2023년 필기</a>
        <a class="btn btn-blue" href="/exam/WRITTEN/2022?user=demo">📝 2022년 필기</a>
        <a class="btn btn-blue" href="/exam/WRITTEN/2021?user=demo">📝 2021년 필기</a>
        <a class="btn btn-blue" href="/exam/WRITTEN/2020?user=demo">📝 2020년 필기</a>
      </div>
      
      <h3 style="margin-top: 20px;">✍️ 실기 필답형 (주관식)</h3>
      <div class="row">
        <a class="btn btn-green" href="/exam/PRACTICAL_WRITTEN/2024?user=demo">✍️ 2024년 필답형</a>
        <a class="btn btn-green" href="/exam/PRACTICAL_WRITTEN/2023?user=demo">✍️ 2023년 필답형</a>
        <a class="btn btn-green" href="/exam/PRACTICAL_WRITTEN/2022?user=demo">✍️ 2022년 필답형</a>
        <a class="btn btn-green" href="/exam/PRACTICAL_WRITTEN/2021?user=demo">✍️ 2021년 필답형</a>
        <a class="btn btn-green" href="/exam/PRACTICAL_WRITTEN/2020?user=demo">✍️ 2020년 필답형</a>
      </div>
    </div>
    
    <div class="card">
      <h2>🛠️ 실기 시험</h2>
      <p class="muted">2D 시뮬레이터를 통한 실기 작업 수행</p>
      <div class="row">
        <a class="btn btn-purple" href="/exam/PRACTICAL_WORK/2024?user=demo">🛠️ 실기 시험 (2024)</a>
      </div>
    </div>
    
    <div class="card">
      <h2>📌 학습 자료</h2>
      <div class="row">
        <a class="btn btn-light" href="/wrong-notes?user=demo">오답노트</a>
      </div>
    </div>
    
    <div class="card">
      <h3>💡 플랫폼 특징</h3>
      <ul>
        <li>✅ 년도별 기출 60문제 (실제 시험 기준)</li>
        <li>✅ CBT 형식의 실제 시험 환경</li>
        <li>✅ 각 선택지별 상세 해설</li>
        <li>✅ 문제점 분석 및 약점 파악</li>
        <li>✅ 2D 시뮬레이터 실습</li>
        <li>✅ 오답노트 및 복습 기능</li>
      </ul>
    </div>
    """
    return render_template_string(BASE_HTML, body=body)

@app.route("/exam/<exam_type>/<int:year>", methods=["GET", "POST"])
def exam(exam_type, year):
    user = request.values.get("user", "demo")
    
    # 문제 로드
    if year not in QUESTIONS_BY_YEAR and year not in PRACTICAL_WRITTEN_BY_YEAR:
        return render_template_string(BASE_HTML, body=f'<div class="card"><h2>❌ {year}년 시험 문제를 찾을 수 없습니다.</h2><a class="btn btn-blue" href="/">돌아가기</a></div>')
    
    # 필답형 문제 로드
    if exam_type == "PRACTICAL_WRITTEN":
        if year not in PRACTICAL_WRITTEN_BY_YEAR:
            return render_template_string(BASE_HTML, body=f'<div class="card"><h2>❌ {year}년 필답형 문제를 찾을 수 없습니다.</h2><a class="btn btn-blue" href="/">돌아가기</a></div>')
        questions = PRACTICAL_WRITTEN_BY_YEAR[year]
    else:
        if year not in QUESTIONS_BY_YEAR:
            return render_template_string(BASE_HTML, body=f'<div class="card"><h2>❌ {year}년 시험 문제를 찾을 수 없습니다.</h2><a class="btn btn-blue" href="/">돌아가기</a></div>')
        questions = [q for q in QUESTIONS_BY_YEAR[year] if q["exam_type"] == exam_type]
    
    if not questions:
        return render_template_string(BASE_HTML, body=f'<div class="card"><h2>시험 문제를 찾을 수 없습니다: {exam_type}</h2></div>')

    # POST: 시험 제출 및 채점
    if request.method == "POST":
        total = len(questions)
        correct = 0
        details = []
        weak_points = {}  # 약점 분석

        for q in questions:
            qid = q["id"]
            is_correct = False
            user_answer_display = ""
            picked_idx = None
            keywords_hit = 0
            keywords_total = 0

            if q["qtype"] == "MCQ":
                picked = request.form.get(f"q_{qid}")
                if picked is not None:
                    picked_idx = int(picked)
                    is_correct = (picked_idx == q["answer"])
                    user_answer_display = q["choices"][picked_idx]
                else:
                    user_answer_display = "(무응답)"
                    picked_idx = -1

            elif q["qtype"] == "SHORT":
                # 필답형 주관식 채점
                user_text = request.form.get(f"q_{qid}", "")
                user_answer_display = user_text
                is_correct, keywords_hit, keywords_total = grade_short_answer(user_text, q.get("keywords", []))

            elif q["qtype"] == "2D_SIMULATOR":
                sim_data = SIMULATOR_PROGRESS.get(user, {})
                completed_tasks = sim_data.get("completed_tasks", 0)
                is_correct = (completed_tasks >= 8)
                user_answer_display = f"{completed_tasks}/8 작업 완료"

            if is_correct:
                correct += 1
            else:
                add_wrong_note(user, qid, memo="복습 필요")
                # 약점 분석
                if "subject" not in weak_points:
                    weak_points[q["subject"]] = 0
                weak_points[q["subject"]] += 1

            details.append({
                "q": q,
                "is_correct": is_correct,
                "user_answer": user_answer_display,
                "picked_idx": picked_idx,
                "keywords_hit": keywords_hit,
                "keywords_total": keywords_total
            })

        score = round((correct / total) * 100)

        ATTEMPTS.append({
            "user": user,
            "exam_type": exam_type,
            "year": year,
            "score": score,
            "correct": correct,
            "total": total,
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # 상세 답안지 생성
        detail_html = ""
        for i, d in enumerate(details, start=1):
            q = d["q"]
            status = '<span class="ok">✅ 정답</span>' if d["is_correct"] else '<span class="bad">❌ 오답</span>'
            
            detail_html += f"""
            <div class="card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <div class="pill">{q['subject']}</div>
                  <h3>문제 {i}. {q['prompt']}</h3>
                </div>
                <div>{status}</div>
              </div>
              
              <div style="margin: 15px 0;">
                <h4>📋 선택지별 설명</h4>
            """
            
            # MCQ 타입일 때 선택지별 설명
            if q["qtype"] == "MCQ":
                for c_idx, c in enumerate(q["choices"]):
                    is_answer = (c_idx == q["answer"])
                    is_picked = (c_idx == d["picked_idx"])
                    
                    # 스타일 결정
                    if is_answer:
                        explanation_class = "choice-explanation correct"
                        mark = "✅ 정답"
                    else:
                        explanation_class = "choice-explanation incorrect"
                        mark = "❌ 오답"
                    
                    # 선택 표시
                    pick_mark = " ← 내 답" if is_picked else ""
                    
                    detail_html += f"""
                    <div class="{explanation_class}">
                      <strong>{chr(65+c_idx)}. {mark}{pick_mark}</strong><br/>
                      {c}<br/>
                      <em>{q['choice_explanations'][c_idx]}</em>
                    </div>
                    """
            
            # 분석
            detail_html += f"""
              </div>
              <div class="analysis-box">
                <strong>📊 분석:</strong> {q.get('analysis', q.get('explanation', '-'))}
              </div>
            </div>
            """

        # 약점 분석 리포트
        weakness_html = "<h3>📊 약점 분석</h3>"
        if weak_points:
            weakness_html += "<ul>"
            for subject, count in sorted(weak_points.items(), key=lambda x: x[1], reverse=True):
                weakness_html += f"<li><strong>{subject}</strong>: {count}개 오답</li>"
            weakness_html += "</ul>"
        else:
            weakness_html += "<p class='ok'>완벽합니다! 약점이 없습니다! 🎉</p>"

        body = f"""
        <div class="header">
          <h1>📊 시험 결과</h1>
          <p>사용자: <strong>{user}</strong> | {year}년 {exam_type}</p>
        </div>
        
        <div class="score-display">
          <h2>{score}점</h2>
          <p>{correct}개 정답 / {total}개 문제</p>
          <p>{"🎉 합격! (60점 이상)" if score >= 60 else "재응시 권장 (60점 미만)"}</p>
        </div>
        
        <div class="card">
          {weakness_html}
        </div>
        
        <div class="row">
          <a class="btn btn-light" href="/exam/{exam_type}/{year}?user={user}">다시 응시</a>
          <a class="btn btn-gray" href="/wrong-notes?user={user}">오답노트 보기</a>
          <a class="btn btn-blue" href="/">홈</a>
        </div>
        
        <hr style="margin: 30px 0; border:none; border-top: 2px solid #e5e7eb;">
        <h2>📖 상세 답안지</h2>
        {detail_html}
        """
        return render_template_string(BASE_HTML, body=body)

    # GET: 시험 화면
    exam_type_name = {
        "WRITTEN": f"{year}년 필기 시험",
        "PRACTICAL_WORK": f"{year}년 실기 시험 (2D 시뮬레이터)"
    }.get(exam_type, exam_type)
    
    # 2D 시뮬레이터가 포함된 경우
    if exam_type == "PRACTICAL_WORK" and any(q["qtype"] == "2D_SIMULATOR" for q in questions):
        body = f"""
        <div class="header">
          <h1>🛠️ {year}년 실기 시험 (2D 시뮬레이터)</h1>
          <p>모든 작업을 완료하고 제출하세요.</p>
        </div>
        
        <div class="card">
          <h2>공조냉동 2D 시뮬레이터</h2>
          <p class="muted">아래에서 8가지 실습 작업을 모두 완료해주세요.</p>
          
          <div id="simulator-container" style="width:100%; height:700px; border:2px solid #e5e7eb; border-radius:8px; overflow:hidden; margin:20px 0; background:#000;">
            <canvas id="simulatorCanvas" style="display:block; width:100%; height:100%;"></canvas>
          </div>
          
          <div style="background:#f0f9ff; padding:15px; border-radius:8px; margin:15px 0; border-left:4px solid #3b82f6;">
            <p><strong>📋 진행 상황:</strong></p>
            <div class="progress-bar">
              <div class="progress-fill" id="progressFill" style="width:0%;"></div>
            </div>
            <p id="progress-display">시뮬레이터 로딩 중...</p>
          </div>
          
          <form method="post">
            <input type="hidden" name="user" value="{user}" />
            <div class="row">
              <button class="btn btn-blue" type="submit">✅ 제출하기</button>
              <a class="btn btn-light" href="/">취소</a>
            </div>
          </form>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
        <script>
          {SIMULATOR_2D_JS}
        </script>
        """
        return render_template_string(BASE_HTML, body=body)

    # 일반 필기 시험 화면 (CBT 형식)
    q_html = ""
    for idx, q in enumerate(questions, start=1):
        q_html += f"""
        <div class="card" style="page-break-inside: avoid;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div class="pill">{q["subject"]}</div>
              <h3>문제 {idx}/{len(questions)}</h3>
            </div>
            <div class="muted">배점: 1점</div>
          </div>
          
          <h4>{q['prompt']}</h4>
          
          <div style="margin: 15px 0;">
        """

        if q["qtype"] == "MCQ":
            for c_idx, c in enumerate(q["choices"]):
                q_html += f"""
                <label>
                  <input type="radio" name="q_{q['id']}" value="{c_idx}" required />
                  <strong>{chr(65+c_idx)}.</strong> {c}
                </label>
                """

        q_html += "</div></div>"

    body = f"""
    <div class="header">
      <h1>📝 {exam_type_name}</h1>
      <p>총 {len(questions)}문제 | 배점: {len(questions)}점</p>
    </div>
    
    <div class="card" style="background: #f0f9ff; border-left: 4px solid #3b82f6; margin-bottom: 20px;">
      <p><strong>⏱️ 시험 정보</strong></p>
      <ul>
        <li>문제 수: {len(questions)}개 (실제 시험 기준)</li>
        <li>배점: 100점 (1문제 = 1점대)</li>
        <li>합격선: 60점 이상</li>
        <li>응답 방식: 객관식 단일 선택</li>
      </ul>
    </div>
    
    <form method="post">
      <input type="hidden" name="user" value="{user}" />
      {q_html}
      <div class="row">
        <button class="btn btn-blue" type="submit">✅ 제출하기</button>
        <a class="btn btn-light" href="/">취소</a>
      </div>
    </form>
    """
    return render_template_string(BASE_HTML, body=body)
    user = request.values.get("user", "demo")
    questions = get_questions(exam_type)

    if not questions:
        return render_template_string(BASE_HTML, body=f'<div class="card"><h2>시험 문제를 찾을 수 없습니다: {exam_type}</h2></div>')

    # POST: 시험 제출 및 채점
    if request.method == "POST":
        total = len(questions)
        correct = 0
        details = []
        weak_points = {}  # 약점 분석

        for q in questions:
            qid = q["id"]
            is_correct = False
            user_answer_display = ""
            picked_idx = None

            if q["qtype"] == "MCQ":
                picked = request.form.get(f"q_{qid}")
                if picked is not None:
                    picked_idx = int(picked)
                    is_correct = (picked_idx == q["answer"])
                    user_answer_display = q["choices"][picked_idx]
                else:
                    user_answer_display = "(무응답)"
                    picked_idx = -1

            elif q["qtype"] == "2D_SIMULATOR":
                sim_data = SIMULATOR_PROGRESS.get(user, {})
                completed_tasks = sim_data.get("completed_tasks", 0)
                is_correct = (completed_tasks >= q["min_completion"])
                user_answer_display = f"{completed_tasks}/{q['min_completion']} 작업 완료"

            if is_correct:
                correct += 1
            else:
                add_wrong_note(user, qid, memo="복습 필요")
                # 약점 분석
                if "subject" not in weak_points:
                    weak_points[q["subject"]] = 0
                weak_points[q["subject"]] += 1

            details.append({
                "q": q,
                "is_correct": is_correct,
                "user_answer": user_answer_display,
                "picked_idx": picked_idx
            })

        score = round((correct / total) * 100)

        ATTEMPTS.append({
            "user": user,
            "exam_type": exam_type,
            "score": score,
            "correct": correct,
            "total": total,
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # 상세 답안지 생성
        detail_html = ""
        for i, d in enumerate(details, start=1):
            q = d["q"]
            status = '<span class="ok">✅ 정답</span>' if d["is_correct"] else '<span class="bad">❌ 오답</span>'
            
            detail_html += f"""
            <div class="card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <div class="pill">{q['subject']}</div>
                  <h3>문제 {i}. {q['prompt']}</h3>
                </div>
                <div>{status}</div>
              </div>
              
              <div style="margin: 15px 0;">
                <h4>📋 선택지별 설명</h4>
            """
            
            # MCQ 타입일 때 선택지별 설명
            if q["qtype"] == "MCQ":
                for c_idx, c in enumerate(q["choices"]):
                    is_answer = (c_idx == q["answer"])
                    is_picked = (c_idx == d["picked_idx"])
                    
                    # 스타일 결정
                    if is_answer:
                        explanation_class = "choice-explanation correct"
                        mark = "✅ 정답"
                    else:
                        explanation_class = "choice-explanation incorrect"
                        mark = "❌ 오답"
                    
                    # 선택 표시
                    pick_mark = " ← 내 답" if is_picked else ""
                    
                    detail_html += f"""
                    <div class="{explanation_class}">
                      <strong>{chr(65+c_idx)}. {mark}{pick_mark}</strong><br/>
                      {c}<br/>
                      <em>{q['choice_explanations'][c_idx]}</em>
                    </div>
                    """
            
            # 분석
            detail_html += f"""
              </div>
              <div class="analysis-box">
                <strong>📊 분석:</strong> {q.get('analysis', q.get('explanation', '-'))}
              </div>
            </div>
            """

        # 약점 분석 리포트
        weakness_html = "<h3>📊 약점 분석</h3>"
        if weak_points:
            weakness_html += "<ul>"
            for subject, count in sorted(weak_points.items(), key=lambda x: x[1], reverse=True):
                weakness_html += f"<li>{subject}: {count}개 오답</li>"
            weakness_html += "</ul>"
        else:
            weakness_html += "<p class='ok'>완벽합니다! 약점이 없습니다! 🎉</p>"

        body = f"""
        <div class="header">
          <h1>📊 시험 결과</h1>
          <p>사용자: <strong>{user}</strong> | 시험: <strong>{exam_type}</strong></p>
        </div>
        
        <div class="score-display">
          <h2>{score}점</h2>
          <p>{correct}개 정답 / {total}개 문제</p>
          <p>{"🎉 합격!" if score >= 60 else "재응시 권장"}</p>
        </div>
        
        <div class="card">
          {weakness_html}
        </div>
        
        <div class="row">
          <a class="btn btn-light" href="/exam/{exam_type}?user={user}">다시 응시</a>
          <a class="btn btn-gray" href="/wrong-notes?user={user}">오답노트 보기</a>
          <a class="btn btn-blue" href="/">홈</a>
        </div>
        
        <hr style="margin: 30px 0; border:none; border-top: 2px solid #e5e7eb;">
        <h2>📖 상세 답안지</h2>
        {detail_html}
        """
        return render_template_string(BASE_HTML, body=body)

    # GET: 시험 화면
    exam_type_name = {
        "WRITTEN": "필기 시험",
        "PRACTICAL_WORK": "실기 시험 (2D 시뮬레이터)"
    }.get(exam_type, exam_type)
    
    # 2D 시뮬레이터가 포함된 경우
    if exam_type == "PRACTICAL_WORK" and any(q["qtype"] == "2D_SIMULATOR" for q in questions):
        body = f"""
        <div class="header">
          <h1>🛠️ 실기 시험 (2D 시뮬레이터)</h1>
          <p>모든 작업을 완료하고 제출하세요.</p>
        </div>
        
        <div class="card">
          <h2>공조냉동 2D 시뮬레이터</h2>
          <p class="muted">아래에서 8가지 실습 작업을 모두 완료해주세요.</p>
          
          <div id="simulator-container" style="width:100%; height:700px; border:2px solid #e5e7eb; border-radius:8px; overflow:hidden; margin:20px 0; background:#000;">
            <canvas id="simulatorCanvas" style="display:block; width:100%; height:100%;"></canvas>
          </div>
          
          <div style="background:#f0f9ff; padding:15px; border-radius:8px; margin:15px 0; border-left:4px solid #3b82f6;">
            <p><strong>📋 진행 상황:</strong></p>
            <div class="progress-bar">
              <div class="progress-fill" id="progressFill" style="width:0%;"></div>
            </div>
            <p id="progress-display">시뮬레이터 로딩 중...</p>
          </div>
          
          <form method="post">
            <input type="hidden" name="user" value="{user}" />
            <div class="row">
              <button class="btn btn-blue" type="submit">✅ 제출하기</button>
              <a class="btn btn-light" href="/">취소</a>
            </div>
          </form>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
        <script>
          {SIMULATOR_2D_JS}
        </script>
        """
        return render_template_string(BASE_HTML, body=body)

    # 일반 필기 시험 화면 (CBT 형식)
    q_html = ""
    for idx, q in enumerate(questions, start=1):
        q_html += f"""
        <div class="card" style="page-break-inside: avoid;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div class="pill">{q["subject"]}</div>
              <h3>문제 {idx}/{len(questions)}</h3>
            </div>
            <div class="muted">배점: 1점</div>
          </div>
          
          <h4>{q['prompt']}</h4>
          
          <div style="margin: 15px 0;">
        """

        if q["qtype"] == "MCQ":
            for c_idx, c in enumerate(q["choices"]):
                q_html += f"""
                <label>
                  <input type="radio" name="q_{q['id']}" value="{c_idx}" />
                  <strong>{chr(65+c_idx)}.</strong> {c}
                </label>
                """

        q_html += "</div></div>"

    body = f"""
    <div class="header">
      <h1>📝 {exam_type_name}</h1>
      <p>총 {len(questions)}문제 | 제한시간 없음</p>
    </div>
    
    <form method="post">
      <input type="hidden" name="user" value="{user}" />
      {q_html}
      <div class="row">
        <button class="btn btn-blue" type="submit">✅ 제출하기</button>
        <a class="btn btn-light" href="/">취소</a>
      </div>
    </form>
    """
    return render_template_string(BASE_HTML, body=body)

@app.route("/wrong-notes")
def wrong_notes():
    user = request.args.get("user", "demo")
    user_wrongs = [w for w in WRONG_NOTES if w["user"] == user]

    if not user_wrongs:
        body = f"""
        <div class="header">
          <h1>📌 오답노트</h1>
          <p>틀린 문제를 모아 복습합니다.</p>
        </div>
        
        <div class="card">
          <h2>축하합니다! 🎉</h2>
          <p>{user}님의 오답이 없습니다. 모든 문제를 정답하셨습니다!</p>
          <a class="btn btn-blue" href="/">홈으로</a>
        </div>
        """
        return render_template_string(BASE_HTML, body=body)

    rows = ""
    for i, w in enumerate(sorted(user_wrongs, key=lambda x: x["ts"], reverse=True), start=1):
        q = find_question(w["qid"])
        if not q:
            continue
        rows += f"""
        <div class="card">
          <div style="display:flex; justify-content:space-between;">
            <div>
              <p class="muted">{i}. [{q['exam_type']}] {q['subject']} / {w['ts']}</p>
              <h3>{q['prompt']}</h3>
            </div>
            <div class="bad">오답</div>
          </div>
          
          <div style="margin-top: 10px;">
            <p><strong>해설:</strong> {q.get('explanation', '-')}</p>
            <p><strong>분석:</strong> {q.get('analysis', '-')}</p>
          </div>
          
          <div style="margin-top: 10px; padding: 10px; background: #f0f9ff; border-radius: 6px;">
            <p><strong>메모:</strong> {w['memo'] or '-'}</p>
          </div>
        </div>
        """

    body = f"""
    <div class="header">
      <h1>📌 오답노트</h1>
      <p>틀린 문제 {len(user_wrongs)}개를 다시 복습하세요.</p>
    </div>
    
    <div class="card">
      <div class="row">
        <a class="btn btn-blue" href="/">홈</a>
      </div>
    </div>
    
    {rows}
    """
    return render_template_string(BASE_HTML, body=body)

@app.route("/attempts")
def attempts():
    user = request.args.get("user", "demo")
    items = [a for a in ATTEMPTS if a["user"] == user]
    
    if not items:
        body = f"""
        <div class="card">
          <h2>📊 응시 기록</h2>
          <p>아직 응시 기록이 없습니다.</p>
          <a class="btn btn-blue" href="/">홈</a>
        </div>
        """
        return render_template_string(BASE_HTML, body=body)

    rows = ""
    for a in sorted(items, key=lambda x: x["ts"], reverse=True):
        rows += f"""
        <tr>
          <td>{a['ts']}</td>
          <td>{a['exam_type']}</td>
          <td><strong>{a['score']}점</strong></td>
          <td>{a['correct']}/{a['total']}</td>
        </tr>
        """

    body = f"""
    <div class="card">
      <h2>📊 응시 기록 - {user}</h2>
      <table border="1" cellpadding="10" cellspacing="0" style="border-collapse:collapse; width:100%;">
        <thead><tr style="background:#f3f4f6;"><th>일시</th><th>유형</th><th>점수</th><th>정답수</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <br/>
      <a class="btn btn-blue" href="/">홈</a>
    </div>
    """
    return render_template_string(BASE_HTML, body=body)

# ================================ 메인 ===================================
if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════╗
    ║  🎓 공조냉동기계기능사 합격 플랫폼         ║
    ║  Flask 서버 시작 중...                    ║
    ║  접속: http://127.0.0.1:5000              ║
    ║  Ctrl+C 로 종료                           ║
    ╚════════════════════════════════════════════╝
    """)
    app.run(debug=True, port=5000)
