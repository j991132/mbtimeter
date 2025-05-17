import streamlit as st

if 'question_number' not in st.session_state:
    st.session_state['question_number'] = 0
if 'answers' not in st.session_state:
    st.session_state['answers'] = []
if 'current_answer' not in st.session_state:
    st.session_state['current_answer'] = None
if 'mbti_calculated' not in st.session_state:
    st.session_state['mbti_calculated'] = False

questions = [
    "주말에 주로 혼자 시간을 보내는 편이다.",
    "새로운 사람을 만나는 것에 부담을 느끼지 않는다.",
    "계획을 세우고 꼼꼼하게 따르는 것을 좋아한다.",
    "다른 사람의 감정에 쉽게 공감하는 편이다.",
    "아이디어가 떠오르면 바로 실행에 옮기는 편이다.",
    "규칙이나 틀에 얽매이는 것을 싫어한다.",
    "주변 사람들에게 조용하고 신중하다는 말을 듣는 편이다.",
    "여럿이 함께 하는 활동에서 에너지를 얻는 편이다.",
    "미래에 대한 가능성보다 현재의 확실한 것을 중요하게 생각한다.",
    "나만의 독특한 방식으로 표현하는 것을 즐긴다.",
]

choices = ["매우 그렇다", "그렇다", "보통이다", "그렇지 않다", "매우 그렇지 않다"]

def start_test():
    st.session_state['question_number'] = 1
    st.session_state['answers'] = []
    st.session_state['current_answer'] = None
    st.session_state['mbti_calculated'] = False

def next_question():
    if st.session_state['current_answer'] is not None:
        st.session_state['answers'].append(st.session_state['current_answer'])
        st.session_state['question_number'] += 1
        st.session_state['current_answer'] = None  # 다음 질문 시 현재 답변 초기화

def prev_question():
    if st.session_state['question_number'] > 1:
        st.session_state['question_number'] -= 1
        if st.session_state['answers']:
            st.session_state['current_answer'] = st.session_state['answers'].pop()
        else:
            st.session_state['current_answer'] = None

def calculate_mbti():
    e_i_score = 0
    s_n_score = 0
    t_f_score = 0
    j_p_score = 0

    for i, answer in enumerate(st.session_state['answers']):
        score = 0
        if answer == "매우 그렇다":
            score = 2
        elif answer == "그렇다":
            score = 1
        elif answer == "보통이다":
            score = 0
        elif answer == "그렇지 않다":
            score = -1
        elif answer == "매우 그렇지 않다":
            score = -2

        if (i + 1) % 4 == 1:
            e_i_score += score
        elif (i + 1) % 4 == 2:
            s_n_score += score
        elif (i + 1) % 4 == 3:
            t_f_score += score
        elif (i + 1) % 4 == 0:
            j_p_score += score

    mbti_result = ""
    if e_i_score > 0:
        mbti_result += "E"
    else:
        mbti_result += "I"

    if s_n_score > 0:
        mbti_result += "S"
    else:
        mbti_result += "N"

    if t_f_score > 0:
        mbti_result += "T"
    else:
        mbti_result += "F"

    if j_p_score > 0:
        mbti_result += "J"
    else:
        mbti_result += "P"

    st.subheader("당신의 MBTI 성향은...")
    st.write(f"**{mbti_result}** 입니다!")

st.title("나의 MBTI 성향 알아보기")
st.write("일상생활과 관련된 10가지 질문에 답하고 당신의 MBTI 성향을 알아보세요!")

if st.button("MBTI 테스트 시작"):
    start_test()

if st.session_state['question_number'] > 0 and st.session_state['question_number'] <= len(questions):
    current_question = questions[st.session_state['question_number'] - 1]
    st.subheader(f"질문 {st.session_state['question_number']}")
    st.write(current_question)

    st.session_state['current_answer'] = st.radio("선택하세요", choices, index=choices.index(st.session_state['current_answer']) if st.session_state['current_answer'] in choices else 2) # 이전 선택 유지 또는 초기값 설정

    cols = st.columns([1, 1])
    if st.session_state['question_number'] > 1:
        if cols[0].button("이전 질문"):
            prev_question()
    if cols[1].button("다음 질문"):
        next_question()

elif st.session_state['question_number'] > len(questions) and not st.session_state['mbti_calculated']:
    calculate_mbti()
    st.session_state['mbti_calculated'] = True
elif st.session_state['mbti_calculated']:
    pass
