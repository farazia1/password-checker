import streamlit as st
import re
import random
import string

# Page Config
st.set_page_config(page_title="Password Strength Checker", layout="centered")

# Background gradient via HTML
page_bg = """
<style>
body {
    background: linear-gradient(120deg, #a8ff78, #78ffd6);
    color: black;
}
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: black !important;
}
.password-input input {
    color: black !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Branding/Logo
st.markdown("<h1 style='text-align:center;'>🔐 RJ Secure Password Meter</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Check your password strength with suggestions & generate strong passwords</h4>", unsafe_allow_html=True)

# Sidebar - Security Tips
st.sidebar.title("💡 Security Tips")
st.sidebar.markdown("""
- Use **12+ characters**
- Avoid names/dates
- Use a mix of **uppercase**, **numbers**, and **symbols**
- Don't reuse passwords
""")

# Language Toggle
lang = st.sidebar.radio("🌐 Language", ("English", "Hindi"))

# Show/Hide Password
show_password = st.checkbox("👁️ Show Password")

# Password Input
password_input = st.text_input("Enter your password:", type="default" if show_password else "password")

# Password Criteria Checker
def check_password_strength(password):
    score = 0
    feedback = []
    checks = {
        "length": len(password) >= 8,
        "uppercase & lowercase": bool(re.search(r"[A-Z]", password)) and bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"\d", password)),
        "special char": bool(re.search(r"[!@#$%^&*]", password)),
        "not common": password.lower() not in ['password123', '123456', 'admin', 'qwerty', 'letmein', 'iloveyou']
    }

    for passed in checks.values():
        if passed:
            score += 1

    # Feedback
    if not checks["length"]:
        feedback.append("❌ Must be at least 8 characters.")
    if not checks["uppercase & lowercase"]:
        feedback.append("❌ Use both uppercase and lowercase letters.")
    if not checks["number"]:
        feedback.append("❌ Include at least one number.")
    if not checks["special char"]:
        feedback.append("❌ Add at least one special character (!@#$%^&*).")
    if not checks["not common"]:
        feedback.append("❌ This password is too common.")

    return score, feedback, checks

# Strength label
def get_strength_label(score):
    if score == 5:
        return "✅ Strong Password"
    elif score >= 3:
        return "⚠️ Moderate Password"
    else:
        return "❌ Weak Password"

# Password Generator
def generate_strong_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# Output
if password_input:
    score, feedback, checks = check_password_strength(password_input)
    
    st.subheader("🔍 Password Strength:")
    st.progress(score / 5)
    st.markdown(f"**{get_strength_label(score)}**")

    # Checklist style
    st.markdown("### 📋 Criteria")
    for key, passed in checks.items():
        st.write(f"{'✅' if passed else '❌'} {key.capitalize()}")

    # Suggestions
    if feedback:
        st.subheader("🔧 Suggestions to Improve:")
        for item in feedback:
            st.write(item)

    if score < 5:
        st.info("💡 Try adding a mix of characters, numbers, and symbols to increase security.")

st.markdown("---")

# Password Generator Section
st.subheader("🔁 Generate a Strong Password")

col1, col2 = st.columns([3, 1])
with col1:
    length = st.slider("Select password length", 8, 32, 12)
with col2:
    if st.button("🔄 Generate"):
        generated = generate_strong_password(length)
        st.success(f"`{generated}`")
        st.code(generated, language="text")
        st.markdown(f"<button onclick='navigator.clipboard.writeText(\"{generated}\")'>📋 Copy Password</button>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>Made with ❤️ by RJ Construction</p>", unsafe_allow_html=True)
