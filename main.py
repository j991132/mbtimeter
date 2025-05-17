import streamlit as st
import os

# 세션 상태 초기화
if 'question_number' not in st.session_state:
    st.session_state['question_number'] = 0
if 'answers' not in st.session_state:
    st.session_state['answers'] = []
if 'mbti_calculated' not in st.session_state:
    st.session_state['mbti_calculated'] = False
if 'current_selection' not in st.session_state:
    st.session_state['current_selection'] = None

# 질문과 MBTI 매핑 (질문, 차원, 방향: 1 또는 -1)
questions = [
    ("주말에 주로 혼자 시간을 보내는 편이다.", "E/I", -1),  # I 선호
    ("새로운 사람을 만나는 것에 부담을 느끼지 않는다.", "E/I", 1),  # E 선호
    ("계획을 세우고 꼼꼼하게 따르는 것을 좋아한다.", "J/P", 1),  # J 선호
    ("다른 사람의 감정에 쉽게 공감하는 편이다.", "T/F", -1),  # F 선호
    ("아이디어가 떠오르면 바로 실행에 옮기는 편이다.", "J/P", -1),  # P 선호
    ("규칙이나 틀에 얽매이는 것을 싫어한다.", "J/P", -1),  # P 선호
    ("주변 사람들에게 조용하고 신중하다는 말을 듣는 편이다.", "E/I", -1),  # I 선호
    ("여럿이 함께 하는 활동에서 에너지를 얻는 편이다.", "E/I", 1),  # E 선호
    ("미래에 대한 가능성보다 현재의 확실한 것을 중요하게 생각한다.", "S/N", 1),  # S 선호
    ("나만의 독특한 방식으로 표현하는 것을 즐긴다.", "S/N", -1),  # N 선호
]

choices = ["매우 그렇다", "그렇다", "보통이다", "그렇지 않다", "매우 그렇지 않다"]

