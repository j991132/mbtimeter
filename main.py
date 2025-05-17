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

    # 글자 크기 계산
    font_sizes = {}
    for dim, letter in zip(["E/I", "S/N", "T/F", "J/P"], [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]):
        positive_letter, negative_letter = letter
        positive_percentage = percentages[dim]
        negative_percentage = 100 - positive_percentage
        # 글자 크기: 16px (0%) ~ 48px (100%)
        font_sizes[positive_letter] = 16 + (positive_percentage / 100) * (48 - 16)
        font_sizes[negative_letter] = 16 + (negative_percentage / 100) * (48 - 16)

    st.subheader("당신의 MBTI 성향은...")
    # MBTI 유형 표시 (글자 크기 적용)
    mbti_display = "".join(
        f'<span style="font-size:{font_sizes[letter]:.2f}px">{letter}</span>'
        for letter in mbti_type
    )
    st.markdown(f"**{mbti_display}** 입니다!", unsafe_allow_html=True)
    st.write("예: INTJ는 전략적 사고와 독립적인 성향으로 알려진 '건축가'입니다.")

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
