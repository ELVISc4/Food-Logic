import streamlit as st
from groq import Groq

# 1. إعداد الواجهة والاسم
st.set_page_config(page_title="Nutri - AI Advisor", page_icon="🍏")
st.title("🍏 Nutri - AI Advisor")

# --- إضافة توقيعك الهندسي في الشريط الجانبي (Sidebar) ---
st.sidebar.title("System Info")
st.sidebar.markdown("---")
st.sidebar.markdown("### Developed by:")
st.sidebar.markdown("🚀 **Hazem El-Helw**")
st.sidebar.markdown("Food Technologist")
st.sidebar.markdown("---")

# 2. قراءة المفتاح بأمان من إعدادات المنصة السحابية
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. ذاكرة المحادثة ودستور النظام
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنت 'Nutri'، خبير ومستشار ذكي في تكنولوجيا وتصنيع الأغذية. حدودك الصارمة: لا تقدم تشخيصاً طبياً. أسلوبك: دقيق ومنظم كالمهندس."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

user_input = st.chat_input("اسأل Nutri عن كيمياء الأغذية والتصنيع...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="qwen/qwen3.8-27b",
                temperature=0.2,
                max_tokens=1024,
            )
            answer = chat_completion.choices[0].message.content
            response_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"حدث خطأ شبكي: {e}")
