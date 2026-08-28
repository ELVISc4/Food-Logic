import streamlit as st
from groq import Groq

# 1. إعداد الواجهة والاسم
st.set_page_config(page_title="Nutri - AI Advisor", page_icon="🍏", layout="centered")

# --- التنسيقات البصرية المتقدمة (تدريج لوني، إخفاء الشريط المزعج، وتنسيق الخطوط) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }

    /* خلفية متدرجة احترافية (Gradient Background) تكسر الجمود البصري */
    .stApp {
        background: linear-gradient(160deg, #0d0d12 0%, #161622 50%, #0a0a0f 100%) !important;
    }

    /* إخفاء الشريط العلوي والشريط الجانبي تماماً لمنع أي فوضى بصرية */
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }

    /* توسيط العنوان الرئيسي */
    .centered-title {
        text-align: center;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0px;
    }
    
    .centered-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 14px;
        margin-top: 5px;
    }

    /* ضبط اتجاه النصوص العربية والإنجليزية بسلاسة */
    .stChatMessage, .stTextInput, p, span, div {
        direction: rtl;
        text-align: right;
    }

    /* تنسيق صندوق الإدخال */
    .stChatInputContainer {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. العنوان في المنتصف تماماً
st.markdown("<h1 class='centered-title'>🍏 Nutri - AI Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p class='centered-subtitle'>مستشارك الذكي في كيمياء وتكنولوجيا الأغذية</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. ذاكرة المحادثة ودستور النظام
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنت 'Nutri'، خبير ومستشار ذكي في تكنولوجيا وتصنيع الأغذية. حدودك الصارمة: لا تقدم تشخيصاً طبياً. أسلوبك: دقيق ومنظم كالمهندس."}
    ]

# شريط تحكم علوي صغير ونظيف داخل الصفحة (زر مسح المحادثة)
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🗑️ مسح", use_container_width=True, help="مسح المحادثة وبدء حوار جديد"):
        st.session_state.messages = [
            {"role": "system", "content": "أنت 'Nutri'، خبير ومستشار ذكي في تكنولوجيا وتصنيع الأغذية. حدودك الصارمة: لا تقدم تشخيصاً طبياً. أسلوبك: دقيق ومنظم كالمهندس."}
        ]
        st.rerun()

# عرض رسائل الشات
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
            chat_completion = client = Groq(api_key=st.secrets["GROQ_API_KEY"]).chat.completions.create(
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

# 4. التوقيع الهندسي في الأسفل
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-family: Cairo; font-size: 13px;'>Designed & Developed with 🚀 by <b>Hazem El-Helw</b></p>", 
    unsafe_allow_html=True
)
