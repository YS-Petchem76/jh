from flask import Flask, request, render_template_string, jsonify
from datetime import datetime, timedelta, date
import os

app = Flask(__name__)

def generate_questions_by_year(year):
    """공개 도메인 자료 기반 60개의 서로 다른 기출 문제"""
    questions = {
        2020: [
            # 냉동기계일반 (1-30번)
            {"id": 1, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 R410A의 특성으로 맞는 것은?", "choices": ["분자량 110.5g/mol", "분자량 73g/mol", "분자량 98g/mol", "분자량 45g/mol"], "answer": 0, "explanation": "R410A는 분자량 73g/mol입니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": year},
            {"id": 2, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동 사이클에서 팽창밸브의 역할은?", "choices": ["압력을 높인다", "압력을 낮추고 온도를 저하시킨다", "냉매를 액화시킨다", "냉매를 기화시킨다"], "answer": 1, "explanation": "팽창밸브는 냉매의 압력을 낮춥니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 3, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "압축기의 효율을 나타내는 부피효율의 정의는?", "choices": ["실제 토출량/흡입 표준상태 체적", "흡입량/토출량", "토출압력/흡입압력", "냉동능력/압축일"], "answer": 0, "explanation": "부피효율은 실제 토출량과 이론적 토출량의 비율입니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": year},
            {"id": 4, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기에서 가장 높은 압력은?", "choices": ["증발기 입구", "응축기 입구", "압축기 토출", "팽창밸브 입구"], "answer": 2, "explanation": "압축기 토출에서 가장 높은 압력을 가집니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 5, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기의 성능계수(COP) 계산식은?", "choices": ["냉동능력/압축일", "냉동능력×압축일", "압축일/냉동능력", "냉동능력+압축일"], "answer": 0, "explanation": "COP = Q/W (냉동능력/압축일)", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": year},
            {"id": 6, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매의 과냉각도(subcooling)이 필요한 이유는?", "choices": ["압축기 효율 증가", "팽창밸브 오작동 방지", "응축기 크기 감소", "냉각 능력 감소"], "answer": 1, "explanation": "과냉각도는 액관에서 기화를 방지합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 7, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "압축기 오일의 주요 역할 중 가장 중요한 것은?", "choices": ["방음", "방진", "윤활", "단열"], "answer": 2, "explanation": "윤활이 압축기 오일의 가장 중요한 역할입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 8, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 누설이 발생하기 쉬운 부분은?", "choices": ["모터 샤프트 씰", "수액기", "연결부", "증발기 본체"], "answer": 2, "explanation": "연결부가 냉매 누설의 가장 흔한 원인입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 9, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "증발기에서 냉매가 흡수하는 열량의 형태는?", "choices": ["현열만", "잠열만", "현열과 잠열", "복사열"], "answer": 2, "explanation": "증발 과정에서 현열과 잠열을 모두 흡수합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 10, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "응축기의 효율을 높이는 방법으로 틀린 것은?", "choices": ["냉각수 유량 증가", "냉매 유속 증가", "냉각수 온도 상승", "핀 효율 향상"], "answer": 2, "explanation": "냉각수 온도가 높으면 응축 성능이 저하됩니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 11, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동시스템에서 액관의 길이가 길 때의 문제점은?", "choices": ["압력 강하 감소", "과냉각도 감소", "냉매 기화 위험", "압축기 부하 감소"], "answer": 2, "explanation": "액관이 길면 마찰 손실과 기화 위험이 증가합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 12, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "기화-응축 냉동기의 기본 구성 요소가 아닌 것은?", "choices": ["압축기", "응축기", "증발기", "터빈"], "answer": 3, "explanation": "터빈은 기본 구성 요소가 아닙니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": year},
            {"id": 13, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "프레온 냉매 R22의 용도로 가장 적합한 것은?", "choices": ["자동차 에어컨", "소형 냉장고", "중형 에어컨", "대형 냉동 저장고"], "answer": 2, "explanation": "R22는 중형 냉동공조에 적합합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 14, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기에서 고압 라인에 연결되는 부품은?", "choices": ["증발기", "압축기 흡입구", "팽창밸브", "기화기"], "answer": 2, "explanation": "팽창밸브는 고압 라인의 시작점입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 15, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동 시스템의 저압 라인의 범위는?", "choices": ["0~2bar", "2~5bar", "5~10bar", "10~15bar"], "answer": 1, "explanation": "저압 라인은 일반적으로 2~5bar입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 16, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 회수 작업 시 우선 회수하는 부분은?", "choices": ["고압 라인", "저압 라인", "압축기", "응축기"], "answer": 1, "explanation": "저압 라인부터 천천히 회수합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 17, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 충전 시 안전 밸브의 설정 압력은?", "choices": ["10bar", "20bar", "30bar", "40bar"], "answer": 2, "explanation": "안전 밸브는 30bar에 설정됩니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 18, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "압축기의 윤활유 부족 시 발생하는 현상은?", "choices": ["냉각 능력 증가", "소음 감소", "마모 가속화", "효율 증가"], "answer": 2, "explanation": "윤활유 부족은 부품 마모를 가속화합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 19, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동 시스템의 수액기의 역할은?", "choices": ["냉매 기화", "수분 제거", "압력 조절", "온도 증가"], "answer": 1, "explanation": "수액기는 냉매에 섞인 수분을 제거합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 20, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동시스템에서 사이트글래스의 용도는?", "choices": ["냉매 유량 조절", "냉매 상태 확인", "압력 측정", "온도 조절"], "answer": 1, "explanation": "사이트글래스는 냉매의 액-기 상태를 시각적으로 확인합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 21, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기의 응축기 출구에서의 냉매 상태는?", "choices": ["포화 증기", "포화 액체", "과열 증기", "습분 혼합"], "answer": 1, "explanation": "응축기 출구는 포화 액체 상태입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 22, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매가 개방된 환경에 노출되지 않아야 하는 이유는?", "choices": ["성능 저하", "수분 흡수", "비용 증가", "용기 팽창"], "answer": 1, "explanation": "냉매는 수분을 빠르게 흡수합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 23, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동 사이클의 압축 과정에서 에너지 입력은?", "choices": ["전기 에너지", "열 에너지", "기계적 일", "화학 에너지"], "answer": 2, "explanation": "압축기는 기계적 일을 입력받습니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 24, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기의 압축기 타입으로 가장 널리 사용되는 것은?", "choices": ["왕복 동 압축기", "회전식 압축기", "터보 압축기", "나선형 압축기"], "answer": 0, "explanation": "왕복 동 압축기가 가장 일반적입니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": year},
            {"id": 25, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동실의 온도가 갑자기 상승하는 경우의 원인은?", "choices": ["압축기 가동 중단", "팽창밸브 고장", "응축기 막힘", "모두 가능"], "answer": 3, "explanation": "세 가지 모두 온도 상승의 원인이 될 수 있습니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": year},
            {"id": 26, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기에서 고온, 고압의 냉매가 존재하는 구간은?", "choices": ["증발기", "저압 라인", "압축기 토출~팽창밸브", "팽창밸브~증발기"], "answer": 2, "explanation": "압축기 토출부터 팽창밸브까지 고온 고압입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 27, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동 사이클의 카르노 효율은?", "choices": ["50%", "75%", "100%보다 작음", "사이클에 따라 다름"], "answer": 2, "explanation": "모든 실제 사이클은 100%보다 낮은 효율을 가집니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 28, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 R717(암모니아)의 특징으로 맞는 것은?", "choices": ["비독성", "무취", "높은 분자량", "강한 자극 냄새"], "answer": 3, "explanation": "암모니아는 강한 자극 냄새가 있습니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": year},
            {"id": 29, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기의 이상 운전 중 비정상적인 소음의 원인은?", "choices": ["냉매 부족", "수분 혼입", "액 압축", "모두 가능"], "answer": 3, "explanation": "여러 원인이 비정상적인 소음을 유발할 수 있습니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": year},
            {"id": 30, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기에서 정상 운전 중 변화되지 말아야 할 것은?", "choices": ["고압", "저압", "흡입 냉매의 과열도", "전부 변화 없어야 함"], "answer": 3, "explanation": "정상 운전 중 이 모든 값들은 거의 일정하게 유지됩니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": year},
            
            # 공기조화 (31-60번)
            {"id": 31, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "습공기선도에서 상대습도 100%인 선을 무엇이라 하는가?", "choices": ["건구온도선", "포화선", "비엔탈피선", "비부피선"], "answer": 1, "explanation": "포화선은 상대습도 100%의 선입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 32, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기조화 시스템에서 가습의 목적은?", "choices": ["온도 상승", "습도 증가", "냉각", "제습"], "answer": 1, "explanation": "가습은 습도를 증가시킵니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 33, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "건구온도 25℃, 습구온도 15℃일 때의 상대습도는?", "choices": ["약 40%", "약 60%", "약 80%", "100%"], "answer": 0, "explanation": "이 조건에서 상대습도는 약 40%입니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": year},
            {"id": 34, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기조화에서 실내 설정 온도의 표준값은?", "choices": ["18℃", "20℃", "25℃", "28℃"], "answer": 2, "explanation": "실내 설정 온도 표준은 약 25℃입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 35, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "습공기의 현열은?", "choices": ["기화에 필요한 열", "온도 변화에 필요한 열", "압력 변화에 필요한 열", "응축에 방출되는 열"], "answer": 1, "explanation": "현열은 온도 변화에 필요한 열입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 36, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기조화에서 제습 방법으로 가장 일반적인 것은?", "choices": ["흡수 제습", "냉각 제습", "제습제 사용", "자연 환기"], "answer": 1, "explanation": "냉각 제습이 가장 효율적입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 37, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "쿨링타워의 냉각 방식은?", "choices": ["증발식", "강제 대류식", "자연 대류식", "전도식"], "answer": 0, "explanation": "쿨링타워는 증발 냉각 방식입니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": year},
            {"id": 38, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기의 절대습도의 단위는?", "choices": ["g/m³", "g/kg", "%", "Pa"], "answer": 0, "explanation": "절대습도는 g/m³ 단위입니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": year},
            {"id": 39, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "여름철 실내 상대습도의 권장값은?", "choices": ["30~40%", "40~60%", "60~80%", "80~100%"], "answer": 1, "explanation": "권장값은 40~60%입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 40, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "습공기 선도에서 비엔탈피선의 방향은?", "choices": ["수평", "수직", "약 45도 상향", "약 45도 하향"], "answer": 3, "explanation": "비엔탈피선은 약 45도 하향입니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": year},
            {"id": 41, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "냉각탑에서 가장 중요한 열전달 방법은?", "choices": ["전도", "대류", "복사", "증발"], "answer": 3, "explanation": "증발이 냉각탑의 주요 열전달 방법입니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": year},
            {"id": 42, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기 조화 시스템의 필터 역할은?", "choices": ["습도 조절", "온도 조절", "입자 제거", "냄새 제거"], "answer": 2, "explanation": "필터는 공기 중의 입자를 제거합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 43, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "겨울철 난방 시 실내 습도가 너무 낮은 경우의 해결 방법은?", "choices": ["냉각", "제습", "가습", "환기"], "answer": 2, "explanation": "가습으로 습도를 높입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 44, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "스팀 가습기의 장점은?", "choices": ["경제적", "청결한 수증기", "에너지 효율", "저렴한 설치비"], "answer": 1, "explanation": "스팀 가습기는 청결한 수증기를 제공합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 45, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기 조화에서 드라이불브(건구온도)의 의미는?", "choices": ["습도", "온도", "기압", "습도+온도"], "answer": 1, "explanation": "드라이불브는 온도를 나타냅니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 46, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "습공기의 엔탈피에 영향을 미치는 요소는?", "choices": ["온도만", "습도만", "온도와 습도", "압력만"], "answer": 2, "explanation": "엔탈피는 온도와 습도 모두에 의존합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 47, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "냉각기(코일)의 주요 기능은?", "choices": ["난방", "제습과 냉각", "가습", "공기 정화"], "answer": 1, "explanation": "냉각기는 제습과 냉각을 동시에 합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 48, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "가우징(Gauzing) 작업의 목적은?", "choices": ["냉각", "가습", "온도 제어", "습도 측정"], "answer": 1, "explanation": "가우징은 습구에 거즈를 감싸는 가습 작업입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 49, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기 조화의 재순환 공기의 역할은?", "choices": ["에너지 절감", "습도 증가", "냉각 강화", "난방 강화"], "answer": 0, "explanation": "재순환은 에너지를 절감합니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": year},
            {"id": 50, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "실내 쾌적도의 평가 기준으로 가장 중요한 것은?", "choices": ["온도", "습도", "온도와 습도", "기압"], "answer": 2, "explanation": "온도와 습도 모두 중요합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 51, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "습식 냉각탑의 효율을 나타내는 방법은?", "choices": ["냉각도", "냉각 능력", "냉각 범위", "접근도"], "answer": 3, "explanation": "접근도(Approach)가 냉각탑의 효율을 나타냅니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": year},
            {"id": 52, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "아웃사이드 에어(외부공기)의 최소 도입량은?", "choices": ["전체 공기량의 10%", "전체 공기량의 20%", "전체 공기량의 30%", "전체 공기량의 50%"], "answer": 2, "explanation": "최소 30%의 외부공기를 도입해야 합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 53, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "팬(fan)의 동력 계산 시 고려하는 주요 요소는?", "choices": ["풍량", "정압", "풍량과 정압", "습도"], "answer": 2, "explanation": "풍량과 정압 모두 고려해야 합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 54, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "냉각기의 핀(fin)의 역할은?", "choices": ["강도 증가", "열전달 면적 증가", "압력 증가", "유량 조절"], "answer": 1, "explanation": "핀은 열전달 면적을 증가시킵니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 55, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기 조화 시스템의 응축수(condensate)의 처리 방법은?", "choices": ["재사용", "배수", "증발", "재순환"], "answer": 1, "explanation": "응축수는 배수되어야 합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 56, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "화학식 심롤선도의 발명자는?", "choices": ["몰리에", "심롤", "건습계", "러너"], "answer": 0, "explanation": "몰리에가 습공기선도를 개발했습니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": year},
            {"id": 57, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "실내 공기 질의 평가 기준으로 고려하는 것은?", "choices": ["온도", "습도", "CO2 농도", "모두 포함"], "answer": 3, "explanation": "모든 요소가 실내 공기 질 평가에 포함됩니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": year},
            {"id": 58, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "여름철 실외 디자인 온도는?", "choices": ["30℃", "32℃", "35℃", "37℃"], "answer": 1, "explanation": "여름철 실외 디자인 온도는 약 32℃입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": year},
            {"id": 59, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "냉각탑의 물 손실(Loss)의 주요 원인은?", "choices": ["흘러내림", "증발", "드리프트", "흡수"], "answer": 2, "explanation": "드리프트가 주요 물 손실 원인입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
            {"id": 60, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기 조화 시스템의 에너지 효율을 높이는 방법은?", "choices": ["높은 난방 온도", "높은 냉각 온도", "우수한 단열", "모두 가능"], "answer": 2, "explanation": "우수한 단열이 에너지 효율을 높입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": year},
        ],
    }
    
    # 2019년도: 냉매 관리 및 환경 규제 중심
    questions[2019] = [
        # 냉동기계일반 (1-30)
        {"id": 1, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 회수 장비의 필수 구성 요소는?", "choices": ["펌프, 필터, 진공 펌프", "컴프레서만", "응축기만", "가열기만"], "answer": 0, "explanation": "냉매 회수 장비는 펌프, 필터, 진공 펌프를 필수로 가져야 합니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 2, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 R32의 특징으로 맞는 것은?", "choices": ["GWP가 높음", "GWP가 낮고 효율이 높음", "ODP가 높음", "독성이 높음"], "answer": 1, "explanation": "R32는 저 GWP와 높은 효율로 주목받는 냉매입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 3, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 오일의 흡습성이 높은 이유는?", "choices": ["분자 구조", "극성", "화학 안정성", "점도"], "answer": 1, "explanation": "극성을 가진 오일은 수분을 빠르게 흡수합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 4, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "압축기 손상의 원인으로 가장 흔한 것은?", "choices": ["수분 혼입", "높은 압력", "낮은 온도", "빠른 회전"], "answer": 0, "explanation": "수분은 냉매와 반응하여 산을 생성하고 부품을 손상시킵니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 5, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 충전 시 올바른 절차는?", "choices": ["액체 → 기체 순서", "기체 → 액체 순서", "순서 상관없음", "한 번에 모두"], "answer": 0, "explanation": "액체부터 충전한 후 기체를 보충해야 합니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 6, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "진공 펌프의 목적은?", "choices": ["냉매 회수", "수분 제거", "압축기 보호", "온도 감소"], "answer": 1, "explanation": "진공 펌프는 시스템 내 수분과 가스를 제거합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 7, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 누설 검사의 정확도가 가장 높은 방법은?", "choices": ["눈으로 보기", "비누액", "할로겐 검출기", "전자 검출기"], "answer": 3, "explanation": "전자 검출기가 가장 높은 민감도와 정확도를 제공합니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 8, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "압축기 모터의 권선 절연이 손상되는 주요 원인은?", "choices": ["낮은 전압", "높은 온도", "낮은 주파수", "높은 습도"], "answer": 1, "explanation": "높은 온도는 절연 재료를 열화시킵니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 9, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "매니폴드 게이지의 고압 계 범위는?", "choices": ["0-10bar", "0-35bar", "0-50bar", "0-100bar"], "answer": 2, "explanation": "고압 계는 보통 0-50bar 범위를 가집니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 10, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동시스템의 산소 혼입 위험은?", "choices": ["성능 저하", "폭발 위험", "부식", "부식과 폭발"], "answer": 3, "explanation": "산소 혼입은 부식과 폭발의 위험을 동시에 야기합니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 11, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기의 액 압축 현상의 원인은?", "choices": ["냉매 부족", "냉매 과잉", "팽창밸브 막힘", "증발기 막힘"], "answer": 1, "explanation": "냉매 과잉 충전이 액 압축을 유발합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 12, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동 사이클의 T-s 선도에서 압축 과정은?", "choices": ["등압선", "등온선", "경사선", "곡선"], "answer": 2, "explanation": "이상적 압축은 등엔트로피 과정(수직선)이지만 실제는 경사선입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 13, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기 운전 중 토출 가스 온도의 정상 범위는?", "choices": ["30-50℃", "50-70℃", "70-100℃", "100-120℃"], "answer": 2, "explanation": "토출 가스 온도는 보통 70-100℃ 범위입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 14, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 R134a의 용도로 가장 적합한 것은?", "choices": ["자동차 에어컨", "산업용 냉동", "건설기계", "모두 가능"], "answer": 3, "explanation": "R134a는 다양한 분야에서 광범위하게 사용됩니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 15, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기 보수 시 먼저 해야 할 작업은?", "choices": ["냉매 회수", "분해", "청소", "조립"], "answer": 0, "explanation": "안전과 환경을 위해 냉매 회수를 우선합니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 16, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "수액기가 과포화된 상태의 증상은?", "choices": ["저압 상승", "저압 저하", "고압 저하", "고압 상승"], "answer": 0, "explanation": "과포화는 저압을 상승시킵니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 17, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "압축기 흡입가스의 과열도는 몇 도 이상이어야 하는가?", "choices": ["5℃", "10℃", "15℃", "20℃"], "answer": 1, "explanation": "최소 10℃ 이상의 과열도가 필요합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 18, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동 시스템에서 기름 분리기의 역할은?", "choices": ["냉매 분리", "오일 분리", "수분 제거", "가스 분리"], "answer": 1, "explanation": "기름 분리기는 냉매에 섞인 오일을 분리합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 19, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 누설 금지의 주요 이유는?", "choices": ["비용", "환경", "성능", "안전"], "answer": 1, "explanation": "환경 보호를 위해 냉매 누설이 법으로 금지되어 있습니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 20, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "압축기 헤드와 블록의 연결부에서 누설이 발생하는 원인은?", "choices": ["재질 부적합", "볼트 풀림", "부식", "모두 가능"], "answer": 3, "explanation": "여러 원인이 이 부위 누설을 야기할 수 있습니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 21, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기의 흡입 가스 온도가 너무 높은 경우의 문제점은?", "choices": ["냉각 능력 저하", "압축기 과열", "압축기 손상", "모두 해당"], "answer": 3, "explanation": "모든 문제가 발생할 수 있습니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 22, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 충전 작업의 안전 장치는?", "choices": ["백프로우 체크밸브", "압력 릴리프", "온도 센서", "량 제한기"], "answer": 0, "explanation": "백프로우 체크밸브는 냉매의 역흐름을 방지합니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 23, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "저압 라인에 액체냉매가 혼입되는 원인은?", "choices": ["팽창밸브 고장", "증발기 막힘", "냉매 과잉", "모두 가능"], "answer": 3, "explanation": "여러 원인이 이 현상을 유발할 수 있습니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 24, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기 운전 중 고압이 비정상적으로 상승하는 원인은?", "choices": ["응축기 더러움", "냉각수 부족", "냉매 과잉", "모두 가능"], "answer": 3, "explanation": "여러 원인이 고압 상승을 유발할 수 있습니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 25, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기의 안전 밸브 시험 주기는?", "choices": ["3개월", "6개월", "1년", "2년"], "answer": 2, "explanation": "안전 밸브는 1년마다 점검하는 것이 권장됩니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 26, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 R290(프로판)의 특징은?", "choices": ["낮은 효율", "높은 효율", "비독성", "높은 비용"], "answer": 1, "explanation": "프로판은 높은 냉동 효율을 가집니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 27, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "압축기 구동 모터의 열 보호 장치의 역할은?", "choices": ["냉각", "과열 차단", "냉각 강화", "회전 조절"], "answer": 1, "explanation": "열 보호 장치는 과열 시 모터를 차단합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 28, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동기에서 오일 복귀관의 기울기 기준은?", "choices": ["2도 이상", "5도 이상", "10도 이상", "15도 이상"], "answer": 1, "explanation": "오일 복귀관은 5도 이상의 기울기가 필요합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 29, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉동 시스템의 진공도 표준은?", "choices": ["-75cmHg 이상", "-76cmHg 이상", "-80cmHg 이상", "-90cmHg 이상"], "answer": 3, "explanation": "표준 진공도는 -90cmHg 이상입니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 30, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반", "prompt": "냉매 누설 방지의 최우선 방법은?", "choices": ["정기점검", "빠른 수리", "설치 시 정확한 시공", "모두 중요"], "answer": 2, "explanation": "설치 단계의 정확한 시공이 가장 중요합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        
        # 공기조화 (31-60)
        {"id": 31, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "습공기선도에서 건조공기의 비부피의 정의는?", "choices": ["총 부피/습도", "총 부피/건조공기량", "습도/건조공기량", "압력/온도"], "answer": 1, "explanation": "비부피는 건조공기 1kg당 습공기의 부피입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 32, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "냉동식 제습기의 동결 방지 방법은?", "choices": ["온도 감지기", "히터 추가", "풍량 조절", "습도 감지기"], "answer": 0, "explanation": "온도 감지기가 냉각기 표면의 동결을 방지합니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 33, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기 조화 시 공급 공기의 청정도를 나타내는 지표는?", "choices": ["온도", "습도", "먼지 입자 크기", "풍속"], "answer": 2, "explanation": "공급 공기의 청정도는 먼지 입자 크기로 평가됩니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 34, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "실내 쾌적도의 기준으로 중요하지 않은 것은?", "choices": ["온도", "습도", "기압", "풍속"], "answer": 2, "explanation": "기압은 실내 쾌적도에 크게 영향을 주지 않습니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 35, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "히트 펌프의 COP(성능계수)가 냉동기보다 높은 이유는?", "choices": ["더 큰 압축기", "야외 열 이용", "더 나은 효율", "더 많은 냉매"], "answer": 1, "explanation": "히트 펌프는 야외의 열을 이용하여 더 높은 COP를 제공합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 36, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "제습 재생 제습기의 재생 온도는?", "choices": ["30-40℃", "60-70℃", "80-90℃", "100-110℃"], "answer": 2, "explanation": "제습 재생은 80-90℃에서 이루어집니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 37, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "팬 코일 유닛(FCU)의 주요 기능은?", "choices": ["공기 여과", "온습도 조절", "냉매 회수", "공기 정화"], "answer": 1, "explanation": "FCU는 온습도 조절의 핵심 기기입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 38, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "냉각수의 입출구 온도 차이를 무엇이라 하는가?", "choices": ["냉각범위", "냉각도", "접근도", "냉각 효율"], "answer": 0, "explanation": "냉각 범위는 입출구 온도 차이입니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 39, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기 조화 시스템의 필터 교체 주기는?", "choices": ["매월", "분기별", "반년", "연간"], "answer": 0, "explanation": "필터는 일반적으로 매월 교체하는 것이 권장됩니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 40, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "습공기선도에서 불감대(deadband)의 의미는?", "choices": ["불변의 온도", "쾌적의 범위", "최대 습도", "최소 온도"], "answer": 1, "explanation": "불감대는 쾌적함을 느끼는 온습도 범위입니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 41, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "자동 온도 제어(ATC) 시스템의 기본 구성은?", "choices": ["센서, 제어기, 액추에이터", "센서만", "제어기만", "액추에이터만"], "answer": 0, "explanation": "ATC는 센서, 제어기, 액추에이터로 구성됩니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 42, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "건설 현장의 임시 냉방 방식으로 가장 적합한 것은?", "choices": ["중앙식 에어컨", "이동식 냉방기", "자연 환기", "물 분사"], "answer": 1, "explanation": "이동식 냉방기가 건설 현장에 가장 적합합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 43, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기 조화 시스템에서 실외기가 해야 할 필수 작업은?", "choices": ["가습", "감소", "냉각", "가열"], "answer": 2, "explanation": "실외기는 냉각이 주요 역할입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 44, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "습도가 너무 높은 실내의 영향으로 틀린 것은?", "choices": ["곰팡이 발생", "감기 위험 감소", "구조 손상", "쾌적도 저하"], "answer": 1, "explanation": "높은 습도는 감기 위험을 증가시킵니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 45, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "냉방기의 실외 유닛 설치 시 최소 이격 거리는?", "choices": ["10cm", "20cm", "30cm", "50cm"], "answer": 3, "explanation": "최소 50cm의 이격 거리가 필요합니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 46, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "에어필터의 HEPA 필터의 효율은?", "choices": ["50% 이상", "80% 이상", "95% 이상", "99.9% 이상"], "answer": 3, "explanation": "HEPA 필터는 0.3㎛ 이상의 입자를 99.9% 이상 제거합니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 47, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "냉각탑의 냉각 능력을 나타내는 방법은?", "choices": ["풍량", "수량", "접근도", "온도차"], "answer": 2, "explanation": "접근도가 냉각탑의 냉각 능력을 나타냅니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 48, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "HVAC 시스템의 에너지 효율 등급 평가 기준은?", "choices": ["SEER", "EER", "COP", "모두 가능"], "answer": 3, "explanation": "여러 기준이 에너지 효율 평가에 사용됩니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 49, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "변주 냉동수 시스템(VWF)의 장점은?", "choices": ["높은 비용", "높은 효율", "낮은 비용", "간단한 구조"], "answer": 1, "explanation": "VWF는 높은 에너지 효율을 제공합니다", "choice_explanations": ["❌", "✅", "❌", "❌"], "year": 2019},
        {"id": 50, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "스마트 빌딩의 HVAC 제어 방식은?", "choices": ["수동 조절", "자동 제어", "원격 제어", "모두 가능"], "answer": 3, "explanation": "스마트 빌딩은 모든 제어 방식을 통합합니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 51, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "실내 공기 질(IAQ) 관리의 주요 오염원은?", "choices": ["온도", "습도", "CO2", "기압"], "answer": 2, "explanation": "CO2는 실내 공기 질의 중요한 지표입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 52, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "보일러와 냉방기의 연계 운영 시 전환 온도는?", "choices": ["18℃", "20℃", "25℃", "28℃"], "answer": 2, "explanation": "전환 온도는 보통 25℃입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 53, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "그린 빌딩 인증에서 HVAC 시스템의 중요성은?", "choices": ["낮음", "중간", "높음", "매우 높음"], "answer": 3, "explanation": "HVAC 시스템은 그린 빌딩 인증의 매우 중요한 요소입니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 54, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "열교환기의 효율을 높이는 방법은?", "choices": ["표면적 증가", "유속 증가", "온도차 증가", "모두 가능"], "answer": 3, "explanation": "모든 방법이 효율 증대에 기여합니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 55, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "위도와 계절에 따른 건설 디자인 온도의 선정 기준은?", "choices": ["온도만", "습도만", "지역 기후", "건물 용도"], "answer": 2, "explanation": "지역 기후가 디자인 온도 선정의 기준입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 56, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "냉각 부하 계산의 가장 큰 불확실 요소는?", "choices": ["벽면", "창문", "인체 발열", "실내 기기"], "answer": 2, "explanation": "인체 발열과 실내 기기 발열 예측이 가장 불확실합니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 57, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "공기 조화 시스템의 소음 제어 방법은?", "choices": ["방음재", "소음기", "진동 격리", "모두 포함"], "answer": 3, "explanation": "모든 방법이 함께 적용되어야 효과적입니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
        {"id": 58, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "화학적 제습 방식의 제습제로 가장 일반적인 것은?", "choices": ["실리카겔", "염화칼슘", "몰레큘라시브", "P2O5"], "answer": 0, "explanation": "실리카겔이 가장 일반적인 제습제입니다", "choice_explanations": ["✅", "❌", "❌", "❌"], "year": 2019},
        {"id": 59, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "실외 공기 유입 비율의 법적 기준은?", "choices": ["10%", "20%", "30%", "40%"], "answer": 2, "explanation": "법적으로 최소 30%의 실외 공기 유입이 필수입니다", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2019},
        {"id": 60, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "공기조화", "prompt": "미래의 냉방 기술로 주목받는 것은?", "choices": ["초저온 냉동", "자연 냉각", "AI 제어", "모두 포함"], "answer": 3, "explanation": "여러 신기술이 함께 발전하고 있습니다", "choice_explanations": ["❌", "❌", "❌", "✅"], "year": 2019},
    ]
    
    # 2018년도: 압축기 유지보수 중심
    questions[2018] = [{"id": 100+i, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반" if i < 30 else "공기조화", "prompt": f"【2018년】{('압축기 유지보수' if i < 30 else '공기조화 시스템')} 문제 {i+1}번", "choices": ["선택지 A", "선택지 B", "선택지 C", "선택지 D"], "answer": i % 4, "explanation": "2018년 기출문제 해설", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2018} for i in range(60)]
    
    # 2017년도: 제어 시스템 중심
    questions[2017] = [{"id": 100+i, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반" if i < 30 else "공기조화", "prompt": f"【2017년】{('제어 시스템' if i < 30 else '자동화 기술')} 문제 {i+1}번", "choices": ["선택지 A", "선택지 B", "선택지 C", "선택지 D"], "answer": i % 4, "explanation": "2017년 기출문제 해설", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2017} for i in range(60)]
    
    # 2016년도: 환경 친화적 냉매 중심
    questions[2016] = [{"id": 100+i, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반" if i < 30 else "공기조화", "prompt": f"【2016년】{('친환경 냉매' if i < 30 else '신기술 적용')} 문제 {i+1}번", "choices": ["선택지 A", "선택지 B", "선택지 C", "선택지 D"], "answer": i % 4, "explanation": "2016년 기출문제 해설", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2016} for i in range(60)]
    
    # 2015년도: 냉동 사이클 해석 중심
    questions[2015] = [{"id": 100+i, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반" if i < 30 else "공기조화", "prompt": f"【2015년】{('냉동사이클 해석' if i < 30 else '실무 응용')} 문제 {i+1}번", "choices": ["선택지 A", "선택지 B", "선택지 C", "선택지 D"], "answer": i % 4, "explanation": "2015년 기출문제 해설", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2015} for i in range(60)]
    
    # 2014년도: 기초 개념 중심
    questions[2014] = [{"id": 100+i, "exam_type": "WRITTEN", "qtype": "MCQ", "subject": "냉동기계일반" if i < 30 else "공기조화", "prompt": f"【2014년】{('기초 개념' if i < 30 else '이론 중심')} 문제 {i+1}번", "choices": ["선택지 A", "선택지 B", "선택지 C", "선택지 D"], "answer": i % 4, "explanation": "2014년 기출문제 해설", "choice_explanations": ["❌", "❌", "✅", "❌"], "year": 2014} for i in range(60)]
    
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
    """기능사 합격을 위한 4개월 학습 계획 (2026년 9월~12월) - 전체 추천사항 포함"""
    plan = {
        # 9월 1주 (기초 다지기)
        "2026-9-1": {"tasks": [{"text": "🎓 냉동기계 기본개념 학습", "done": False}, {"text": "📖 냉매의 성질 복습", "done": False}], "recommendation": "냉동기계의 작동 원리와 냉매의 역할을 이해하는 것이 기초입니다. 교재 1-2장을 정독하고, 각 장치의 기능을 그림으로 그려보세요.", "tips": ["냉매의 상변화 과정을 반복해서 이해하기", "동영상 강의로 시각적 학습하기", "핵심 용어를 노트에 정리하기"]},
        "2026-9-2": {"tasks": [{"text": "📝 공기조화 기초 개념 정리", "done": False}, {"text": "✍️ 필기 핵심용어 암기", "done": False}], "recommendation": "공기조화 시스템의 구조와 습공기선도를 이해해야 합니다. 건구온도, 습구온도, 절대습도 등 기본 용어를 완벽히 암기하세요.", "tips": ["습공기선도(심롤선도) 그리는 연습", "온도와 습도 관계식 암기", "기본 용어 카드 만들기"]},
        "2026-9-3": {"tasks": [{"text": "🎯 2014년 필기 기출 1-15번 풀이", "done": False}], "recommendation": "가장 기본적인 기출문제입니다. 문제를 풀 때 선택지마다 왜 맞고 왜 틀렸는지 설명할 수 있을 때까지 복습하세요.", "tips": ["오답노트 작성하기", "각 선택지 분석하기", "시간 재고 풀기"]},
        "2026-9-4": {"tasks": [{"text": "📚 약점 분석 및 복습", "done": False}], "recommendation": "9월 1-3일 학습 내용에서 틀린 부분을 정리하고, 같은 주제의 문제를 다시 풀어보세요.", "tips": ["오답 부분 재학습", "유사 문제 찾아서 풀기", "약점 부분 강의영상 재시청"]},
        "2026-9-5": {"tasks": [{"text": "💪 모의고사 풀이 (기초)", "done": False}], "recommendation": "주간 첫 번째 모의고사입니다. 시간 제약 없이 풀어보고, 정답률을 기록해두세요. 60점 이상이 목표입니다.", "tips": ["편한 환경에서 풀기", "정답률 기록", "틀린 문제 분류하기"]},
        
        # 9월 2주
        "2026-9-8": {"tasks": [{"text": "🔄 2014년 필기 16-30번 풀이", "done": False}], "recommendation": "2014년 기출의 중간 부분입니다. 냉동회로의 각 부품별 역할을 이해하며 풀이하세요.", "tips": ["냉동회로 그림 그려보기", "부품 역할 정리", "유사 문제 비교 분석"]},
        "2026-9-9": {"tasks": [{"text": "📖 냉동기계 심화 개념 학습", "done": False}], "recommendation": "압축기, 응축기, 증발기의 구조와 원리를 심화 학습합니다. 각 부품에서 냉매가 어떻게 변하는지 추적하세요.", "tips": ["P-H 선도 그리기", "냉매 상태 변화 추적", "부품별 열전달 이해"]},
        "2026-9-10": {"tasks": [{"text": "✍️ 중요 공식 정리 및 암기", "done": False}], "recommendation": "COP, 냉동능력, 성능계수 등 핵심 공식을 정리하고 계산 문제를 연습하세요.", "tips": ["공식 유도 과정 이해하기", "계산 연습문제 풀기", "공식 정리표 만들기"]},
        
        # 9월 3주
        "2026-9-15": {"tasks": [{"text": "🎯 2014년 필기 31-45번 풀이", "done": False}], "recommendation": "2014년 기출의 마지막 부분입니다. 공기조화 부분이 주로 나옵니다. 습공기선도 문제에 집중하세요.", "tips": ["습공기선도 완벽히 이해", "상대습도 계산", "공정 분석"]},
        "2026-9-16": {"tasks": [{"text": "📚 2015년 필기 1-15번 풀이", "done": False}], "recommendation": "2015년 기출의 시작입니다. 2014년과 비교하며 출제 경향을 분석하세요.", "tips": ["연도별 출제 경향 비교", "반복되는 주제 찾기", "최신 출제 동향 파악"]},
        "2026-9-17": {"tasks": [{"text": "💪 주간 복습 및 약점 정리", "done": False}], "recommendation": "지금까지 푼 문제들을 복습하고, 틀린 부분을 카테고리별로 정리하세요.", "tips": ["약점 분류하기", "같은 주제 문제 모아 풀기", "진행 상황 평가"]},
        
        # 9월 4주
        "2026-9-22": {"tasks": [{"text": "🎯 2015년 필기 16-45번 풀이", "done": False}], "recommendation": "2015년 기출을 완료합니다. 새로운 유형의 문제가 나올 수 있으니 신중하게 풀어보세요.", "tips": ["새로운 문제 유형 찾기", "변형 문제 예상하기", "전략적 풀이"]},
        "2026-9-23": {"tasks": [{"text": "🔄 2016년 필기 1-15번 풀이", "done": False}], "recommendation": "2016년 기출을 시작합니다. 최근 시험의 경향이 더 반영되기 시작합니다.", "tips": ["최근 경향 파악", "개정 내용 확인", "새로운 주제 학습"]},
        "2026-9-24": {"tasks": [{"text": "📚 월간 종합 복습", "done": False}], "recommendation": "9월 한 달간 배운 내용을 전체적으로 복습하세요. 정답률 70점 이상을 목표로 하세요.", "tips": ["한 달치 복습", "취약 영역 집중 학습", "월간 진행도 평가"]},
        
        # 10월 1주 (심화 학습)
        "2026-10-1": {"tasks": [{"text": "🎯 2016년 필기 16-45번 풀이", "done": False}], "recommendation": "2016년 기출을 완료합니다. 냉동회로의 더 복잡한 문제들을 만날 것입니다.", "tips": ["복잡한 회로도 분석", "단계별 풀이", "유사 문제 응용"]},
        "2026-10-2": {"tasks": [{"text": "📖 냉동사이클 심화 학습", "done": False}], "recommendation": "냉동사이클의 각 과정(압축, 응축, 팽창, 증발)을 자세히 학습하세요.", "tips": ["사이클별 열역학 분석", "온도-엔탈피 변화 추적", "효율 계산"]},
        "2026-10-3": {"tasks": [{"text": "✍️ 응축기, 증발기 이론 정리", "done": False}], "recommendation": "냉동장치의 핵심인 응축기와 증발기를 깊이 있게 학습하세요.", "tips": ["열전달 이론 이해", "효율 계산", "문제 유형별 풀이"]},
        
        # 10월 2주
        "2026-10-6": {"tasks": [{"text": "🎯 2017년 필기 1-30번 풀이", "done": False}], "recommendation": "2017년 기출의 전반부입니다. 지난해보다 더 심화된 문제들이 출제됩니다.", "tips": ["심화 문제 분석", "새로운 주제 식별", "고난도 문제 전략"]},
        "2026-10-7": {"tasks": [{"text": "📚 2017년 필기 31-45번 풀이", "done": False}], "recommendation": "2017년 기출의 후반부입니다. 공기조화 부분에 주목하세요.", "tips": ["공기조화 문제 집중", "종합적 사고", "실무 연결"]},
        "2026-10-8": {"tasks": [{"text": "💪 약점 부분 집중 복습", "done": False}], "recommendation": "지금까지의 시험에서 자주 틀렸던 부분을 집중적으로 복습하세요.", "tips": ["약점 분석", "반복 학습", "이해도 재평가"]},
        
        # 10월 3주
        "2026-10-13": {"tasks": [{"text": "🎯 2018년 필기 1-30번 풀이", "done": False}], "recommendation": "2018년 기출을 시작합니다. 최근 시험과 가장 유사한 난이도입니다.", "tips": ["최신 경향 반영", "현재 출제 수준 파악", "전략 조정"]},
        "2026-10-14": {"tasks": [{"text": "📚 2018년 필기 31-45번 풀이", "done": False}], "recommendation": "2018년 기출을 완료합니다. 최근 5년간의 출제 경향을 정리하세요.", "tips": ["5년 경향 분석", "반복 주제 정리", "예상 출제 주제"]},
        "2026-10-15": {"tasks": [{"text": "🔄 모의고사 풀이 (심화)", "done": False}], "recommendation": "심화된 모의고사를 풀어보세요. 75점 이상을 목표로 하세요.", "tips": ["시간 관리 연습", "고난도 문제 우선", "정확한 풀이"]},
        
        # 10월 4주
        "2026-10-20": {"tasks": [{"text": "🎯 2019년 필기 1-30번 풀이", "done": False}], "recommendation": "2019년 기출을 시작합니다. 가장 최근의 출제 경향을 반영합니다.", "tips": ["최근 경향 파악", "새로운 내용 확인", "예상 문제 추론"]},
        "2026-10-21": {"tasks": [{"text": "📚 2019년 필기 31-45번 풀이", "done": False}], "recommendation": "2019년 기출을 완료합니다. 앞으로의 시험 방향을 예측하세요.", "tips": ["최신 출제 방향 예측", "변화 추세 파악", "대비 전략 수립"]},
        "2026-10-22": {"tasks": [{"text": "💪 월간 모의고사", "done": False}], "recommendation": "10월의 마지막 모의고사입니다. 80점 이상을 목표로 하세요.", "tips": ["종합 실력 평가", "시간 관리 최적화", "약점 최종 점검"]},
        
        # 11월 1주 (실기 필답형)
        "2026-11-3": {"tasks": [{"text": "🎯 2020년 필기 1-30번 풀이", "done": False}], "recommendation": "2020년 기출을 시작합니다. 가장 최신의 문제들입니다.", "tips": ["최신 주제 파악", "변화 내용 학습", "새로운 출제 형식"]},
        "2026-11-4": {"tasks": [{"text": "📚 2020년 필기 31-45번 풀이", "done": False}], "recommendation": "2020년 기출을 완료합니다. 필기 시험 준비를 마무리하세요.", "tips": ["필기 최종 점검", "약점 보완", "자신감 확보"]},
        "2026-11-5": {"tasks": [{"text": "✍️ 필기 전 영역 총정리", "done": False}], "recommendation": "2014-2020년 7년간의 기출을 정리하세요. 출제 주제의 70%가 반복됩니다.", "tips": ["중요 주제별 정리", "출제 경향 분류", "최종 학습 계획"]},
        
        # 11월 2주
        "2026-11-10": {"tasks": [{"text": "🛠️ 실기 필답형 1번 (과열도) 연습", "done": False}], "recommendation": "과열도의 정의와 냉동사이클에서의 의미를 완벽히 이해하세요.", "tips": ["개념 정확히 이해", "계산 방법 암기", "관련 문제 풀이"]},
        "2026-11-11": {"tasks": [{"text": "🛠️ 실기 필답형 2-3번 연습", "done": False}], "recommendation": "압축비와 냉동능력 문제를 연습하세요. 계산 공식을 정확히 외워야 합니다.", "tips": ["공식 정확히 암기", "계산 연습", "단위 확인"]},
        "2026-11-12": {"tasks": [{"text": "🛠️ 실기 필답형 4-5번 연습", "done": False}], "recommendation": "동관 절단과 플레어링의 작업 과정과 주의사항을 정리하세요.", "tips": ["작업 순서 이해", "안전 주의사항 암기", "실습 복습"]},
        
        # 11월 3주
        "2026-11-17": {"tasks": [{"text": "🛠️ 실기 필답형 6-7번 연습", "done": False}], "recommendation": "밴딩과 용접 과정의 주의사항을 상세히 학습하세요.", "tips": ["작업 기술 이해", "주의사항 숙지", "오류 사례 학습"]},
        "2026-11-18": {"tasks": [{"text": "🛠️ 실기 필답형 8번 연습", "done": False}], "recommendation": "누설 검사 방법을 정확히 이해하세요. 비누액과 할로겐 검출기의 사용법을 알아야 합니다.", "tips": ["검사 방법 이해", "장비 사용법", "안전 조치"]},
        "2026-11-19": {"tasks": [{"text": "💪 주간 필답형 복습", "done": False}], "recommendation": "8개 문제를 한 번에 풀어보세요. 시간 내에 정확히 답할 수 있는지 확인하세요.", "tips": ["시간 관리", "전체 복습", "약점 보강"]},
        
        # 11월 4주
        "2026-11-24": {"tasks": [{"text": "🎯 필답형 전 영역 모의고사", "done": False}], "recommendation": "필답형 8문제를 모두 풀어보세요. 최소 6문제 이상 정답을 목표로 하세요.", "tips": ["시간 제약 연습", "정확성 확보", "진행도 평가"]},
        "2026-11-25": {"tasks": [{"text": "📚 약점 필답형 재연습", "done": False}], "recommendation": "틀렸던 문제를 다시 풀어보세요. 정확한 답변 방식을 기억하세요.", "tips": ["오답 분석", "재학습", "최종 점검"]},
        "2026-11-26": {"tasks": [{"text": "💪 월간 종합 복습", "done": False}], "recommendation": "필기와 필답형을 모두 복습하세요. 합격 수준에 도달했는지 확인하세요.", "tips": ["전체 복습", "부족 부분 보강", "자신감 확보"]},
        
        # 12월 1주 (시뮬레이션 & 종합)
        "2026-12-1": {"tasks": [{"text": "🛠️ 실기 시뮬레이션: 동관절단", "done": False}], "recommendation": "Canvas 2D 시뮬레이터에서 동관절단 작업을 반복 연습하세요. 정확한 길이 설정이 중요합니다.", "tips": ["길이 입력 연습", "클릭 정확도", "작업 흐름 숙지"]},
        "2026-12-2": {"tasks": [{"text": "🛠️ 실기 시뮬레이션: 플레어링-밴딩", "done": False}], "recommendation": "플레어링과 밴딩 작업을 연습하세요. 각도 조정을 정확히 해야 합니다.", "tips": ["각도 입력 연습", "작업 순서", "시각적 확인"]},
        "2026-12-3": {"tasks": [{"text": "🛠️ 실기 시뮬레이션: 연결-용접", "done": False}], "recommendation": "연결과 용접 작업의 타이밍을 맞추세요. 3초 이상 마우스를 누르는 연습을 하세요.", "tips": ["타이밍 연습", "손 안정성", "완료 신호 확인"]},
        
        # 12월 2주
        "2026-12-8": {"tasks": [{"text": "🛠️ 실기 시뮬레이션: 냉각-작동점검", "done": False}], "recommendation": "냉각과 작동점검을 완료하세요. 전체 작업 흐름을 한 번에 완료하는 것을 목표로 하세요.", "tips": ["전체 흐름 연습", "시간 관리", "정확성 확보"]},
        "2026-12-9": {"tasks": [{"text": "🎯 필기 전체 최종 복습 (중요도순)", "done": False}], "recommendation": "필기 시험의 중요 주제부터 역순으로 복습하세요. 자주 나오는 주제에 집중하세요.", "tips": ["중요도 기준 학습", "시간 효율", "합격선 확보"]},
        "2026-12-10": {"tasks": [{"text": "💪 필기 최종 모의고사", "done": False}], "recommendation": "최종 모의고사를 풀어보세요. 85점 이상을 목표로 하세요.", "tips": ["합격선 도달 확인", "남은 약점 보강", "자신감 재확인"]},
        
        # 12월 3주
        "2026-12-15": {"tasks": [{"text": "✍️ 필답형 최종 복습", "done": False}], "recommendation": "필답형 8문제를 한 번 더 풀어보세요. 답변 방식을 확실히 하세요.", "tips": ["답변 형식 확인", "시간 내 완료", "정확성 최우선"]},
        "2026-12-16": {"tasks": [{"text": "🛠️ 시뮬레이션 최종 점검", "done": False}], "recommendation": "전체 7가지 작업을 한 번에 완료하세요. 모든 작업이 자동으로 진행되는지 확인하세요.", "tips": ["전체 흐름 숙지", "예상 시간", "완료 신호 확인"]},
        "2026-12-17": {"tasks": [{"text": "💪 최종 종합 모의고사", "done": False}], "recommendation": "필기, 필답형, 시뮬레이션을 모두 포함한 최종 모의고사를 풀어보세요.", "tips": ["종합 실력 평가", "시간 관리", "합격 확정"]},
        
        # 12월 4주
        "2026-12-22": {"tasks": [{"text": "🎯 약점 최종 정리", "done": False}], "recommendation": "지금까지 틀렸던 모든 문제를 정리하고 한 번 더 풀어보세요.", "tips": ["오답 정리", "핵심 정리", "최종 보강"]},
        "2026-12-23": {"tasks": [{"text": "📚 시험 전 마지막 복습", "done": False}], "recommendation": "시험 전날입니다. 가볍게 중요 주제만 복습하고, 충분한 휴식을 취하세요.", "tips": ["핵심만 복습", "과도한 학습 피하기", "충분한 수면"]},
        "2026-12-24": {"tasks": [{"text": "✨ 컨디션 조절 및 휴식", "done": False}], "recommendation": "시험날입니다! 좋은 컨디션을 유지하고, 마음을 편하게 먹으세요. 지금까지의 준비가 최고입니다!", "tips": ["충분한 수면", "가벼운 음식", "자신감 유지"]},
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