# MBTI 유형별 직업 추천
career_recommendations = {
    "INTJ": [
        ("소프트웨어 개발자", "복잡한 시스템을 설계하고 코드를 작성하여 소프트웨어 솔루션을 개발한다."),
        ("프로젝트 매니저", "프로젝트 계획을 수립하고 팀을 관리하여 목표를 성공적으로 달성한다."),
        ("데이터 분석가", "데이터를 분석하여 비즈니스 의사결정을 지원하는 통찰을 제공한다."),
        ("변호사", "법률 자문을 제공하고 소송을 관리하여 고객의 권익을 보호한다."),
        ("경영 컨설턴트", "기업의 전략을 수립하고 운영 효율성을 높이는 솔루션을 제안한다.")
    ],
    "INTP": [
        ("소프트웨어 개발자", "혁신적인 코드를 작성하여 기술 문제를 해결한다."),
        ("교수", "학문적 지식을 연구하고 학생들에게 가르친다."),
        ("작가", "창의적인 아이디어를 글로 표현하여 독자를 사로잡는다."),
        ("회계사", "재무 데이터를 분석하고 정확한 보고서를 작성한다."),
        ("과학자", "실험과 연구를 통해 새로운 지식을 발견한다.")
    ],
    "ENTJ": [
        ("CEO", "조직의 비전을 설정하고 전략적 결정을 내려 성과를 극대화한다."),
        ("판매 관리자", "판매 팀을 이끌고 매출 목표를 달성한다."),
        ("심리학자", "인간 행동을 연구하고 치료 계획을 수립한다."),
        ("홍보 관리자", "브랜드 이미지를 관리하고 대중과의 소통을 조율한다."),
        ("정치 컨설턴트", "정치 캠페인을 계획하고 전략을 수립한다.")
    ],
    "ENTP": [
        ("변호사", "법적 논쟁을 통해 고객을 대변하고 문제를 해결한다."),
        ("아트 디렉터", "창의적인 비전을 구체화하여 시각적 콘텐츠를 제작한다."),
        ("판매 관리자", "판매 전략을 개발하고 팀을 동기부여한다."),
        ("엔지니어", "기술적 문제를 해결하기 위해 혁신적인 설계를 한다."),
        ("분석가", "데이터를 해석하여 비즈니스 전략을 지원한다.")
    ],
    "INFJ": [
        ("상담사", "개인의 정서적 문제를 지원하고 해결 방안을 제시한다."),
        ("작가", "깊이 있는 이야기를 통해 사람들에게 영감을 준다."),
        ("사회복지사", "취약 계층을 지원하고 사회적 문제를 해결한다."),
        ("교육자", "학생들의 학습과 성장을 돕는 교육 프로그램을 운영한다."),
        ("디자이너", "창의적인 시각으로 사용자 경험을 개선한다.")
    ],
    "INFP": [
        ("UX 디자이너", "사용자 친화적인 인터페이스를 설계하여 경험을 향상시킨다."),
        ("심리학자", "개인의 정신 건강을 지원하고 치료를 제공한다."),
        ("작가", "감성적인 이야기를 통해 독자와 연결된다."),
        ("물리치료사", "환자의 신체적 회복을 돕는 치료 계획을 실행한다."),
        ("중재자", "갈등을 해결하고 당사자 간 합의를 도출한다.")
    ],
    "ENFJ": [
        ("인사 전문가", "직원 채용과 조직 문화를 관리하여 팀을 강화한다."),
        ("홍보 코디네이터", "브랜드 메시지를 전달하고 대중 관계를 구축한다."),
        ("비영리 단체 관리자", "사회적 사명을 추구하며 조직을 운영한다."),
        ("고객 서비스 대표", "고객의 문제를 해결하고 만족도를 높인다."),
        ("지도 상담사", "학생들의 진로를 안내하고 목표 설정을 돕는다.")
    ],
    "ENFP": [
        ("마케터", "창의적인 캠페인을 통해 브랜드를 홍보한다."),
        ("기자", "흥미로운 이야기를 취재하고 대중에게 전달한다."),
        ("배우", "감정을 표현하며 관객을 사로잡는다."),
        ("이벤트 플래너", "행사를 기획하고 실행하여 참가자 경험을 극대화한다."),
        ("여행 가이드", "여행자들에게 지역의 매력을 소개하고 안내한다.")
    ],
    "ISTJ": [
        ("회계사", "재무 기록을 관리하고 정확한 보고서를 작성한다."),
        ("프로젝트 매니저", "프로젝트를 체계적으로 관리하여 목표를 달성한다."),
        ("물류 관리자", "공급망을 최적화하여 물류 흐름을 관리한다."),
        ("감사원", "조직의 재무 및 운영 절차를 검토하여 규정을 준수한다."),
        ("은행원", "고객의 금융 거래를 처리하고 자산을 관리한다.")
    ],
    "ISFJ": [
        ("간호사", "환자를 돌보며 건강 상태를 관리하고 치료를 지원한다."),
        ("유치원 교사", "어린이들의 학습과 정서적 발달을 돕는다."),
        ("행정 보조", "사무 업무를 지원하여 조직의 효율성을 높인다."),
        ("약사", "약을 조제하고 환자에게 복약 지도를 제공한다."),
        ("사회복지사", "취약 계층의 삶의 질을 향상시키는 지원을 제공한다.")
    ],
    "ESTJ": [
        ("경영자", "조직을 이끌고 전략적 결정을 내려 목표를 달성한다."),
        ("회계사", "재무 기록을 관리하고 세무 신고를 준비한다."),
        ("변호사", "법률 자문을 제공하고 소송을 진행한다."),
        ("프로젝트 매니저", "팀과 자원을 조율하여 프로젝트를 성공적으로 실행한다."),
        ("보험 대리인", "고객에게 보험 상품을 판매하고 청구를 처리한다.")
    ],
    "ESFJ": [
        ("특수 교육 교사", "특별한 요구가 있는 학생들의 학습을 지원한다."),
        ("아동 보육 제공자", "어린이들을 돌보며 안전하고 건강한 환경을 제공한다."),
        ("의사", "환자를 진찰하고 치료 계획을 수립하여 건강을 관리한다."),
        ("간호사", "환자의 건강을 모니터링하고 의료 지원을 제공한다."),
        ("인사 관리자", "직원 채용과 복지를 관리하여 조직 문화를 강화한다.")
    ],
    "ISTP": [
        ("기계공", "기계 장비를 수리하고 유지보수하여 작동 상태를 유지한다."),
        ("소방관", "화재를 진압하고 긴급 상황에서 생명을 구한다."),
        ("건축가", "건물 설계를 통해 기능적이고 미적인 공간을 창조한다."),
        ("전기기사", "전기 시스템을 설치하고 유지보수한다."),
        ("컴퓨터 프로그래머", "소프트웨어를 개발하여 기술 솔루션을 제공한다.")
    ],
    "ISFP": [
        ("수의사", "동물의 건강을 관리하고 질병을 치료한다."),
        ("패션 디자이너", "창의적인 의상을 설계하여 트렌드를 선도한다."),
        ("조경사", "야외 공간을 설계하고 관리하여 환경을美化한다."),
        ("음악가", "음악을 연주하거나 작곡하여 예술적 표현을 한다."),
        ("요리사", "음식을 준비하여 고객에게 맛과 만족을 제공한다.")
    ],
    "ESTP": [
        ("프로젝트 코디네이터", "프로젝트를 계획하고 실행하여 목표를 달성한다."),
        ("투자자", "금융 시장을 분석하고 투자 기회를 포착한다."),
        ("형사", "범죄를 조사하고 용의자를 추적한다."),
        ("스포츠 코치", "선수들을 훈련시키고 경기 전략을 수립한다."),
        ("마케터", "제품이나 서비스를 홍보하여 판매를 촉진한다.")
    ],
    "ESFP": [
        ("배우", "연기를 통해 캐릭터를 구현하고 관객을 즐겁게 한다."),
        ("웨이터", "고객에게 음식을 서빙하고 친절한 서비스를 제공한다."),
        ("여행 가이드", "관광객에게 지역의 매력을 소개하고 안내한다."),
        ("이벤트 플래너", "행사를 기획하여 참가자들에게 즐거움을 선사한다."),
        ("소매 판매원", "고객에게 제품을 판매하고 쇼핑 경험을 개선한다.")
    ]
}

