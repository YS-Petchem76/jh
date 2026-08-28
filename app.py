from flask import Flask, request, render_template_string, jsonify
from datetime import datetime, timedelta, date
import os

app = Flask(__name__)

def generate_questions_by_year(year):
    questions = {
        2020: [
            {"id": 1, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매의 조건으로 가장 중요하지 않은 것은?", "choices": ["열전달이 우수해야 한다", "화학적으로 안정해야 한다", "생산 비용이 낮아야 한다", "독성이 없어야 한다"], "answer": 2, "explanation": "생산 비용보다 안전성과 효율이 중요합니다.", "choice_explanations": ["✅ 냉매는 열전달이 우수해야 합니다", "✅ 화학적 안정성은 필수입니다", "❌ 안전성이 비용보다 중요합니다", "✅ 독성이 없어야 안전합니다"], "analysis": "냉매 선택 시 안전성을 최우선으로 고려합니다", "year": year},
            {"id": 2, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기의 성능계수(COP)의 정의는?", "choices": ["냉동능력÷압축기입력", "응축기 출력÷냉동능력", "압축기 입력÷냉동능력", "냉동능력×응축능력"], "answer": 0, "explanation": "COP는 냉동능력을 압축기 입력으로 나눈 값입니다.", "choice_explanations": ["✅ 정확", "❌ 아님", "❌ 역수", "❌ 아님"], "year": year},
            {"id": 3, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "압축기 오일의 역할이 아닌 것은?", "choices": ["냉매 누설 차단", "베어링 윤활", "피스톤 링 씰링", "열 제거"], "answer": 0, "explanation": "오일의 주요 역할은 윤활, 씰링, 냉각입니다.", "choice_explanations": ["❌ 차단 안함", "✅ 윤활", "✅ 씰링", "✅ 냉각"], "year": year},
            {"id": 4, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "건구온도와 습구온도의 차를 무엇이라 하는가?", "choices": ["절대습도", "상대습도", "과열도", "건습도차"], "answer": 3, "explanation": "건구온도와 습구온도의 차이를 건습도차라 합니다.", "choice_explanations": ["❌ 다른개념", "❌ 다른개념", "❌ 사이클", "✅ 건습도차"], "year": year},
            {"id": 5, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "습공기의 엔탈피는 다음 중 어느 것의 조합인가?", "choices": ["현열+잠열", "건공기의 엔탈피+수증기의 엔탈피", "온도×습도", "압력×부피"], "answer": 0, "explanation": "엔탈피는 현열과 잠열의 합입니다.", "choice_explanations": ["✅ 정의", "✅ 표현", "❌ 작업량", "❌ 다른개념"], "year": year},
            {"id": 6, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "응축기에서 냉매의 상태 변화는?", "choices": ["액체→증기", "증기→액체", "액체→액체", "증기→증기"], "answer": 1, "explanation": "응축기에서는 고온 고압 증기가 액화됩니다.", "choice_explanations": ["❌ 반대", "✅ 응축", "❌ 무", "❌ 무"], "year": year},
            {"id": 7, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "쿨링타워의 주요 기능은?", "choices": ["습공기 제거", "온수를 냉각", "냉수를 가열", "습도 증가"], "answer": 1, "explanation": "쿨링타워는 응축기에서 나온 온수를 냉각시킵니다.", "choice_explanations": ["❌ 아님", "✅ 정확", "❌ 반대", "❌ 반대"], "year": year},
            {"id": 8, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "증발기의 출구에서 냉매의 상태는?", "choices": ["포화 액체", "포화 증기", "과냉각 액체", "습공기"], "answer": 1, "explanation": "정상 운전 시 증발기 출구는 포화 증기 상태입니다.", "choice_explanations": ["❌ 입구", "✅ 출구", "❌ 비정상", "❌ 아님"], "year": year},
            {"id": 9, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "가습 방식 중 가장 간단한 방식은?", "choices": ["분무식", "스팀식", "기계식", "UV식"], "answer": 0, "explanation": "분무식 가습은 가장 간단하고 경제적입니다.", "choice_explanations": ["✅ 간단", "❌ 복잡", "❌ 복잡", "❌ 비쌈"], "year": year},
            {"id": 10, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동장치에서 안전장치의 역할이 아닌 것은?", "choices": ["과압 방지", "과전류 방지", "냉매 누설 감지", "냉각수 온도 조절"], "answer": 3, "explanation": "안전장치는 과압, 과전류 방지와 누설 감지를 합니다.", "choice_explanations": ["✅ 역할", "✅ 역할", "✅ 역할", "❌ 제어"], "year": year},
        ] + [
            {"id": 10+i, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반" if i < 25 else "공기조화", "prompt": f"기출문제 {10+i}번 ({year}년)", "choices": ["선택지 A", "선택지 B", "선택지 C", "선택지 D"], "answer": i % 4, "explanation": "기출문제 해설", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year}
            for i in range(50)
        ],
    }
    
    for y in [2019, 2018, 2017, 2016, 2015, 2014]:
        base_id = (2020 - y) * 100 + 200
        questions[y] = [
            {"id": base_id + i, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반" if i < 30 else "공기조화", "prompt": f"기출문제 {base_id + i}번 ({y}년)", "choices": ["선택지 A", "선택지 B", "선택지 C", "선택지 D"], "answer": i % 4, "explanation": "기출문제 해설입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": y}
            for i in range(60)
        ]
    
    return questions.get(year, [])

def generate_practical_written_by_year(year):
    return [
        {"id": 1001, "exam_type": "PRACTICAL_WRITTEN", "qtype": "SHORT", "subject": "실기", "prompt": "과열도의 정의를 설명하시오.", "keywords": ["증발기", "출구", "포화", "온도"], "sample_answer": "증발기 출구에서의 냉매 온도와 같은 압력에서의 포화온도의 차이", "explanation": "과열도는 냉동 사이클의 효율을 평가합니다", "year": year},
        {"id": 1002, "exam_type": "PRACTICAL_WRITTEN", "qtype": "SHORT", "subject": "실기", "prompt": "냉동기의 압축비를 정의하시오.", "keywords": ["고압", "저압", "비율"], "sample_answer": "압축기 토출 압력을 흡입 압력으로 나눈 값", "explanation": "압축비가 높을수록 압축기에 부하가 커집니다", "year": year},
        {"id": 1003, "exam_type": "PRACTICAL_WRITTEN", "qtype": "SHORT", "subject": "실기", "prompt": "응축기의 역할을 설명하시오.", "keywords": ["냉매", "액화", "열"], "sample_answer": "고온 고압의 냉매 증기를 냉각하여 액체로 변화시키고 열을 제거", "explanation": "응축기는 냉동 사이클의 핵심 부품입니다", "year": year},
        {"id": 1004, "exam_type": "PRACTICAL_WRITTEN", "qtype": "SHORT", "subject": "실기", "prompt": "동관 절단 시 주의사항을 두 가지 이상 쓰시오.", "keywords": ["직각", "버", "청결"], "sample_answer": "직각으로 정확히 절단하고, 버를 제거하며, 절단면을 청결하게 유지", "explanation": "동관 절단은 이후 모든 작업의 기초입니다", "year": year},
        {"id": 1005, "exam_type": "PRACTICAL_WRITTEN", "qtype": "SHORT", "subject": "실기", "prompt": "플레어링의 목적을 설명하시오.", "keywords": ["접합", "누설", "방지"], "sample_answer": "동관의 끝을 벌려서 연결구와의 접합면을 넓혀 누설을 방지", "explanation": "플레어링은 냉동 장치 안정성의 핵심입니다", "year": year},
        {"id": 1006, "exam_type": "PRACTICAL_WRITTEN", "qtype": "SHORT", "subject": "실기", "prompt": "밴딩(bending) 작업의 주의사항을 설명하시오.", "keywords": ["반경", "최소", "압력"], "sample_answer": "최소 반경 이상으로 구부리고 과도한 압력을 가하지 않기", "explanation": "동관의 손상을 방지하려면 적절한 반경이 필요합니다", "year": year},
        {"id": 1007, "exam_type": "PRACTICAL_WRITTEN", "qtype": "SHORT", "subject": "실기", "prompt": "용접 시 냉매 누출을 방지하는 방법을 쓰시오.", "keywords": ["질소", "충전", "산화"], "sample_answer": "동관 내부에 질소를 충전하여 산화를 방지", "explanation": "용접 부위의 산화는 냉동장치 고장의 원인입니다", "year": year},
        {"id": 1008, "exam_type": "PRACTICAL_WRITTEN", "qtype": "SHORT", "subject": "실기", "prompt": "누설 검사(leak test) 방법을 설명하시오.", "keywords": ["비누", "할로겐", "감지"], "sample_answer": "비누액을 이용하여 거품 생성 여부를 확인하거나 할로겐 검출기 사용", "explanation": "누설 검사는 안전성을 보장하는 중요한 과정입니다", "year": year},
    ]

QUESTIONS_BY_YEAR = {year: generate_questions_by_year(year) for year in range(2014, 2021)}
PRACTICAL_WRITTEN_BY_YEAR = {year: generate_practical_written_by_year(year) for year in range(2014, 2021)}

ATTEMPTS = []
WRONG_NOTES = []
SIMULATOR_PROGRESS = {}
PLANNER_DATA = {}

SIMULATOR_2D_JS = """
const canvas = document.getElementById('simulatorCanvas');
const ctx = canvas.getContext('2d');
canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

let completedTasks = 0;
let tubeLength = 100;
let bendingAngle = 45;
let currentMode = null;
let flaringDone = false;
let toolAnimationStart = null;
let weldingHoldStart = null;
let weldingDone = false;
let coolingStart = null;
let coolingDone = false;
let coolingTransitioned = false;
let inspectionCompleted = false;

const tasks = ['1️⃣ 동관절단', '2️⃣ 플레어링', '3️⃣ 밴딩', '4️⃣ 연결', '5️⃣ 용접', '6️⃣ 냉각작업', '7️⃣ 작동점검'];
let taskStates = [
  {x:80,y:60,w:140,h:70,done:false,interactive:true},
  {x:270,y:60,w:140,h:70,done:false,interactive:false},
  {x:460,y:60,w:140,h:70,done:false,interactive:false},
  {x:650,y:60,w:140,h:70,done:false,interactive:false},
  {x:80,y:180,w:140,h:70,done:false,interactive:false},
  {x:270,y:180,w:140,h:70,done:false,interactive:false},
  {x:460,y:180,w:140,h:70,done:false,interactive:false},
];

function draw(){
  const g=ctx.createLinearGradient(0,0,canvas.width,canvas.height);g.addColorStop(0,'#e8f4f8');g.addColorStop(1,'#f0e8f8');ctx.fillStyle=g;ctx.fillRect(0,0,canvas.width,canvas.height);
  ctx.font='bold 18px Arial';ctx.fillStyle='#1a3a4a';ctx.fillText('🛠️ 실기 작업 시뮬레이션',20,35);
  
  const WORK_AREA_Y = 280;
  const WORK_AREA_HEIGHT = 200;
  ctx.fillStyle='rgba(200,220,240,0.3)';ctx.fillRect(80, WORK_AREA_Y, 600, WORK_AREA_HEIGHT);
  ctx.strokeStyle='#4d7ec7';ctx.lineWidth=2;ctx.strokeRect(80, WORK_AREA_Y, 600, WORK_AREA_HEIGHT);
  ctx.fillStyle='#4d7ec7';ctx.font='bold 11px Arial';ctx.fillText('📋 작업 영역', 85, WORK_AREA_Y + 15);
  
  if(currentMode){
    ctx.fillStyle='#4d7ec7';ctx.font='bold 14px Arial';
    if(currentMode === 'cutting'){
      ctx.fillText('👇 동관을 클릭하여 절단 위치를 선택하세요',20,270);
      const w = tubeLength * 2;
      ctx.fillStyle = '#e8a333';
      ctx.fillRect(150, 320, w, 40);
      ctx.strokeStyle = '#d4860f';ctx.lineWidth = 2;ctx.strokeRect(150, 320, w, 40);
      ctx.fillStyle = 'rgba(255,255,255,0.2)';ctx.fillRect(150, 320, w, 15);
      ctx.fillStyle = '#000';ctx.font = 'bold 12px Arial';ctx.fillText(tubeLength + 'mm', 150 + tubeLength - 15, 350);
    }
    else if(currentMode === 'flaring'){
      ctx.fillText('👇 동관 끝을 클릭하여 플레어링 하세요',20,270);
      const sw = (tubeLength / 3) * 2;
      ctx.fillStyle = '#e8a333';
      ctx.fillRect(150, 320, sw, 40);
      ctx.strokeStyle = '#d4860f';ctx.lineWidth = 2;ctx.strokeRect(150, 320, sw, 40);
      ctx.fillStyle = 'rgba(255,255,255,0.3)';ctx.fillRect(150, 320, sw, 15);
      if(flaringDone){
        ctx.fillStyle = '#f5c26b';
        ctx.beginPath();ctx.moveTo(150+sw, 320);ctx.lineTo(150+sw+20, 310);ctx.lineTo(150+sw+20, 360);ctx.lineTo(150+sw, 360);ctx.closePath();
        ctx.fill();
      }
      ctx.fillStyle = '#000';ctx.font = 'bold 11px Arial';ctx.fillText('1/3크기', 150 + sw/2 - 20, 350);
    }
    else if(currentMode === 'bending'){
      ctx.fillText('👇 동관을 클릭하여 밴딩을 완료하세요 (각도: ' + bendingAngle + '°)',20,270);
      
      const segLen = (tubeLength * 2) / 2;
      const startX = 100, startY = 330;
      const rad = (bendingAngle * Math.PI) / 180;
      
      ctx.strokeStyle = '#e8a333';
      ctx.lineWidth = 8;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      ctx.beginPath();
      ctx.moveTo(startX, startY);
      ctx.lineTo(startX + segLen, startY);
      ctx.stroke();
      
      ctx.save();
      ctx.translate(startX + segLen, startY);
      ctx.rotate(rad);
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(0, segLen);
      ctx.stroke();
      ctx.restore();
      
      ctx.fillStyle = '#000';ctx.font = 'bold 12px Arial';
      ctx.fillText(bendingAngle + '°', startX + segLen + 20, startY - 30);
    }
    else if(currentMode === 'connecting'){
      ctx.fillText('👇 절단된 동관들을 연결하세요',20,270);
      const elapsed = Date.now() - toolAnimationStart;
      const prog = Math.min(elapsed / 4000, 1);
      const tubes = [{n:'절단1',x:120},{n:'절단2',x:200},{n:'플레어링',x:280},{n:'밴딩',x:360}];
      tubes.forEach((t,idx) => {
        const a = Math.max(0, (prog - idx*0.3));
        ctx.globalAlpha = a;
        ctx.fillStyle = '#e8a333';
        ctx.fillRect(t.x, 320, 60, 40);
        ctx.strokeStyle = '#d4860f';ctx.lineWidth = 2;ctx.strokeRect(t.x, 320, 60, 40);
        ctx.fillStyle = '#000';ctx.font = 'bold 10px Arial';ctx.textAlign = 'center';
        ctx.fillText(t.n, t.x + 30, 340);ctx.textAlign = 'left';
        ctx.globalAlpha = 1;
      });
    }
    else if(currentMode === 'welding'){
      ctx.fillText('🔥 연결된 동관에 용접을 합니다. 마우스를 3초 이상 누르세요',20,270);
      const tubes = [{n:'절단1',x:120},{n:'절단2',x:180},{n:'플레어',x:240},{n:'밴딩',x:300}];
      tubes.forEach(t => {
        ctx.fillStyle = '#e8a333';
        ctx.fillRect(t.x, 320, 50, 35);
        ctx.strokeStyle = '#d4860f';ctx.lineWidth = 2;ctx.strokeRect(t.x, 320, 50, 35);
        ctx.fillStyle = '#000';ctx.font = 'bold 9px Arial';ctx.textAlign = 'center';
        ctx.fillText(t.n, t.x + 25, 338);ctx.textAlign = 'left';
      });
      if(weldingHoldStart !== null){
        const holdT = Date.now() - weldingHoldStart;
        const p = Math.min(holdT / 3000, 1);
        ctx.fillStyle = '#ddd';ctx.fillRect(100,380,300,20);
        ctx.fillStyle = '#ff6b35';ctx.fillRect(100,380,300*p,20);
        ctx.fillStyle = '#000';ctx.font = 'bold 12px Arial';
        ctx.fillText(Math.round(p*100)+'%', 410, 390);
        if(p >= 1) weldingDone = true;
      }
      if(weldingDone){
        ctx.fillStyle = 'rgba(255,107,53,0.8)';ctx.fillRect(100,320,300,60);
        ctx.fillStyle = '#fff';ctx.font = 'bold 20px Arial';ctx.textAlign = 'center';
        ctx.fillText('✅ 용접 완료!', 250, 355);ctx.textAlign = 'left';
      }
    }
    else if(currentMode === 'cooling'){
      ctx.fillText('💧 냉각수로 냉각합니다... 3초 대기 중',20,270);
      const tubes = [{n:'동관1',x:120},{n:'동관2',x:180},{n:'동관3',x:240},{n:'동관4',x:300}];
      tubes.forEach(t => {
        ctx.fillStyle = '#d4a574';ctx.fillRect(t.x, 330, 50, 30);
        ctx.strokeStyle = '#8b5a2b';ctx.lineWidth = 2;ctx.strokeRect(t.x, 330, 50, 30);
        ctx.fillStyle = '#000';ctx.font = 'bold 9px Arial';ctx.textAlign = 'center';
        ctx.fillText(t.n, t.x + 25, 348);ctx.textAlign = 'left';
      });
      if(coolingStart !== null){
        const elapsed = Date.now() - coolingStart;
        const p = Math.min(elapsed / 3000, 1);
        ctx.fillStyle = '#e0f2fe';ctx.fillRect(100,420,300,20);
        ctx.fillStyle = '#0ea5e9';ctx.fillRect(100,420,300*p,20);
        ctx.fillStyle = '#000';ctx.font = 'bold 10px Arial';ctx.textAlign = 'center';
        ctx.fillText(Math.round(p*100)+'%', 250, 432);ctx.textAlign = 'left';
        if(p >= 1 && !coolingTransitioned){
          coolingDone = true;
          coolingTransitioned = true;
          currentMode = 'inspection';
          inspectionCompleted = false;
        }
      }
    }
    else if(currentMode === 'inspection'){
      ctx.fillText('✅ 작동점검 - 조립된 장치가 정상 작동합니다',20,270);
      ctx.font = 'bold 36px Arial';
      const items = ['🔧','⚙️','🔩','💨'];
      items.forEach((item,i) => {
        ctx.fillText(item, 150 + i*50, 350);
      });
      ctx.fillStyle = 'rgba(82,196,26,0.8)';ctx.fillRect(100,400,300,50);
      ctx.fillStyle = '#fff';ctx.font = 'bold 20px Arial';ctx.textAlign = 'center';
      ctx.fillText('✅ 합격!', 250, 435);ctx.textAlign = 'left';
      if(!inspectionCompleted){
        inspectionCompleted = true;
        setTimeout(() => {
          currentMode = null;
          taskStates[6].done = true;
          completedTasks++;
          const pf = document.getElementById('progressFill');if(pf)pf.style.width = (completedTasks/7*100)+'%';
          fetch('/api/simulator-progress',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:'{user}',completed_tasks:completedTasks})});
        }, 2000);
      }
    }
  }
  
  taskStates.forEach((t,i)=>{
    const g=ctx.createLinearGradient(t.x,t.y,t.x,t.y+t.h);
    if(t.done){g.addColorStop(0,'#27ae60');g.addColorStop(1,'#229954');}
    else if(t.interactive){g.addColorStop(0,'#5b9bd5');g.addColorStop(1,'#4472c4');}
    else{g.addColorStop(0,'#bdc3c7');g.addColorStop(1,'#95a5a6');}
    ctx.fillStyle=g;ctx.fillRect(t.x,t.y,t.w,t.h);
    ctx.strokeStyle=t.done?'#27ae60':(t.interactive?'#667eea':'#95a5a6');ctx.lineWidth=2;ctx.strokeRect(t.x,t.y,t.w,t.h);
    ctx.fillStyle='#fff';ctx.font='bold 12px Arial';ctx.textAlign='center';
    ctx.fillText(t.done?tasks[i]+' ✅':tasks[i],t.x+t.w/2,t.y+t.h/2+5);ctx.textAlign='left';
  });
  
  ctx.fillStyle='#1a3a4a';ctx.font='bold 20px Arial';ctx.fillText('진행률: ' + completedTasks + '/7',20,canvas.height-20);
}

canvas.addEventListener('click',(e)=>{
  const rect=canvas.getBoundingClientRect();const x=e.clientX-rect.left;const y=e.clientY-rect.top;
  
  if(currentMode === 'cutting' && y > 310 && y < 370) {
    const sx = 150, ex = 150 + tubeLength * 2;
    if(x >= sx && x <= ex) {
      currentMode = null;
      taskStates[0].done = true;
      completedTasks++;
      if(completedTasks < 8) taskStates[completedTasks].interactive = true;
      const pf = document.getElementById('progressFill');
      if(pf) pf.style.width = (completedTasks/8*100)+'%';
      fetch('/api/simulator-progress', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({user:'{user}',completed_tasks:completedTasks})});
      draw();
      return;
    }
  }
  else if(currentMode === 'flaring' && y > 310 && y < 370) {
    const sw = (tubeLength / 3) * 2;
    if(x >= 150 && x <= 150 + sw + 20) {
      flaringDone = true;
      draw();
      setTimeout(() => {
        currentMode = null;
        taskStates[1].done = true;
        completedTasks++;
        if(completedTasks < 7) taskStates[completedTasks].interactive = true;
        const pf = document.getElementById('progressFill');
        if(pf) pf.style.width = (completedTasks/7*100)+'%';
        fetch('/api/simulator-progress', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({user:'{user}',completed_tasks:completedTasks})});
        draw();
      }, 300);
      return;
    }
  }
  else if(currentMode === 'bending' && y > 310 && y < 380) {
    currentMode = null;
    taskStates[2].done = true;
    completedTasks++;
    if(completedTasks < 7) taskStates[completedTasks].interactive = true;
    const pf = document.getElementById('progressFill');
    if(pf) pf.style.width = (completedTasks/7*100)+'%';
    document.getElementById('bendingPanel').style.display = 'none';
    fetch('/api/simulator-progress', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({user:'{user}',completed_tasks:completedTasks})});
    draw();
    return;
  }
  
  taskStates.forEach((t,i)=>{
    if(x>t.x&&x<t.x+t.w&&y>t.y&&y<t.y+t.h&&!t.done&&t.interactive){
      if(i===0){currentMode='cutting';}
      else if(i===1){currentMode='flaring';flaringDone=false;}
      else if(i===2){currentMode='bending';document.getElementById('bendingPanel').style.display='block';}
      else if(i===3){currentMode='connecting';toolAnimationStart=Date.now();setTimeout(()=>{currentMode=null;taskStates[3].done=true;completedTasks++;if(completedTasks<7)taskStates[completedTasks].interactive=true;fetch('/api/simulator-progress',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:'{user}',completed_tasks:completedTasks})});draw();},4500);}
      else if(i===4){currentMode='welding';weldingDone=false;weldingHoldStart=null;}
      else if(i===5){currentMode='cooling';coolingStart=Date.now();coolingDone=false;coolingTransitioned=false;inspectionCompleted=false;}
      else if(i===6){currentMode='inspection';}
      const pf=document.getElementById('progressFill');if(pf)pf.style.width=(completedTasks/7*100)+'%';
      draw();
    }
  });
});

canvas.addEventListener('mousedown',(e)=>{
  if(currentMode==='welding'&&!weldingDone){weldingHoldStart=Date.now();}
});

canvas.addEventListener('mouseup',(e)=>{
  if(currentMode==='welding'&&weldingDone&&weldingHoldStart!==null){
    currentMode=null;
    taskStates[4].done=true;
    completedTasks++;
    if(completedTasks<7)taskStates[completedTasks].interactive=true;
    const pf=document.getElementById('progressFill');if(pf)pf.style.width=(completedTasks/7*100)+'%';
    fetch('/api/simulator-progress',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:'{user}',completed_tasks:completedTasks})});
    draw();
  }
  weldingHoldStart=null;
});

window.addEventListener('resize',()=>{canvas.width=canvas.offsetWidth;canvas.height=canvas.offsetHeight;});

let lastMouseX=0,lastMouseY=0;
canvas.addEventListener('mousemove',(e)=>{
  const r=canvas.getBoundingClientRect();lastMouseX=e.clientX-r.left;lastMouseY=e.clientY-r.top;
  if(currentMode==='welding'||currentMode==='cooling'){
    canvas.style.cursor='none';
  }else{canvas.style.cursor='auto';}
});

function animate(){
  draw();
  if(currentMode==='welding'&&!weldingDone){
    ctx.font='bold 32px Arial';ctx.fillText('🔥',lastMouseX-15,lastMouseY+10);
  }else if(currentMode==='cooling'&&!coolingDone){
    ctx.font='bold 32px Arial';ctx.fillText('💧',lastMouseX-15,lastMouseY+10);
  }
  requestAnimationFrame(animate);
}
animate();

document.getElementById('tubeLength').addEventListener('change', (e) => {
  const v = parseInt(e.target.value);
  if(v > 0) tubeLength = v;
  draw();
});

document.getElementById('bendingAngle').addEventListener('change', (e) => {
  const v = parseInt(e.target.value);
  if(v >= 0 && v <= 180) bendingAngle = v;
  draw();
});

draw();
"""

def grade_short_answer(user_text, keywords):
    text = (user_text or "").replace(" ", "").lower()
    hit = sum(1 for kw in keywords if kw.replace(" ", "").lower() in text)
    return hit >= max(1, len(keywords)//2), hit, len(keywords)

def add_wrong_note(user, qid, memo=""):
    if not any(w["user"]==user and w["qid"]==qid for w in WRONG_NOTES):
        WRONG_NOTES.append({"user":user,"qid":qid,"memo":memo,"ts":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

BASE_HTML = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"/><title>공조냉동기계기능사 시험</title><meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI','Noto Sans KR',sans-serif;background:linear-gradient(135deg,#f0f4f8 0%,#e8f1f8 100%);color:#1a3a4a;min-height:100vh}
.container{max-width:1200px;margin:0 auto;padding:20px}.header{background:linear-gradient(135deg,#2c5aa0 0%,#5b9bd5 100%);color:white;padding:40px 20px;border-radius:12px;margin-bottom:30px;text-align:center;box-shadow:0 8px 24px rgba(44,90,160,0.3)}
.header h1{font-size:36px;margin-bottom:8px}.header p{font-size:16px;opacity:0.95}.card{background:white;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 4px 16px rgba(44,90,160,0.12)}
.btn{display:inline-block;padding:12px 24px;border-radius:8px;text-decoration:none;border:none;cursor:pointer;font-weight:600;font-size:14px;transition:all 0.3s}
.btn:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,0.15)}
.btn-primary{background:#4d7ec7;color:white}.btn-success{background:#52c41a;color:white}.btn-danger{background:#ff4d4f;color:white}.btn-light{background:#f0f4f8;color:#1a3a4a}
.row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}.row a{flex:1;min-width:120px;text-align:center}
h2{font-size:24px;margin-bottom:16px;color:#1a3a4a}h3{font-size:20px;margin:20px 0 12px 0;color:#2c5aa0}.score-display{background:linear-gradient(135deg,#2c5aa0 0%,#5b9bd5 100%);color:white;padding:40px;border-radius:12px;text-align:center;margin:30px 0}
.score-display .score{font-size:72px;font-weight:bold;margin:20px 0}.score-display .label{font-size:18px;opacity:0.95}
label{display:block;padding:12px 16px;margin:8px 0;border:2px solid #d6e8f7;border-radius:8px;cursor:pointer;transition:all 0.2s}
label:hover{background:#f0f4f8;border-color:#4d7ec7}input[type=radio]{margin-right:12px}textarea{width:100%;padding:12px;border:2px solid #d6e8f7;border-radius:8px;font-family:inherit;resize:vertical;margin-bottom:8px}
textarea:focus{border-color:#4d7ec7;outline:none}.pill{display:inline-block;padding:6px 12px;background:#eef2ff;color:#3730a3;border-radius:20px;font-size:12px;font-weight:600;margin-bottom:12px}
.ok{color:#27ae60;font-weight:700}.bad{color:#e74c3c;font-weight:700}.analysis-box{background:#e8f4f8;border-left:4px solid #4d7ec7;padding:16px;margin:16px 0;border-radius:6px;color:#1a3a4a}
.choice-explain{padding:12px;margin:8px 0;border-radius:6px;border-left:4px solid #d1d5db}.choice-explain.correct{background:#dcfce7;border-left-color:#27ae60;color:#166534}
.choice-explain.wrong{background:#fee2e2;border-left-color:#e74c3c;color:#7f1d1d}.progress-bar{width:100%;height:10px;background:#ecf0f1;border-radius:6px;overflow:hidden;margin:16px 0}
.progress-fill{height:100%;background:linear-gradient(90deg,#52c41a,#84c444);transition:width 0.3s}#simulatorCanvas{width:100%;height:400px;display:block;margin:20px 0;background:white;border-radius:8px;border:2px solid #d6e8f7}
.section-title{font-size:18px;font-weight:bold;color:#2c5aa0;margin-top:24px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #4d7ec7}pre{white-space:pre-wrap;word-break:break-word;background:#f5f5f5;padding:10px;border-radius:4px;margin:8px 0}
</style></head><body><div class="container">{{ body|safe }}</div></body></html>"""

@app.route("/")
def home():
    body = """
    <div class="header"><h1>🎓 공조냉동기계기능사 시험 플랫폼</h1><p>2014-2020 기출 문제 | 실시간 채점</p></div>
    <div class="card" style="text-align:center;padding:60px 20px;">
      <h2 style="font-size:32px;margin:20px 0;">📚 시작하기</h2>
      <p style="font-size:18px;color:#666;margin-bottom:40px;">공조냉동기계기능사 시험을 준비하세요</p>
      <a class="btn btn-primary" href="/menu" style="padding:20px 40px;font-size:18px;margin:20px 10px;">🚀 시작하기</a>
    </div>
    """
    return render_template_string(BASE_HTML, body=body)

@app.route("/menu")
def menu():
    body = """
    <div class="header"><h1>🎓 시험 메뉴</h1><p>원하는 시험을 선택하세요</p></div>
    <div class="card"><div class="section-title">📝 필기 시험</div><div class="row"><a class="btn btn-primary" href="/exam-written?user=demo" style="padding:20px 40px;font-size:16px;">📝 필기 시험</a></div></div>
    <div class="card"><div class="section-title">✍️ 실기 필답형</div><div class="row"><a class="btn btn-success" href="/exam-practical?user=demo" style="padding:20px 40px;font-size:16px;">✍️ 실기 필답형</a></div></div>
    <div class="card"><div class="section-title">🛠️ 실기 시뮬레이션</div><div class="row"><a class="btn btn-danger" href="/simulator?user=demo" style="padding:20px 40px;font-size:16px;">🛠️ 실기 시뮬레이션</a></div></div>
    <div class="card"><div class="section-title">📅 데일리 플래너</div><div class="row"><a class="btn btn-warning" href="/planner?user=demo" style="background:#ff9c6e;color:white;padding:20px 40px;font-size:16px;">📅 데일리 플래너</a></div></div>
    <div class="card" style="text-align:center;padding:20px;"><a class="btn btn-light" href="/" style="font-size:16px;">← 돌아가기</a></div>
    """
    return render_template_string(BASE_HTML, body=body)

@app.route("/exam-written")
def exam_written():
    user = request.args.get("user", "demo")
    body = f"""<div class="header"><h1>📝 필기 시험 (객관식)</h1><p>년도를 선택하세요</p></div><div class="card"><div class="row">{"  ".join(f'<a class="btn btn-primary" href="/exam/WRITTEN/{y}?user={user}">{y}년</a>' for y in range(2020, 2013, -1))}</div></div><div class="card" style="text-align:center;"><a class="btn btn-light" href="/menu">← 돌아가기</a></div>"""
    return render_template_string(BASE_HTML, body=body)

@app.route("/exam-practical")
def exam_practical():
    user = request.args.get("user", "demo")
    body = f"""<div class="header"><h1>✍️ 실기 필답형</h1><p>년도를 선택하세요</p></div><div class="card"><div class="row">{"  ".join(f'<a class="btn btn-success" href="/exam/PRACTICAL_WRITTEN/{y}?user={user}">{y}년</a>' for y in range(2020, 2013, -1))}</div></div><div class="card" style="text-align:center;"><a class="btn btn-light" href="/menu">← 돌아가기</a></div>"""
    return render_template_string(BASE_HTML, body=body)

@app.route("/simulator")
def simulator():
    user = request.args.get("user", "demo")
    body = f"""<div class="header"><h1>🛠️ 실기 시뮬레이션</h1></div><div class="card"><div class="row"><a class="btn btn-danger" href="/exam/PRACTICAL_WORK/2020?user={user}" style="padding:20px 40px;font-size:16px;">시작하기</a></div></div><div class="card" style="text-align:center;"><a class="btn btn-light" href="/menu">← 돌아가기</a></div>"""
    return render_template_string(BASE_HTML, body=body)

@app.route("/exam/<exam_type>/<int:year>", methods=["GET", "POST"])
def exam(exam_type, year):
    user = request.values.get("user", "demo")
    
    if exam_type == "PRACTICAL_WRITTEN":
        questions = PRACTICAL_WRITTEN_BY_YEAR.get(year, [])
    elif exam_type == "PRACTICAL_WORK":
        questions = [{"id": 2001, "qtype": "2D_SIMULATOR"}]
    else:
        questions = QUESTIONS_BY_YEAR.get(year, [])
    
    if not questions:
        return render_template_string(BASE_HTML, body='<div class="card"><h2>❌ 문제를 찾을 수 없습니다</h2><a class="btn btn-light" href="/">돌아가기</a></div>')

    if request.method == "POST":
        correct = 0
        total = len(questions)
        details = []
        weak_points = {}

        for q in questions:
            is_correct = False
            user_ans = ""
            picked_idx = None
            kw_hit = kw_total = 0

            if q["qtype"] == "MCQ":
                picked = request.form.get(f"q_{q['id']}")
                if picked:
                    picked_idx = int(picked)
                    is_correct = (picked_idx == q["answer"])
                    user_ans = q["choices"][picked_idx]
                else:
                    user_ans = "(미응답)"
            elif q["qtype"] == "SHORT":
                user_text = request.form.get(f"q_{q['id']}", "")
                user_ans = user_text
                is_correct, kw_hit, kw_total = grade_short_answer(user_text, q.get("keywords", []))
            elif q["qtype"] == "2D_SIMULATOR":
                completed = SIMULATOR_PROGRESS.get(user, {}).get("completed_tasks", 0)
                is_correct = completed >= 8
                user_ans = f"{completed}/8 작업 완료"

            if is_correct:
                correct += 1
            else:
                add_wrong_note(user, q["id"], "복습")
                subject = q.get("subject", "기타")
                weak_points[subject] = weak_points.get(subject, 0) + 1

            details.append({"q": q, "is_correct": is_correct, "user_ans": user_ans, "picked_idx": picked_idx, "kw_hit": kw_hit, "kw_total": kw_total})

        score = round((correct / total) * 100)
        ATTEMPTS.append({"user": user, "exam_type": exam_type, "year": year, "score": score, "correct": correct, "total": total, "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        detail_html = ""
        for i, d in enumerate(details, start=1):
            q = d["q"]
            if q.get("qtype") == "2D_SIMULATOR":
                detail_html += f"<div class='card'><h3>🛠️ 실기 시뮬레이션 - {d['user_ans']}</h3><div class='ok' style='font-size:18px;padding:20px;text-align:center;'>✅ 모든 작업 완료</div></div>"
                continue
            status = f"<span class='ok'>✅ 정답</span>" if d["is_correct"] else f"<span class='bad'>❌ 오답</span>"
            detail_html += f"<div class='card'><div style='display:flex;justify-content:space-between;'><div><span class='pill'>{q.get('subject', '시험')}</span><h3>문제 {i}. {q['prompt']}</h3></div><div>{status}</div></div>"
            
            if q["qtype"] == "MCQ":
                for c_idx, c in enumerate(q["choices"]):
                    is_ans = c_idx == q["answer"]
                    is_picked = c_idx == d["picked_idx"]
                    cls = "choice-explain correct" if is_ans else "choice-explain wrong"
                    mark = "✅" if is_ans else "❌"
                    pick = " ← 내 답" if is_picked else ""
                    detail_html += f"<div class='{cls}'><strong>{chr(65+c_idx)}. {mark}{pick}</strong><br/>{c}<br/><em>{q['choice_explanations'][c_idx]}</em></div>"
            elif q["qtype"] == "SHORT":
                detail_html += f"<strong>학생 답변:</strong><pre>{d['user_ans'] or '(무응답)'}</pre><strong>채점:</strong> {d['kw_hit']}/{d['kw_total']} 키워드<br/><strong>모범 답안:</strong><pre>{q.get('sample_answer', '-')}</pre>"
            
            detail_html += f"<div class='analysis-box'><strong>분석:</strong> {q.get('analysis', q.get('explanation', '-'))}</div></div>"

        weakness_html = "<h3>📊 약점 분석</h3>"
        if weak_points:
            weakness_html += "<ul>" + "".join(f"<li><strong>{s}</strong>: {c}개 오답</li>" for s, c in sorted(weak_points.items(), key=lambda x: x[1], reverse=True)) + "</ul>"
        else:
            weakness_html += "<p class='ok'>완벽합니다! 🎉</p>"

        body = f"""
        <div class="score-display">
          <div class="label">📊 시험 결과</div>
          <div class="score">{score}점</div>
          <div class="label">{correct}/{total} 정답</div>
          <div class="label">{"🎉 합격!" if score >= 60 else "재응시 권장"}</div>
        </div>
        <div class="card">{weakness_html}</div>
        <div class="row">
          <a class="btn btn-light" href="/exam/{exam_type}/{year}?user={user}">다시 풀기</a>
          <a class="btn btn-light" href="/">홈</a>
        </div>
        <hr style="margin:30px 0;opacity:0.3">
        <h2>📖 상세 답안지</h2>
        {detail_html}
        """
        return render_template_string(BASE_HTML, body=body)

    if exam_type == "PRACTICAL_WORK":
        body = f"""
        <div class="header"><h1>🛠️ 실기 시뮬레이션</h1><p>모든 작업을 완료하세요</p></div>
        <div class="card">
          <div style="margin-bottom:20px;padding:15px;background:#f0f9ff;border-left:4px solid #667eea;border-radius:8px;">
            <label><strong>🔧 동관 길이 입력 (mm):</strong><br/>
            <input type="number" id="tubeLength" value="100" min="50" max="200" style="width:150px;padding:8px;margin-top:8px;border:2px solid #667eea;border-radius:6px;font-size:14px;"/></label>
            <p style="font-size:12px;color:#666;margin-top:8px;">위에서 길이를 입력한 후 "1️⃣ 동관절단" 버튼을 클릭하세요</p>
          </div>
          <div style="margin-bottom:20px;padding:15px;background:#fff9e6;border-left:4px solid #f5c26b;border-radius:8px;display:none;" id="bendingPanel">
            <label><strong>📐 밴딩 각도 입력 (°):</strong><br/>
            <input type="number" id="bendingAngle" value="45" min="0" max="180" style="width:150px;padding:8px;margin-top:8px;border:2px solid #f5c26b;border-radius:6px;font-size:14px;"/></label>
            <p style="font-size:12px;color:#666;margin-top:8px;">각도를 입력하고 "3️⃣ 밴딩" 버튼을 클릭하면 동관이 휘어집니다</p>
          </div>
          <div id="simulator-container" style="width:100%;height:900px;border:2px solid #e5e7eb;border-radius:8px;overflow:hidden;">
            <canvas id="simulatorCanvas"></canvas>
          </div>
          <div style="margin:20px 0;">
            <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%;"></div></div>
            <div id="progress-display">0/8 작업 완료</div>
          </div>
          <form method="post"><input type="hidden" name="user" value="{user}"/><div class="row"><button class="btn btn-success" type="submit">✅ 제출하기</button><a class="btn btn-light" href="/">취소</a></div></form>
        </div>
        <script>{SIMULATOR_2D_JS}</script>
        """
        return render_template_string(BASE_HTML, body=body)

    if exam_type == "PRACTICAL_WRITTEN":
        q_html = "".join(f"<div class='card'><div style='display:flex;justify-content:space-between;'><h3>문제 {i}/{len(questions)}</h3><div class='pill'>{q.get('subject', '실기')}</div></div><h4>{q['prompt']}</h4><textarea name='q_{q['id']}' placeholder='답변을 입력하세요'></textarea></div>" for i, q in enumerate(questions, 1))
        body = f"""
        <div class="header"><h1>✍️ {year}년 실기 필답형</h1><p>총 {len(questions)}문제</p></div>
        <div class="card" style="background:#f0f9ff;border-left:4px solid #667eea;"><strong>📌 안내:</strong> 모든 문제를 풀 필요는 없습니다. 작성하지 않은 문제는 자동으로 0점입니다.</div>
        <form method="post"><input type="hidden" name="user" value="{user}"/>{q_html}<div class="row"><button class="btn btn-success" type="submit">✅ 제출하기</button><a class="btn btn-light" href="/">취소</a></div></form>
        """
        return render_template_string(BASE_HTML, body=body)

    q_html = ""
    for i, q in enumerate(questions, 1):
        choices_html = "".join(f'<label><input type="radio" name="q_{q["id"]}" value="{c_idx}"/><strong>{chr(65+c_idx)}.</strong> {c}</label>' for c_idx, c in enumerate(q['choices']))
        q_html += f"<div class='card'><div style='display:flex;justify-content:space-between;'><h3>문제 {i}/{len(questions)}</h3><div class='pill'>{q['subject']}</div></div><h4>{q['prompt']}</h4><div>{choices_html}</div></div>"
    
    body = f"""
    <div class="header"><h1>📝 {year}년 필기 시험</h1><p>총 {len(questions)}문제</p></div>
    <div class="card" style="background:#f0f9ff;border-left:4px solid #667eea;"><strong>📌 안내:</strong> 모든 문제를 풀 필요는 없습니다. 선택하지 않은 문제는 자동으로 0점입니다.</div>
    <form method="post"><input type="hidden" name="user" value="{user}"/>{q_html}<div class="row"><button class="btn btn-success" type="submit">✅ 제출하기</button><a class="btn btn-light" href="/">취소</a></div></form>
    """
    return render_template_string(BASE_HTML, body=body)

@app.route("/api/simulator-progress", methods=["POST"])
def save_simulator_progress():
    data = request.get_json() or {}
    user = data.get("user", "demo")
    completed_tasks = data.get("completed_tasks", 0)
    if user not in SIMULATOR_PROGRESS:
        SIMULATOR_PROGRESS[user] = {}
    SIMULATOR_PROGRESS[user]["completed_tasks"] = completed_tasks
    return jsonify({"status": "saved"})

@app.route("/planner")
def planner():
    user = request.args.get("user", "demo")
    PLANNER_HTML = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📅 데일리 플래너</title>
        <style>
            *{margin:0;padding:0;box-sizing:border-box}
            body{font-family:'Segoe UI','맑은 고딕',sans-serif;background:linear-gradient(135deg,#f0f4f8,#e8f1f8);min-height:100vh;padding:20px}
            .container{max-width:1200px;margin:0 auto}
            header{text-align:center;margin-bottom:40px}
            h1{color:#2c5aa0;font-size:32px;margin-bottom:10px}
            .controls{display:flex;gap:10px;justify-content:center;margin-bottom:30px;flex-wrap:wrap}
            .btn{padding:10px 20px;border:none;border-radius:6px;cursor:pointer;font-size:14px;font-weight:bold;transition:0.3s}
            .btn-primary{background:#4d7ec7;color:white}
            .btn-primary:hover{background:#2c5aa0}
            .btn-primary.active{background:#2c5aa0;box-shadow:0 0 10px rgba(44,90,160,0.4)}
            .calendar-container{background:white;border-radius:12px;padding:15px;box-shadow:0 4px 12px rgba(0,0,0,0.1);margin-bottom:30px}
            .calendar-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
            .calendar-header h2{color:#2c5aa0;font-size:24px}
            .nav-btn{padding:8px 12px;background:#e0e8f0;border:none;cursor:pointer;border-radius:4px;font-weight:bold}
            .nav-btn:hover{background:#c0d0e0}
            .weekdays{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-bottom:5px}
            .weekday{text-align:center;font-weight:bold;color:#4d7ec7;padding:6px;border-bottom:2px solid #4d7ec7;font-size:12px}
            .days{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
            .day{min-height:75px;padding:6px;border:1px solid #e0e8f0;border-radius:4px;cursor:pointer;background:white;transition:0.3s;overflow:hidden}
            .day:hover{border-color:#4d7ec7;background:#f0f4f8}
            .day.other-month{color:#ccc;background:#f8f8f8}
            .day.today{background:#d4e6f1;border-color:#2c5aa0;font-weight:bold}
            .day-number{font-weight:bold;color:#1a3a4a;margin-bottom:2px;font-size:13px}
            .day-tasks{font-size:10px;color:#666}
            .task-item{background:#e8f4f8;padding:2px 4px;margin:1px 0;border-radius:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:10px}
            .task-item.done{text-decoration:line-through;opacity:0.6}
            .modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:1000;justify-content:center;align-items:center}
            .modal.active{display:flex}
            .modal-content{background:white;padding:30px;border-radius:12px;width:90%;max-width:500px;max-height:80vh;overflow-y:auto}
            .modal-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;border-bottom:2px solid #e0e8f0;padding-bottom:15px}
            .modal-header h3{color:#2c5aa0;font-size:20px}
            .close-btn{cursor:pointer;font-size:24px;color:#999}
            .task-form{display:flex;flex-direction:column;gap:15px}
            .form-group{display:flex;flex-direction:column}
            .form-group label{font-weight:bold;color:#1a3a4a;margin-bottom:5px}
            .form-group input,.form-group textarea{padding:8px;border:1px solid #ddd;border-radius:4px;font-family:inherit}
            .form-group textarea{resize:vertical;min-height:60px}
            .tasks-list{margin-top:20px}
            .tasks-list h4{color:#2c5aa0;margin-bottom:10px}
            .tasks-list li{list-style:none;display:flex;align-items:center;padding:8px;background:#f8f8f8;margin:5px 0;border-radius:4px;cursor:pointer;transition:0.2s}
            .tasks-list li:hover{background:#e8f4f8}
            .tasks-list input[type="checkbox"]{margin-right:10px;cursor:pointer}
            .delete-task{margin-left:auto;cursor:pointer;color:red;font-weight:bold}
            .progress-bar{width:100%;height:25px;background:#e0e8f0;border-radius:12px;overflow:hidden;margin-top:10px}
            .progress-fill{height:100%;background:linear-gradient(90deg,#52c41a,#95de64);transition:width 0.3s;display:flex;align-items:center;justify-content:center;color:white;font-size:12px;font-weight:bold}
            .form-buttons{display:flex;gap:10px;justify-content:flex-end;margin-top:20px}
            .btn-submit,.btn-cancel{padding:10px 20px;border:none;border-radius:6px;cursor:pointer;font-weight:bold;transition:0.3s}
            .btn-submit{background:#52c41a;color:white}
            .btn-submit:hover{background:#389e0d}
            .btn-cancel{background:#ff4d4f;color:white}
            .btn-cancel:hover{background:#d9363e}
            .stats{display:flex;gap:20px;margin-top:20px;justify-content:space-around}
            .stat-card{background:#f0f4f8;padding:15px;border-radius:8px;text-align:center;flex:1}
            .stat-value{font-size:24px;font-weight:bold;color:#2c5aa0}
            .stat-label{font-size:12px;color:#666;margin-top:5px}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>📅 데일리 플래너</h1>
                <p>계획을 세우고 진행률을 추적하세요</p>
            </header>

            <div class="controls">
                <button class="btn btn-primary active" data-range="month">📅 1달</button>
                <button class="btn btn-primary" data-range="3weeks">📆 3주</button>
                <button class="btn btn-primary" data-range="2weeks">📋 2주</button>
                <button class="btn btn-primary" onclick="location.href='/'">← 돌아가기</button>
            </div>

            <div class="calendar-container">
                <div class="calendar-header">
                    <button class="nav-btn" onclick="prevMonth()">◀ 이전</button>
                    <h2 id="currentMonth">2026년 8월</h2>
                    <button class="nav-btn" onclick="nextMonth()">다음 ▶</button>
                </div>

                <div class="weekdays">
                    <div class="weekday">일</div>
                    <div class="weekday">월</div>
                    <div class="weekday">화</div>
                    <div class="weekday">수</div>
                    <div class="weekday">목</div>
                    <div class="weekday">금</div>
                    <div class="weekday">토</div>
                </div>

                <div class="days" id="calendarDays"></div>
            </div>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value" id="totalTasks">0</div>
                    <div class="stat-label">총 계획</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="completedTasks">0</div>
                    <div class="stat-label">완료된 계획</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="progressPercent">0%</div>
                    <div class="stat-label">진행률</div>
                </div>
            </div>
        </div>

        <div class="modal" id="plannerModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 id="modalTitle">2026년 8월 28일</h3>
                    <span class="close-btn" onclick="closeModal()">&times;</span>
                </div>
                
                <div id="recommendationBox" style="display:none;background:#f0f4f8;padding:15px;border-left:4px solid #4d7ec7;margin:15px 0;border-radius:6px;">
                    <h4 style="color:#2c5aa0;margin-bottom:10px;">💡 오늘의 학습 추천</h4>
                    <p id="recommendationText" style="color:#1a3a4a;margin-bottom:15px;line-height:1.6;"></p>
                    <h5 style="color:#2c5aa0;margin-top:15px;margin-bottom:8px;">📚 학습 팁:</h5>
                    <ul id="tipsList" style="margin-left:20px;color:#1a3a4a;"></ul>
                </div>
                
                <div class="task-form">
                    <div class="form-group">
                        <label>📝 계획 입력 (무엇을 할건가요?)</label>
                        <input type="text" id="taskInput" placeholder="예: 시험 공부하기, 운동하기...">
                    </div>
                    <div class="form-buttons">
                        <button class="btn-submit" onclick="addTask()">+ 계획 추가</button>
                        <button class="btn-cancel" onclick="closeModal()">닫기</button>
                    </div>
                </div>
                <div class="tasks-list">
                    <h4>📋 이 날짜의 계획들</h4>
                    <ul id="tasksList"></ul>
                    <div class="progress-bar">
                        <div class="progress-fill" id="dayProgress" style="width:0%">0%</div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            const USER = '{user}';
            let currentDate = new Date();
            let viewRange = 'month';
            let plannerData = {};
            let selectedDate = null;

            async function loadPlannerData(){
                try{
                    const res = await fetch('/api/planner/get?user='+USER+'&month='+currentDate.getFullYear()+'-'+(currentDate.getMonth()+1));
                    plannerData = await res.json();
                    renderCalendar();
                    updateStats();
                }catch(e){console.error(e)}
            }

            function getDateKey(d){return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate()}
            function formatDate(d){return d.getFullYear()+'년 '+(d.getMonth()+1)+'월 '+d.getDate()+'일'}

            function renderCalendar(){
                const year = currentDate.getFullYear();
                const month = currentDate.getMonth();
                const firstDay = new Date(year,month,1);
                const lastDay = new Date(year,month+1,0);
                const startDate = new Date(firstDay);
                const day = firstDay.getDay();
                const offset = (day === 0) ? 6 : (day - 1);
                startDate.setDate(startDate.getDate() - offset);
                
                const container = document.getElementById('calendarDays');
                container.innerHTML = '';
                
                let displayWeeks = 6;
                if(viewRange === '2weeks'){displayWeeks = 2}
                else if(viewRange === '3weeks'){displayWeeks = 3}

                const today = new Date();
                for(let i=0;i<displayWeeks*7;i++){
                    const d = new Date(startDate);d.setDate(d.getDate()+i);
                    const dayEl = document.createElement('div');
                    dayEl.className = 'day';
                    if(d.getMonth() !== month){dayEl.classList.add('other-month')}
                    if(d.toDateString() === today.toDateString()){dayEl.classList.add('today')}
                    
                    const dateKey = getDateKey(d);
                    const dayData = plannerData[dateKey] || {tasks:[]};
                    const tasks = dayData.tasks || [];
                    const doneTasks = tasks.filter(t => t.done).length;
                    
                    dayEl.innerHTML = `<div class="day-number">${d.getDate()}</div>`;
                    tasks.slice(0,2).forEach(t => {
                        const cls = t.done ? 'task-item done' : 'task-item';
                        dayEl.innerHTML += `<div class="${cls}">✓ ${t.text}</div>`;
                    });
                    if(tasks.length > 2){dayEl.innerHTML += `<div class="task-item" style="font-size:10px">+${tasks.length-2}개 더</div>`}
                    
                    dayEl.onclick = () => openModal(d);
                    container.appendChild(dayEl);
                }

                document.getElementById('currentMonth').textContent = year+'년 '+(month+1)+'월';
            }

            function openModal(d){
                selectedDate = d;
                const dateKey = getDateKey(d);
                const dayData = plannerData[dateKey] || {tasks:[]};
                document.getElementById('modalTitle').textContent = formatDate(d);
                document.getElementById('taskInput').value = '';
                
                const recBox = document.getElementById('recommendationBox');
                if(dayData.recommendation){
                    recBox.style.display = 'block';
                    document.getElementById('recommendationText').textContent = dayData.recommendation;
                    const tipsList = document.getElementById('tipsList');
                    tipsList.innerHTML = '';
                    (dayData.tips || []).forEach(tip => {
                        const li = document.createElement('li');
                        li.textContent = tip;
                        li.style.marginBottom = '8px';
                        tipsList.appendChild(li);
                    });
                } else {
                    recBox.style.display = 'none';
                }
                
                const tasksList = document.getElementById('tasksList');
                tasksList.innerHTML = '';
                const tasks = dayData.tasks || [];
                tasks.forEach((t,idx) => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <input type="checkbox" ${t.done?'checked':''} onchange="toggleTask('${dateKey}',${idx})">
                        <span>${t.text}</span>
                        <span class="delete-task" onclick="deleteTask('${dateKey}',${idx})">✕</span>
                    `;
                    tasksList.appendChild(li);
                });
                
                const done = tasks.filter(t => t.done).length;
                const total = tasks.length;
                const pct = total > 0 ? Math.round(done/total*100) : 0;
                const progressFill = document.getElementById('dayProgress');
                progressFill.style.width = pct+'%';
                progressFill.textContent = pct+'%';
                
                document.getElementById('plannerModal').classList.add('active');
            }

            function closeModal(){
                document.getElementById('plannerModal').classList.remove('active');
                selectedDate = null;
            }

            async function addTask(){
                const text = document.getElementById('taskInput').value.trim();
                if(!text || !selectedDate) return;
                
                const dateKey = getDateKey(selectedDate);
                await fetch('/api/planner/save',{
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify({user:USER,date:dateKey,task:{text:text,done:false}})
                });
                
                loadPlannerData();
                openModal(selectedDate);
            }

            async function toggleTask(dateKey,idx){
                if(!plannerData[dateKey]) return;
                plannerData[dateKey].tasks[idx].done = !plannerData[dateKey].tasks[idx].done;
                await fetch('/api/planner/save',{
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify({user:USER,date:dateKey,tasks:plannerData[dateKey].tasks})
                });
                loadPlannerData();
                openModal(selectedDate);
            }

            async function deleteTask(dateKey,idx){
                if(!plannerData[dateKey]) return;
                plannerData[dateKey].tasks.splice(idx,1);
                await fetch('/api/planner/delete',{
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body:JSON.stringify({user:USER,date:dateKey,taskIndex:idx})
                });
                loadPlannerData();
                openModal(selectedDate);
            }

            function prevMonth(){
                currentDate.setMonth(currentDate.getMonth()-1);
                loadPlannerData();
            }

            function nextMonth(){
                currentDate.setMonth(currentDate.getMonth()+1);
                loadPlannerData();
            }

            function updateStats(){
                let total = 0, completed = 0;
                Object.values(plannerData).forEach(d => {
                    d.tasks = d.tasks || [];
                    total += d.tasks.length;
                    completed += d.tasks.filter(t => t.done).length;
                });
                document.getElementById('totalTasks').textContent = total;
                document.getElementById('completedTasks').textContent = completed;
                const pct = total > 0 ? Math.round(completed/total*100) : 0;
                document.getElementById('progressPercent').textContent = pct+'%';
            }

            document.querySelectorAll('[data-range]').forEach(btn => {
                btn.onclick = (e) => {
                    document.querySelectorAll('[data-range]').forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    viewRange = e.target.dataset.range;
                    renderCalendar();
                };
            });

            loadPlannerData();
        </script>
    </body>
    </html>
    """.replace('{user}', user)
    return render_template_string(PLANNER_HTML)

def get_default_study_plan():
    """기능사 합격을 위한 4개월 학습 계획 (2026년 9월~12월)"""
    plan = {
        # 9월 1주 (기초 다지기)
        "2026-9-1": {"tasks": [{"text": "🎓 냉동기계 기본개념 학습", "done": False}, {"text": "📖 냉매의 성질 복습", "done": False}], "recommendation": "냉동기계의 작동 원리와 냉매의 역할을 이해하는 것이 기초입니다. 교재 1-2장을 정독하고, 각 장치의 기능을 그림으로 그려보세요.", "tips": ["냉매의 상변화 과정을 반복해서 이해하기", "동영상 강의로 시각적 학습하기", "핵심 용어를 노트에 정리하기"]},
        "2026-9-2": {"tasks": [{"text": "📝 공기조화 기초 개념 정리", "done": False}, {"text": "✍️ 필기 핵심용어 암기", "done": False}], "recommendation": "공기조화 시스템의 구조와 습공기선도를 이해해야 합니다. 건구온도, 습구온도, 절대습도 등 기본 용어를 완벽히 암기하세요.", "tips": ["습공기선도(심롤선도) 그리는 연습", "온도와 습도 관계식 암기", "기본 용어 카드 만들기"]},
        "2026-9-3": {"tasks": [{"text": "🎯 2014년 필기 기출 1-15번 풀이", "done": False}], "recommendation": "가장 기본적인 기출문제입니다. 문제를 풀 때 선택지마다 왜 맞고 왜 틀렸는지 설명할 수 있을 때까지 복습하세요.", "tips": ["오답노트 작성하기", "각 선택지 분석하기", "시간 재고 풀기"]},
        "2026-9-4": {"tasks": [{"text": "📚 약점 분석 및 복습", "done": False}], "recommendation": "9월 1-3일 학습 내용에서 틀린 부분을 정리하고, 같은 주제의 문제를 다시 풀어보세요.", "tips": ["오답 부분 재학습", "유사 문제 찾아서 풀기", "약점 부분 강의영상 재시청"]},
        "2026-9-5": {"tasks": [{"text": "💪 모의고사 풀이 (기초)", "done": False}], "recommendation": "주간 첫 번째 모의고사입니다. 시간 제약 없이 풀어보고, 정답률을 기록해두세요. 60점 이상이 목표입니다.", "tips": ["편한 환경에서 풀기", "정답률 기록", "틀린 문제 분류하기"]},
        
        # 9월 2주
        "2026-9-8": {"tasks": [{"text": "🔄 2014년 필기 16-30번 풀이", "done": False}]},
        "2026-9-9": {"tasks": [{"text": "📖 냉동기계 심화 개념 학습", "done": False}]},
        "2026-9-10": {"tasks": [{"text": "✍️ 중요 공식 정리 및 암기", "done": False}]},
        
        # 9월 3주
        "2026-9-15": {"tasks": [{"text": "🎯 2014년 필기 31-45번 풀이", "done": False}]},
        "2026-9-16": {"tasks": [{"text": "📚 2015년 필기 1-15번 풀이", "done": False}]},
        "2026-9-17": {"tasks": [{"text": "💪 주간 복습 및 약점 정리", "done": False}]},
        
        # 9월 4주
        "2026-9-22": {"tasks": [{"text": "🎯 2015년 필기 16-45번 풀이", "done": False}]},
        "2026-9-23": {"tasks": [{"text": "🔄 2016년 필기 1-15번 풀이", "done": False}]},
        "2026-9-24": {"tasks": [{"text": "📚 월간 종합 복습", "done": False}]},
        
        # 10월 1주 (심화 학습)
        "2026-10-1": {"tasks": [{"text": "🎯 2016년 필기 16-45번 풀이", "done": False}]},
        "2026-10-2": {"tasks": [{"text": "📖 냉동사이클 심화 학습", "done": False}]},
        "2026-10-3": {"tasks": [{"text": "✍️ 응축기, 증발기 이론 정리", "done": False}]},
        
        # 10월 2주
        "2026-10-6": {"tasks": [{"text": "🎯 2017년 필기 1-30번 풀이", "done": False}]},
        "2026-10-7": {"tasks": [{"text": "📚 2017년 필기 31-45번 풀이", "done": False}]},
        "2026-10-8": {"tasks": [{"text": "💪 약점 부분 집중 복습", "done": False}]},
        
        # 10월 3주
        "2026-10-13": {"tasks": [{"text": "🎯 2018년 필기 1-30번 풀이", "done": False}]},
        "2026-10-14": {"tasks": [{"text": "📚 2018년 필기 31-45번 풀이", "done": False}]},
        "2026-10-15": {"tasks": [{"text": "🔄 모의고사 풀이 (심화)", "done": False}]},
        
        # 10월 4주
        "2026-10-20": {"tasks": [{"text": "🎯 2019년 필기 1-30번 풀이", "done": False}]},
        "2026-10-21": {"tasks": [{"text": "📚 2019년 필기 31-45번 풀이", "done": False}]},
        "2026-10-22": {"tasks": [{"text": "💪 월간 모의고사", "done": False}]},
        
        # 11월 1주 (실기 필답형)
        "2026-11-3": {"tasks": [{"text": "🎯 2020년 필기 1-30번 풀이", "done": False}]},
        "2026-11-4": {"tasks": [{"text": "📚 2020년 필기 31-45번 풀이", "done": False}]},
        "2026-11-5": {"tasks": [{"text": "✍️ 필기 전 영역 총정리", "done": False}]},
        
        # 11월 2주
        "2026-11-10": {"tasks": [{"text": "🛠️ 실기 필답형 1번 (과열도) 연습", "done": False}]},
        "2026-11-11": {"tasks": [{"text": "🛠️ 실기 필답형 2-3번 연습", "done": False}]},
        "2026-11-12": {"tasks": [{"text": "🛠️ 실기 필답형 4-5번 연습", "done": False}]},
        
        # 11월 3주
        "2026-11-17": {"tasks": [{"text": "🛠️ 실기 필답형 6-7번 연습", "done": False}]},
        "2026-11-18": {"tasks": [{"text": "🛠️ 실기 필답형 8번 연습", "done": False}]},
        "2026-11-19": {"tasks": [{"text": "💪 주간 필답형 복습", "done": False}]},
        
        # 11월 4주
        "2026-11-24": {"tasks": [{"text": "🎯 필답형 전 영역 모의고사", "done": False}]},
        "2026-11-25": {"tasks": [{"text": "📚 약점 필답형 재연습", "done": False}]},
        "2026-11-26": {"tasks": [{"text": "💪 월간 종합 복습", "done": False}]},
        
        # 12월 1주 (시뮬레이션 & 종합)
        "2026-12-1": {"tasks": [{"text": "🛠️ 실기 시뮬레이션: 동관절단", "done": False}]},
        "2026-12-2": {"tasks": [{"text": "🛠️ 실기 시뮬레이션: 플레어링-밴딩", "done": False}]},
        "2026-12-3": {"tasks": [{"text": "🛠️ 실기 시뮬레이션: 연결-용접", "done": False}]},
        
        # 12월 2주
        "2026-12-8": {"tasks": [{"text": "🛠️ 실기 시뮬레이션: 냉각-작동점검", "done": False}]},
        "2026-12-9": {"tasks": [{"text": "🎯 필기 전체 최종 복습 (중요도순)", "done": False}]},
        "2026-12-10": {"tasks": [{"text": "💪 필기 최종 모의고사", "done": False}]},
        
        # 12월 3주
        "2026-12-15": {"tasks": [{"text": "✍️ 필답형 최종 복습", "done": False}]},
        "2026-12-16": {"tasks": [{"text": "🛠️ 시뮬레이션 최종 점검", "done": False}]},
        "2026-12-17": {"tasks": [{"text": "💪 최종 종합 모의고사", "done": False}]},
        
        # 12월 4주
        "2026-12-22": {"tasks": [{"text": "🎯 약점 최종 정리", "done": False}]},
        "2026-12-23": {"tasks": [{"text": "📚 시험 전 마지막 복습", "done": False}]},
        "2026-12-24": {"tasks": [{"text": "✨ 컨디션 조절 및 휴식", "done": False}]},
    }
    return plan

@app.route("/api/planner/get")
def get_planner():
    user = request.args.get("user", "demo")
    month = request.args.get("month", str(date.today().year)+"-"+str(date.today().month))
    if user not in PLANNER_DATA:
        PLANNER_DATA[user] = get_default_study_plan()
    return jsonify(PLANNER_DATA[user])

@app.route("/api/planner/save", methods=["POST"])
def save_planner():
    data = request.get_json() or {}
    user = data.get("user", "demo")
    date_key = data.get("date", "")
    if user not in PLANNER_DATA:
        PLANNER_DATA[user] = {}
    
    if "tasks" in data:
        PLANNER_DATA[user][date_key] = {"tasks": data["tasks"]}
    elif "task" in data:
        if date_key not in PLANNER_DATA[user]:
            PLANNER_DATA[user][date_key] = {"tasks": []}
        PLANNER_DATA[user][date_key]["tasks"].append(data["task"])
    return jsonify({"status": "saved"})

@app.route("/api/planner/delete", methods=["POST"])
def delete_planner():
    data = request.get_json() or {}
    user = data.get("user", "demo")
    date_key = data.get("date", "")
    task_index = data.get("taskIndex", 0)
    
    if user in PLANNER_DATA and date_key in PLANNER_DATA[user]:
        tasks = PLANNER_DATA[user][date_key].get("tasks", [])
        if 0 <= task_index < len(tasks):
            tasks.pop(task_index)
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
