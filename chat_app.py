import streamlit as st
from groq import Groq

# 1. إعداد الواجهة والاسم مع تفعيل التصميم الاحترافي
st.set_page_config(page_title="Nutri - AI Advisor", page_icon="🍏", layout="centered")

# --- تنسيقات CSS لحل مشاكل الخطوط، الاتجاه، والتداخل (RTL & Typography) ---
st.markdown("""
    <style>
    /* تغيير الخط الافتراضي بالكامل إلى خط عصري ونظيف */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }

    /* ضبط اتجاه النصوص العربية لتكون من اليمين لليسار ومنع تداخل الإنجليزي */
    .stChatMessage, .stTextInput, p, span, div {
        direction: rtl;
        text-align: right;
    }

    /* تخصيص صندوق الإدخال وجعله أكثر مرونة وجمالاً */
    .stChatInputContainer {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.title("🍏 Nutri - AI Advisor")

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

# --- توقيعك الهندسي المباشر أسفل الصفحة ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-family: Cairo;'>Designed & Developed 🚀 by <b>Leader Elvis</b></p>", 
    unsafe_allow_html=True
)