def start_test():
    st.session_state['question_number'] = 1
    st.session_state['answers'] = []
    st.session_state['mbti_calculated'] = False
    st.session_state['current_selection'] = None

def prev_question():
    if st.session_state['question_number'] > 1:
        st.session_state['question_number'] -= 1
        # 이전 답변 로드
        if len(st.session_state['answers']) >= st.session_state['question_number']:
            st.session_state['current_selection'] = st.session_state['answers'][st.session_state['question_number'] - 1]
        else:
            st.session_state['current_selection'] = None
        # 디버깅: 상태 업데이트 후 로그
        st.write(f"이전 질문 클릭 - 질문 번호: {st.session_state['question_number']}, 선택: {st.session_state['current_selection']}, 답변 리스트: {st.session_state['answers']}")
        # 즉시 재실행
        st.rerun()

def calculate_mbti():
    scores = {"E/I": 0, "S/N": 0, "T/F": 0, "J/P": 0}
    for i, answer in enumerate(st.session_state['answers']):
        score = {"매우 그렇다": 2, "그렇다": 1, "보통이다": 0, "그렇지 않다": -1, "매우 그렇지 않다": -2}[answer]
        dimension = questions[i][1]
        direction = questions[i][2]
        scores[dimension] += score * direction

    # 최대 점수
    max_scores = {"E/I": 8, "S/N": 4, "T/F": 2, "J/P": 6}  # 질문 수 * 2
    percentages = {}
    for dim in scores:
        # 비율 계산: ((점수 + 최대 점수) / (2 * 최대 점수)) * 100
        positive_percentage = ((scores[dim] + max_scores[dim]) / (2 * max_scores[dim])) * 100
        percentages[dim] = positive_percentage

    mbti_result = (
        "E" if scores["E/I"] > 0 else "I",
        "S" if scores["S/N"] > 0 else "N",
        "T" if scores["T/F"] > 0 else "F",
        "J" if scores["J/P"] > 0 else "P",
    )
    mbti_type = "".join(mbti_result)

    # 글자 크기 및 색상
    font_sizes = {}
    font_colors = {
        "E": "#6366F1", "I": "#F472B6", "S": "#10B981", "N": "#F59E0B",
        "T": "#06B6D4", "F": "#A855F7", "J": "#EF4444", "P": "#6B7280"
    }
    percentage_values = {}
    for dim, letter in zip(["E/I", "S/N", "T/F", "J/P"], [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]):
        positive_letter, negative_letter = letter
        positive_percentage = percentages[dim]
        negative_percentage = 100 - positive_percentage
        # 글자 크기: 19px (0%) ~ 51px (100%)
        font_sizes[positive_letter] = 19 + (positive_percentage / 100) * (51 - 19)
        font_sizes[negative_letter] = 19 + (negative_percentage / 100) * (51 - 19)
        percentage_values[positive_letter] = positive_percentage
        percentage_values[negative_letter] = negative_percentage

    st.subheader("당신의 MBTI 성향은...")
    # MBTI 유형 표시 (글자 크기, 색상, 비율, 중앙 정렬)
    mbti_display = "".join(
        f'<div class="mbti-letter" style="display: inline-block; text-align: center; margin: 0 10px;">'
        f'<span style="font-size:{font_sizes[letter]:.2f}px; color:{font_colors[letter]}">{letter}</span>'
        f'<div style="font-size:16px; color:{font_colors[letter]}">{percentage_values[letter]:.1f}%</div>'
        f'</div>'
        for letter in mbti_type
    )
    st.markdown(
        f"""
        <style>
        .mbti-result {{ text-align: center; margin: 20px auto; }}
        .mbti-letter {{ margin: 0 10px; }}
        .career-table {{ width: 80%; margin: 20px auto; border-collapse: collapse; }}
        .career-table th, .career-table td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
        .career-table th {{ background-color: #f4f4f4; }}
        </style>
        <div class="mbti-result">**{mbti_display}** 입니다!</div>
        """,
        unsafe_allow_html=True
    )

    # 직업 추천 표시
    st.subheader(f"{mbti_type}에 어울리는 직업")
    careers = career_recommendations[mbti_type]
    career_table = "<table class='career-table'><tr><th>직업</th><th>설명</th></tr>"
    for job, description in careers:
        career_table += f"<tr><td>{job}</td><td>{description}</td></tr>"
    career_table += "</table>"
    st.markdown(career_table, unsafe_allow_html=True)

