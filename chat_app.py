import streamlit as st
from groq import Groq

# 1. إعداد الواجهة والاسم
st.set_page_config(page_title="Nutri - AI Advisor", page_icon="🍏", layout="centered")

# --- التنسيقات البصرية CSS المتقدمة (خط Cairo، تحسين الشات، وتوسيط العنوان) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }

    /* توسيط العنوان الرئيسي بشكل احترافي */
    .centered-title {
        text-align: center;
        font-weight: 700;
        margin-bottom: 0px;
    }

    /* ضبط اتجاه النصوص العربية والإنجليزية بسلاسة */
    .stChatMessage, .stTextInput, p, span, div {
        direction: rtl;
        text-align: right;
    }

    /* تحسين شكل صندوق الإدخال وتنعيمه */
    .stChatInputContainer {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. العنوان في المنتصف تماماً
st.markdown("<h1 class='centered-title'>🍏 Nutri - AI Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>مستشارك الذكي في كيمياء وتكنولوجيا الأغذية</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. الشريط الجانبي للإعدادات الذكية (Clean Cache & Controls)
with st.sidebar:
    st.markdown("### ⚙️ لوحة التحكم")
    st.markdown("---")
    
    # زر مسح الذاكرة (Clear Cache / Reset Chat)
    if st.button("🗑️ مسح المحادثة (Clear Chat)", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": "أنت 'Nutri'، خبير ومستشار ذكي في تكنولوجيا وتصنيع الأغذية. حدودك الصارمة: لا تقدم تشخيصاً طبياً. أسلوبك: دقيق ومنظم كالمهندس."}
        ]
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🚀 معلومات المطور")
    st.markdown("**Leader Elvis**")
    st.markdown("Food Tech & AI Engineer")

# 4. قراءة المفتاح بأمان من إعدادات المنصة السحابية
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 5. ذاكرة المحادثة ودستور النظام
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

# 6. التوقيع الهندسي في الأسفل
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-family: Cairo; font-size: 13px;'>Designed & Developed  🚀 by <b>Hazem El-Helw</b></p>", 
    unsafe_allow_html=True
)
