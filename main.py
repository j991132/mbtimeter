import streamlit as st

# Initialize session state
if 'question_number' not in st.session_state:
    st.session_state['question_number'] = 0
if 'answers' not in st.session_state:
    st.session_state['answers'] = []
if 'current_answer' not in st.session_state:
    st.session_state['current_answer'] = None
if 'mbti_calculated' not in st.session_state:
    st.session_state['mbti_calculated'] = False

# Questions and their MBTI mapping (question, dimension, direction: 1 or -1)
questions = [
    ("주말에 주로 혼자 시간을 보내는 편이다.", "E/I", -1),  # Favors I
    ("새로운 사람을 만나는 것에 부담을 느끼지 않는다.", "E/I", 1),  # Favors E
    ("계획을 세우고 꼼꼼하게 따르는 것을 좋아한다.", "J/P", 1),  # Favors J
    ("다른 사람의 감정에 쉽게 공감하는 편이다.", "T/F", -1),  # Favors F
    ("아이디어가 떠오르면 바로 실행에 옮기는 편이다.", "J/P", -1),  # Favors P
    ("규칙이나 틀에 얽매이는 것을 싫어한다.", "J/P", -1),  # Favors P
    ("주변 사람들에게 조용하고 신중하다는 말을 듣는 편이다.", "E/I", -1),  # Favors I
    ("여럿이 함께 하는 활동에서 에너지를 얻는 편이다.", "E/I", 1),  # Favors E
    ("미래에 대한 가능성보다 현재의 확실한 것을 중요하게 생각한다.", "S/N", 1),  # Favors S
    ("나만의 독특한 방식으로 표현하는 것을 즐긴다.", "S/N", -1),  # Favors N
]

choices = ["매우 그렇다", "그렇다", "보통이다", "그렇지 않다", "매우 그렇지 않다"]

def start_test():
    st.session_state['question_number'] = 1
    st.session_state['answers'] = []
    st.session_state['current_answer'] = None
    st.session_state['mbti_calculated'] = False

def next_question(selected_answer):
    if selected_answer is not None:
        # Append the selected answer to the answers list
        if len(st.session_state['answers']) < st.session_state['question_number']:
            st.session_state['answers'].append(selected_answer)
        else:
            # Update the answer if revisiting a question
            st.session_state['answers'][st.session_state['question_number'] - 1] = selected_answer
        st.session_state['question_number'] += 1
        st.session_state['current_answer'] = None
    else:
        st.warning("답변을 선택해주세요.")

def prev_question():
    if st.session_state['question_number'] > 1:
        st.session_state['question_number'] -= 1
        # Load the previous answer, if available
        if len(st.session_state['answers']) >= st.session_state['question_number']:
            st.session_state['current_answer'] = st.session_state['answers'][st.session_state['question_number'] - 1]
        else:
            st.session_state['current_answer'] = None

def calculate_mbti():
    scores = {"E/I": 0, "S/N": 0, "T/F": 0, "J/P": 0}
    for i, answer in enumerate(st.session_state['answers']):
        score = {"매우 그렇다": 2, "그렇다": 1, "보통이다": 0, "그렇지 않다": -1, "매우 그렇지 않다": -2}[answer]
        dimension = questions[i][1]
        direction = questions[i][2]
        scores[dimension] += score * direction

    mbti_result = (
        "E" if scores["E/I"] > 0 else "I",
        "S" if scores["S/N"] > 0 else "N",
        "T" if scores["T/F"] > 0 else "F",
        "J" if scores["J/P"] > 0 else "P",
    )
    mbti_type = "".join(mbti_result)
    st.subheader("당신의 MBTI 성향은...")
    st.write(f"**{mbti_type}** 입니다!")
    # Example MBTI description
    st.write("예: INTJ는 전략적 사고와 독립적인 성향으로 알려진 '건축가'입니다.")

st.title("나의 MBTI 성향 알아보기")
st.write("일상생활과 관련된 10가지 질문에 답하고 당신의 MBTI 성향을 알아보세요!")

if st.button("MBTI 테스트 시작"):
    start_test()

if 1 <= st.session_state['question_number'] <= len(questions):
    current_question = questions[st.session_state['question_number'] - 1][0]
    st.progress(st.session_state['question_number'] / len(questions))
    st.write(f"질문 {st.session_state['question_number']} / {len(questions)}")
    st.subheader(f"질문 {st.session_state['question_number']}")
    st.write(current_question)

    # Get the current answer from the radio button
    selected_answer = st.radio(
        "선택하세요",
        choices,
        index=choices.index(st.session_state['current_answer']) if st.session_state['current_answer'] in choices else None,
        key=f"radio_{st.session_state['question_number']}",
    )
    st.session_state['current_answer'] = selected_answer

    cols = st.columns([1, 1])
    if st.session_state['question_number'] > 1:
        if cols[0].button("이전 질문"):
            prev_question()
    if cols[1].button("다음 질문"):
        next_question(selected_answer)

elif st.session_state['question_number'] > len(questions) and not st.session_state['mbti_calculated']:
    if len(st.session_state['answers']) == len(questions):
        calculate_mbti()
        st.session_state['mbti_calculated'] = True
    else:
        st.warning("모든 질문에 답변해주세요!")
    if st.button("테스트 다시 시작"):
        start_test()
elif st.session_state['mbti_calculated']:
    if st.button("테스트 다시 시작"):
        start_test()