st.title("나의 MBTI 성향 알아보기")
st.write("일상생활과 관련된 10가지 질문에 답하고 당신의 MBTI 성향을 알아보세요!")

if st.button("MBTI 테스트 시작", key="start_test"):
    start_test()

if 1 <= st.session_state['question_number'] <= len(questions):
    current_question = questions[st.session_state['question_number'] - 1][0]
    st.progress(st.session_state['question_number'] / len(questions))
    st.write(f"질문 {st.session_state['question_number']} / {len(questions)}")
    st.subheader(f"질문 {st.session_state['question_number']}")

    # 질문과 이미지를 좌우로 배치
    cols = st.columns([2, 1])  # 왼쪽(질문): 2, 오른쪽(이미지): 1 비율
    with cols[0]:
        st.write(current_question)
        # 이전 답변을 기본값으로 설정
        default_answer = None
        if len(st.session_state['answers']) >= st.session_state['question_number']:
            default_answer = st.session_state['answers'][st.session_state['question_number'] - 1]
        else:
            default_answer = st.session_state['current_selection']

        # 라디오 버튼
        st.session_state['current_selection'] = st.radio(
            "선택하세요",
            choices,
            index=choices.index(default_answer) if default_answer in choices else None,
            key=f"radio_{st.session_state['question_number']}",
        )

    with cols[1]:
        image_path = f"images/{st.session_state['question_number']}.png"
        if os.path.exists(image_path):
            st.image(image_path, caption=f"질문 {st.session_state['question_number']} 이미지", use_container_width=True, width=300)
        else:
            st.warning(f"이미지 {image_path}를 찾을 수 없습니다. 파일 경로를 확인해주세요.")

    cols = st.columns([1, 1])
    if st.session_state['question_number'] > 1:
        if cols[0].button("이전 질문", key=f"prev_{st.session_state['question_number']}"):
            prev_question()
    if cols[1].button("다음 질문", key=f"next_{st.session_state['question_number']}", disabled=not st.session_state['current_selection']):
        if st.session_state['current_selection']:
            # 답변 저장
            if len(st.session_state['answers']) < st.session_state['question_number']:
                st.session_state['answers'].append(st.session_state['current_selection'])
            else:
                st.session_state['answers'][st.session_state['question_number'] - 1] = st.session_state['current_selection']
            st.session_state['question_number'] += 1
            st.session_state['current_selection'] = None
            # 디버깅: 상태 업데이트 후 로그
            st.write(f"다음 질문 클릭 - 선택: {st.session_state['current_selection']}, 질문 번호: {st.session_state['question_number']}, 답변 리스트: {st.session_state['answers']}")
            # 즉시 재실행
            st.rerun()
        else:
            st.warning("답변을 선택해주세요.")

elif st.session_state['question_number'] > len(questions) and not st.session_state['mbti_calculated']:
    if len(st.session_state['answers']) == len(questions):
        calculate_mbti()
        st.session_state['mbti_calculated'] = True
    else:
        st.warning("모든 질문에 답변해주세요!")
    if st.button("테스트 다시 시작", key="restart_test"):
        start_test()
elif st.session_state['mbti_calculated']:
    if st.button("테스트 다시 시작", key="restart_test_final"):
        start_test()
