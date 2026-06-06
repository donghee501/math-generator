import streamlit as st
import sympy as sp
import random
from data_pool import STORY_THEMES

st.set_page_config(page_title="AI 수학 문제 생성기", page_icon="🎨")
x = sp.Symbol('x')

# -----------------------------------------------------------
# HTML 문서 생성 함수 (PDF 변환 과정 제거, 더 가볍고 빠름!)
# -----------------------------------------------------------
def create_html_document(math_type, items, is_solution=False):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script type="text/javascript" async
          src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
        </script>
        <style>
            @media print {{
                body {{ padding: 0; margin: 20px; }}
                .content-box, .solution-box {{ page-break-inside: avoid; }}
                @page {{ margin: 15mm; }}
            }}
            body {{ font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; padding: 40px; max-width: 800px; margin: auto; }}
            h1 {{ text-align: center; border-bottom: 2px solid black; padding-bottom: 15px; }}
            .header-info {{ text-align: right; margin-bottom: 30px; font-size: 18px; }}
            .content-box {{ margin-bottom: 40px; font-size: 20px; line-height: 1.8; }}
            .solution-box {{ color: #0033cc; font-size: 20px; margin-top: 15px; line-height: 1.8; }}
            .MathJax_CHTML {{ font-size: 130% !important; }}
        </style>
    </head>
    <body>
    """
    
    if not is_solution:
        html_content += f"""
        <h1>수학 시험지: {math_type}</h1>
        <div class="header-info">학년: &nbsp;&nbsp;&nbsp;&nbsp; 반: &nbsp;&nbsp;&nbsp;&nbsp; 이름: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
        <h2>📝 문제</h2>
        """
        for i, prob in enumerate(items):
            if "OX 퀴즈" in math_type:
                html_content += f'<div class="content-box"><b>{i+1}번.</b> 다음 설명이 맞으면 O, 틀리면 X를 선택하시오.<br><br>{prob}<br><br>( &nbsp;&nbsp;&nbsp;O&nbsp;&nbsp;&nbsp; / &nbsp;&nbsp;&nbsp;X&nbsp;&nbsp;&nbsp; )</div>'
            elif "스토리텔링" in math_type:
                html_content += f'<div class="content-box"><b>{i+1}번.</b> 다음 이야기를 읽고 식을 세워 정답을 구하시오.<br><br>{prob}</div>'
            else:
                html_content += f'<div class="content-box"><b>{i+1}번.</b> 다음 방정식을 푸시오.<br><br>$$ {prob} = 0 $$</div>'
    else:
        html_content += f"""
        <h1>정답 및 해설: {math_type}</h1>
        <h2>💡 상세 풀이</h2>
        """
        for i, sol in enumerate(items):
            sol_html = sol.replace('\n', '<br>')
            html_content += f'<div class="content-box"><b>[{i+1}번 해설]</b><div class="solution-box">{sol_html}</div></div>'
            
    html_content += "</body></html>"
    return html_content

# -----------------------------------------------------------
# 메인 UI
# -----------------------------------------------------------
if 'run_id' not in st.session_state:
    st.session_state.run_id = 0
    st.session_state.saved_math_type = ""
    st.session_state.saved_num_prob = 0
    st.session_state.show_problems = False

st.title("🌟 수학 무한 문제 자동 생성기")
st.sidebar.header("⚙️ 출제 설정")
st.sidebar.markdown("### 📖 단원 및 유형 선택")

main_category = st.sidebar.selectbox("단원을 선택하세요", ["일차방정식", "이차방정식", "삼차방정식"])

if main_category == "일차방정식":
    sub_type = st.sidebar.radio("📌 문제 유형", ["하 - 기본형", "중 - 계수 확장형", "스토리텔링 융합 🌟", "개념 확인 OX 퀴즈"])
elif main_category == "이차방정식":
    sub_type = st.sidebar.radio("📌 문제 유형", ["하 - 정수 근", "중 - 분수 근", "상 - 근의 공식", "스토리텔링 융합 🌟", "개념 확인 OX 퀴즈"])
elif main_category == "삼차방정식":
    sub_type = st.sidebar.radio("📌 문제 유형", ["기본형", "스토리텔링 융합 🌟", "개념 확인 OX 퀴즈"])

if "스토리텔링" in sub_type:
    math_type = f"{main_category} (스토리텔링 융합) 🌟"
elif "OX 퀴즈" in sub_type:
    math_type = f"{main_category} (개념 확인 OX 퀴즈)"
else:
    math_type = "삼차방정식" if main_category == "삼차방정식" and sub_type == "기본형" else f"{main_category} ({sub_type})"

num_prob = st.sidebar.number_input("출제할 문제 개수", min_value=1, max_value=20, value=5, step=1)

if st.sidebar.button("🚀 문제지 생성하기"):
    st.session_state.run_id += 1 
    st.session_state.saved_math_type = math_type
    st.session_state.saved_num_prob = num_prob
    st.session_state.show_problems = True

# -----------------------------------------------------------
# 문제 생성 로직
# -----------------------------------------------------------
if st.session_state.show_problems:
    random.seed(st.session_state.run_id)
    st.markdown("---")
    st.subheader(f"📝 {st.session_state.saved_math_type} 문제지")
    
    problems_for_pdf = []
    solutions_for_pdf = []
    used_problems = set()

    if "스토리텔링" in st.session_state.saved_math_type:
        if "일차" in st.session_state.saved_math_type:
            current_pool = STORY_THEMES["일차방정식"].copy()
        elif "이차" in st.session_state.saved_math_type:
            current_pool = STORY_THEMES["이차방정식"].copy()
        else:
            current_pool = STORY_THEMES["삼차방정식"].copy()
        random.shuffle(current_pool)

    for i in range(1, st.session_state.saved_num_prob + 1):
        curr_type = st.session_state.saved_math_type
        
        if curr_type == "일차방정식 (하 - 기본형)":
            while True:
                root = random.randint(-15, 15)
                if root not in used_problems:
                    used_problems.add(root)
                    break
            expr = x - root
            eq_expanded = sp.expand(expr)
            problems_for_pdf.append(sp.latex(eq_expanded))
            solutions_for_pdf.append(f"이항하여 정리하면 \\( x = {root} \\) 입니다.")
            st.latex(f"{sp.latex(eq_expanded)} = 0")
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"): 
                st.success(f"**최종 정답:** $x = {root}$")

        elif curr_type == "일차방정식 (중 - 계수 확장형)":
            while True:
                a = random.choice([2, 3, 4, 5, -2, -3, -4])
                b = random.randint(-20, 20)
                if (a, b) not in used_problems:
                    used_problems.add((a, b))
                    break
            expr = a*x + b
            problems_for_pdf.append(sp.latex(expr))
            ans = sp.Rational(-b, a) 
            solutions_for_pdf.append(f"이항하면 \\( {a}x = {-b} \\)\n양변을 \\( {a} \\)(으)로 나누면 정답: \\( x = {sp.latex(ans)} \\)")
            st.latex(f"{sp.latex(expr)} = 0")
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"): 
                st.success(f"**최종 정답:** $x = {sp.latex(ans)}$")

        elif curr_type == "일차방정식 (스토리텔링 융합) 🌟":
            if not current_pool: 
                current_pool = STORY_THEMES["일차방정식"].copy()
                random.shuffle(current_pool)
            
            theme = current_pool.pop() 
            x_val = random.randint(2, 12)
            a_val = random.randint(1, 10)
            b_val = x_val + a_val
            
            prob_text = theme["context"].format(a_val=a_val, b_val=b_val)
            problems_for_pdf.append(prob_text)
            solutions_for_pdf.append(f"식으로 세우면: \\( x + {a_val} = {b_val} \\)<br>정답: \\( x = {x_val} \\)")
            st.markdown(f"**Q.** {prob_text}", unsafe_allow_html=True)
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"):
                st.success(f"**최종 정답:** $x = {x_val}$")

        elif curr_type == "이차방정식 (하 - 정수 근)":
            while True:
                r1, r2 = random.randint(-9, 9), random.randint(-9, 9)
                r_tuple = tuple(sorted([r1, r2]))
                if r_tuple not in used_problems:
                    used_problems.add(r_tuple)
                    break
            expr = (x - r1) * (x - r2)
            eq_expanded = sp.expand(expr)
            problems_for_pdf.append(sp.latex(eq_expanded))
            sign1, sign2 = ("+" if -r1 > 0 else "-"), ("+" if -r2 > 0 else "-")
            if r1 == r2:
                solutions_for_pdf.append(f"인수분해: \\( (x {sign1} {abs(r1)})(x {sign2} {abs(r2)}) = 0 \\)\n정답: \\( x = {r1} \\) (중근)")
            else:
                solutions_for_pdf.append(f"인수분해: \\( (x {sign1} {abs(r1)})(x {sign2} {abs(r2)}) = 0 \\)\n정답: \\( x = {r1} \\) 또는 \\( x = {r2} \\)")
            st.latex(f"{sp.latex(eq_expanded)} = 0")
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"): 
                st.success(f"**최종 정답:** $x = {r1}$ 또는 $x = {r2}$" if r1 != r2 else f"**최종 정답:** $x = {r1}$ (중근)")

        elif curr_type == "이차방정식 (중 - 분수 근)":
            while True:
                a, c = random.randint(2, 5), random.randint(2, 5)
                b, d = random.randint(-7, 7), random.randint(-7, 7)
                t_check = tuple(sorted([(a, b), (c, d)]))
                if t_check not in used_problems:
                    used_problems.add(t_check)
                    break
            expr = (a*x - b) * (c*x - d)
            eq_expanded = sp.expand(expr)
            problems_for_pdf.append(sp.latex(eq_expanded))
            ans1, ans2 = sp.Rational(b, a), sp.Rational(d, c)
            sign1, sign2 = ("+" if -b > 0 else "-"), ("+" if -d > 0 else "-")
            if ans1 == ans2:
                solutions_for_pdf.append(f"인수분해: \\( ({a}x {sign1} {abs(b)})({c}x {sign2} {abs(d)}) = 0 \\)\n정답: \\( x = {sp.latex(ans1)} \\) (중근)")
            else:
                solutions_for_pdf.append(f"인수분해: \\( ({a}x {sign1} {abs(b)})({c}x {sign2} {abs(d)}) = 0 \\)\n정답: \\( x = {sp.latex(ans1)} \\) 또는 \\( x = {sp.latex(ans2)} \\)")
            st.latex(f"{sp.latex(eq_expanded)} = 0")
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"): 
                st.success(f"**최종 정답:** $x = {sp.latex(ans1)}$ 또는 $x = {sp.latex(ans2)}$" if ans1 != ans2 else f"**최종 정답:** $x = {sp.latex(ans1)}$ (중근)")

        elif curr_type == "이차방정식 (상 - 근의 공식)":
            while True:
                a_val = random.choice([1, 2])
                b_val, c_val = random.randint(-5, 5), random.randint(-5, 5)
                D = b_val**2 - 4*a_val*c_val
                if D > 0 and int(D**0.5)**2 != D and a_val != 0:
                    if (a_val, b_val, c_val) not in used_problems:
                        used_problems.add((a_val, b_val, c_val))
                        break
            expr = a_val*x**2 + b_val*x + c_val
            problems_for_pdf.append(sp.latex(expr))
            roots = sp.solve(expr, x)
            solutions_for_pdf.append(f"근의 공식 대입: \\( a={a_val}, b={b_val}, c={c_val} \\)\n정답: \\( x = {sp.latex(roots[0])} \\) 또는 \\( x = {sp.latex(roots[1])} \\)")
            st.latex(f"{sp.latex(expr)} = 0")
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"): 
                st.success(f"**최종 정답:** $x = {sp.latex(roots[0])}$ 또는 $x = {sp.latex(roots[1])}$")

        elif curr_type == "이차방정식 (스토리텔링 융합) 🌟":
            if not current_pool:
                current_pool = STORY_THEMES["이차방정식"].copy()
                random.shuffle(current_pool)
            
            theme = current_pool.pop()
            
            if theme["type"] == "도형":
                x_val = random.randint(3, 8) 
                w_diff = random.randint(1, 5) 
                area = x_val * (x_val + w_diff)
                prob_text = theme["context"].format(w_diff=w_diff, area=area)
                solutions_for_pdf.append(f"식: \\( x(x + {w_diff}) = {area} \\)<br>정답: \\( x = {x_val} \\)")
            else:
                t_val = random.randint(3, 8) 
                v0 = 5 * t_val 
                prob_text = theme["context"].format(v0=v0)
                solutions_for_pdf.append(f"식: \\( -5t^2 + {v0}t = 0 \\)<br>정답: \\( t = {t_val} \\)")
                
            problems_for_pdf.append(prob_text)
            st.markdown(f"**Q.** {prob_text}", unsafe_allow_html=True)
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"):
                st.success(f"**최종 정답:** 완료")

        elif curr_type == "삼차방정식":
            while True:
                r1, r2, r3 = random.randint(-3, 3), random.randint(-3, 3), random.randint(-3, 3)
                r_tuple = tuple(sorted([r1, r2, r3]))
                if r_tuple not in used_problems:
                    used_problems.add(r_tuple)
                    break
            expr = (x - r1) * (x - r2) * (x - r3)
            eq_expanded = sp.expand(expr)
            problems_for_pdf.append(sp.latex(eq_expanded))
            sign1, sign2, sign3 = ("+" if -r1 > 0 else "-"), ("+" if -r2 > 0 else "-"), ("+" if -r3 > 0 else "-")
            roots = list(set([r1, r2, r3]))
            roots_str_pdf = " 또는 ".join([f"\\( x = {r} \\)" for r in roots])
            roots_str_ui = " 또는 ".join([f"$x = {r}$" for r in roots])
            solutions_for_pdf.append(f"인수분해: \\( (x {sign1} {abs(r1)})(x {sign2} {abs(r2)})(x {sign3} {abs(r3)}) = 0 \\)\n정답: {roots_str_pdf}")
            st.latex(f"{sp.latex(eq_expanded)} = 0")
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"): 
                st.success(f"**최종 정답:** {roots_str_ui}")

        elif curr_type == "삼차방정식 (스토리텔링 융합) 🌟":
            if not current_pool:
                current_pool = STORY_THEMES["삼차방정식"].copy()
                random.shuffle(current_pool)
            
            theme = current_pool.pop()
            
            if "cm 더" in theme["context"] or "m 더" in theme["context"]: 
                x_val = random.randint(3, 6) 
                h_diff = random.choice([-2, -1, 1, 2])
                h_val = x_val + h_diff
                vol = (x_val**2) * h_val
                word = "깁" if h_diff > 0 else "짧"
                prob_text = theme["context"].format(abs_h_diff=abs(h_diff), word=word, vol=vol)
                solutions_for_pdf.append(f"식: \\( x^2(x {'+' if h_diff>0 else '-'} {abs(h_diff)}) = {vol} \\)<br>정답: \\( x = {x_val} \\)")
            else: 
                x_val = random.randint(3, 7)
                vol = (x_val - 1) * x_val * (x_val + 1)
                prob_text = theme["context"].format(vol=vol)
                solutions_for_pdf.append(f"식: \\( (x-1)x(x+1) = {vol} \\)<br>정답: \\( x = {x_val} \\)")
                
            problems_for_pdf.append(prob_text)
            st.markdown(f"**Q.** {prob_text}", unsafe_allow_html=True)
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"):
                st.success(f"**최종 정답:** 완료")

        elif "개념 확인 OX 퀴즈" in curr_type:
            if "일차" in curr_type:
                bank = [{"q": "\\( x \\)에 대한 일차방정식은 항상 단 1개의 해를 가진다. (단, 계수는 0이 아니다.)", "a": "O", "exp": "일차방정식은 기울기를 가진 직선과 같아 \\( x \\)축과 한 점에서만 만나므로 단 하나의 실근을 가집니다."},
                        {"q": "방정식의 양변에 같은 수를 곱하거나 나누어도 등식은 항상 성립한다. (단, 0은 제외)", "a": "O", "exp": "등식의 성질이며, 이를 이용해 이항을 하고 해를 구합니다."}]
            elif "이차" in curr_type:
                bank = [{"q": "이차방정식은 항상 서로 다른 두 개의 해를 가진다.", "a": "X", "exp": "중근을 가지거나 실근이 없을 수도 있습니다."},
                        {"q": "이차방정식 \\( x^2 = 0 \\) 은 해가 존재하지 않는다.", "a": "X", "exp": "\\( x = 0 \\) 이라는 한 개의 해(중근)를 가집니다."}]
            else:
                bank = [{"q": "모든 삼차방정식은 실수 범위에서 적어도 하나의 해(실근)를 반드시 가진다.", "a": "O", "exp": "삼차함수의 그래프는 \\( x \\)축을 최소 한 번은 통과하므로 실근이 반드시 존재합니다."}]
            
            avail = [q for q in bank if q["q"] not in used_problems]
            if not avail:
                used_problems.difference_update([q["q"] for q in bank])
                avail = bank
            ox = random.choice(avail)
            used_problems.add(ox["q"])
            
            problems_for_pdf.append(ox["q"])
            solutions_for_pdf.append(f"정답: {ox['a']}\n해설: {ox['exp']}")
            st.markdown(f"**Q.** {ox['q'].replace(r'\(', '$').replace(r'\)', '$')}")
            with st.expander(f"💡 {i}번 정답 확인"): 
                if ox["a"] == "O": st.success(f"**정답: O**")
                else: st.error(f"**정답: X**")

    # -----------------------------------------------------------
    # 다운로드 버튼 (HTML 파일 다운로드로 완벽 변경)
    # -----------------------------------------------------------
    st.markdown("---")
    st.info("💡 **출력 꿀팁:** 다운로드한 HTML 파일을 열고 **인쇄(Ctrl+P) 버튼**을 눌러 **'PDF로 저장'**을 선택하시면 수식이 완벽하게 유지된 깔끔한 시험지가 완성됩니다!")
    
    with st.spinner('시험지를 준비하는 중...'):
        problem_html = create_html_document(st.session_state.saved_math_type, problems_for_pdf, is_solution=False)
        solution_html = create_html_document(st.session_state.saved_math_type, solutions_for_pdf, is_solution=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📄 [학생용] 문제지 다운로드", data=problem_html, file_name=f"문제지.html", mime="text/html")
    with col2:
        st.download_button("💡 [교사용] 해설지 다운로드", data=solution_html, file_name=f"해설지.html", mime="text/html")
