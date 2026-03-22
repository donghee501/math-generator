import streamlit as st
import sympy as sp
import random

# 웹페이지 기본 설정
st.set_page_config(page_title="AI 수학 문제 생성기", page_icon="📝")
x = sp.Symbol('x')

# -----------------------------------------------------------
# ⭐ [클라우드 완벽 대응] HTML 문서 생성 함수 (PDF 변환 에러 원천 차단)
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
            body {{ font-family: 'Malgun Gothic', sans-serif; padding: 40px; }}
            h1 {{ text-align: center; border-bottom: 2px solid black; padding-bottom: 15px; }}
            .header-info {{ text-align: right; margin-bottom: 30px; font-size: 18px; }}
            .content-box {{ margin-bottom: 40px; font-size: 20px; line-height: 2.0; page-break-inside: avoid; }}
            .solution-box {{ color: #0033cc; font-size: 20px; margin-top: 15px; line-height: 2.0; page-break-inside: avoid; }}
            .MathJax_CHTML {{ font-size: 150% !important; }}
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
    
    # 텍스트 문서(HTML) 자체를 utf-8 포맷으로 안전하게 내보냅니다!
    return html_content.encode('utf-8')

# -----------------------------------------------------------
# 메인 UI 및 문제 생성 로직
# -----------------------------------------------------------
if 'run_id' not in st.session_state:
    st.session_state.run_id = 0
    st.session_state.saved_math_type = ""
    st.session_state.saved_num_prob = 0
    st.session_state.show_problems = False

st.title("🌟 수학 무한 문제 자동 생성기")
st.sidebar.header("⚙️ 출제 설정")

math_type = st.sidebar.radio("출제 단원을 선택하세요", [
    "일차방정식",
    "이차방정식 (하 - 정수 근)",
    "이차방정식 (중 - 분수 근)",
    "이차방정식 (상 - 근의 공식)",
    "삼차방정식"
])
num_prob = st.sidebar.slider("출제할 문제 개수", min_value=1, max_value=15, value=10)

if st.sidebar.button("🚀 문제지 생성하기"):
    st.session_state.run_id += 1 
    st.session_state.saved_math_type = math_type
    st.session_state.saved_num_prob = num_prob
    st.session_state.show_problems = True

if st.session_state.show_problems:
    random.seed(st.session_state.run_id)
    st.markdown("---")
    st.subheader(f"📝 {st.session_state.saved_math_type} 문제지")
    
    problems_for_pdf = []
    solutions_for_pdf = []
    
    for i in range(1, st.session_state.saved_num_prob + 1):
        curr_type = st.session_state.saved_math_type
        
        if curr_type == "일차방정식":
            root = random.randint(-10, 10)
            expr = x - root
            eq_expanded = sp.expand(expr)
            problems_for_pdf.append(sp.latex(eq_expanded))
            solutions_for_pdf.append(f"이항하여 정리하면 \\( x = {root} \\) 입니다.")
            
            st.latex(f"{sp.latex(eq_expanded)} = 0")
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"): 
                st.write("상수항을 우변으로 이항하여 기호를 바꾼 뒤 해를 구합니다.")
                st.success(f"**최종 정답:** $x = {root}$")

        elif curr_type == "이차방정식 (하 - 정수 근)":
            r1, r2 = random.randint(-9, 9), random.randint(-9, 9)
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
                st.write("1️⃣ 주어진 이차식을 두 일차식의 곱으로 인수분해합니다.")
                st.latex(rf"(x {sign1} {abs(r1)})(x {sign2} {abs(r2)}) = 0")
                st.write("2️⃣ 일차식이 각각 $0$이 되는 $x$의 값을 찾습니다.")
                st.success(f"**최종 정답:** $x = {r1}$ 또는 $x = {r2}$" if r1 != r2 else f"**최종 정답:** $x = {r1}$ (중근)")

        elif curr_type == "이차방정식 (중 - 분수 근)":
            a, c = random.randint(2, 5), random.randint(2, 5)
            b, d = random.randint(-7, 7), random.randint(-7, 7)
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
                st.write("1️⃣ 주어진 이차식을 인수분해합니다. (X자형 교차 곱셈 활용)")
                st.latex(rf"({a}x {sign1} {abs(b)})({c}x {sign2} {abs(d)}) = 0")
                st.write("2️⃣ 일차식의 해를 각각 구하기 위해 이항 후 앞의 계수로 나눕니다.")
                st.success(f"**최종 정답:** $x = {sp.latex(ans1)}$ 또는 $x = {sp.latex(ans2)}$" if ans1 != ans2 else f"**최종 정답:** $x = {sp.latex(ans1)}$ (중근)")

        elif curr_type == "이차방정식 (상 - 근의 공식)":
            a_val = random.choice([1, 2])
            b_val, c_val = random.randint(-5, 5), random.randint(-5, 5)
            D = b_val**2 - 4*a_val*c_val
            while D <= 0 or int(D**0.5)**2 == D or a_val == 0:
                a_val = random.choice([1, 2])
                b_val, c_val = random.randint(-5, 5), random.randint(-5, 5)
                D = b_val**2 - 4*a_val*c_val
                
            expr = a_val*x**2 + b_val*x + c_val
            problems_for_pdf.append(sp.latex(expr))
            
            roots = sp.solve(expr, x)
            solutions_for_pdf.append(f"근의 공식 대입: \\( a={a_val}, b={b_val}, c={c_val} \\)\n정답: \\( x = {sp.latex(roots[0])} \\) 또는 \\( x = {sp.latex(roots[1])} \\)")
            
            st.latex(f"{sp.latex(expr)} = 0")
            with st.expander(f"💡 {i}번 상세 풀이 및 정답"): 
                st.write("유리수 범위에서 쉽게 인수분해되지 않으므로, **근의 공식**을 사용합니다.")
                st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                st.write(f"1️⃣ 주어진 식에서 각 계수를 확인합니다: $a = {a_val}, b = {b_val}, c = {c_val}$")
                st.write("2️⃣ 근의 공식에 계수를 대입하여 계산합니다.")
                st.latex(rf"x = \frac{{-({b_val}) \pm \sqrt{{({b_val})^2 - 4 \cdot ({a_val}) \cdot ({c_val})}}}}{{2 \cdot ({a_val})}}")
                st.success(f"**최종 정답:** $x = {sp.latex(roots[0])}$ 또는 $x = {sp.latex(roots[1])}$")

        elif curr_type == "삼차방정식":
            r1, r2, r3 = random.randint(-3, 3), random.randint(-3, 3), random.randint(-3, 3)
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
                st.write("1️⃣ 조립제법 등을 이용하여 삼차식을 세 일차식의 곱으로 인수분해합니다.")
                st.latex(rf"(x {sign1} {abs(r1)})(x {sign2} {abs(r2)})(x {sign3} {abs(r3)}) = 0")
                st.write("2️⃣ 각 일차식이 $0$이 되는 $x$의 값을 찾습니다.")
                st.success(f"**최종 정답:** {roots_str_ui}")

    # -----------------------------------------------------------
    # ⭐ [업데이트] 웹 문서(HTML) 다운로드 버튼
    # -----------------------------------------------------------
    st.markdown("---")
    with st.spinner('시험지 문서를 생성하는 중입니다...'):
        problem_html_file = create_html_document(st.session_state.saved_math_type, problems_for_pdf, is_solution=False)
        solution_html_file = create_html_document(st.session_state.saved_math_type, solutions_for_pdf, is_solution=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📄 [학생용] 문제지 다운로드", data=problem_html_file, file_name=f"문제지_{st.session_state.saved_math_type}.html", mime="text/html")
    with col2:
        st.download_button("💡 [교사용] 해설지 다운로드", data=solution_html_file, file_name=f"해설지_{st.session_state.saved_math_type}.html", mime="text/html")
