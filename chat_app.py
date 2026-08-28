import streamlit as st
from groq import Groq

# 1. إعداد الواجهة والاسم
st.set_page_config(page_title="Nutri - AI Advisor", page_icon="🍏", layout="centered")

# --- التنسيقات البصرية CSS المتقدمة ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }

    /* خلفية متدرجة ديناميكية احترافية */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: linear-gradient(135deg, #090a0f 0%, #13151f 50%, #0d1117 100%) !important;
    }

    /* إخفاء الشريط العلوي والشريط الجانبي تماماً */
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

# شريط أدوات علوي منظم (مسح، حفظ، وأسئلة مقترحة)
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col2:
    if st.button("🗑️ مسح", use_container_width=True, help="مسح المحادثة وبدء حوار جديد"):
        st.session_state.messages = [
            {"role": "system", "content": "أنت 'Nutri'، خبير ومستشار ذكي في تكنولوجيا وتصنيع الأغذية. حدودك الصارمة: لا تقدم تشخيصاً طبياً. أسلوبك: دقيق ومنظم كالمهندس."}
        ]
        st.rerun()

with col3:
    chat_export = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages if msg['role'] != 'system'])
    st.download_button(
        label="📥 حفظ",
        data=chat_export,
        file_name="nutri_chat_history.txt",
        mime="text/plain",
        help="تصدير وتحميل المحادثة",
        use_container_width=True
    )

with col4:
    with st.popover("💡 مقترحة", use_container_width=True, help="أسئلة تقنية مقترحة"):
        st.markdown("**اختر سؤالاً استراتيجياً:**")
        if st.button("كيف أتحكم في نشاط الماء ($a_w$) للحفاظ على صلاحية المنتج؟", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "كيف أتحكم في نشاط الماء (aw) للحفاظ على صلاحية المنتج؟"})
            st.rerun()
        if st.button("ما هي خطوات تطبيق نظام HACCP بخطوط إنتاج الأغذية؟", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "ما هي خطوات تطبيق نظام HACCP بخطوط إنتاج الأغذية؟"})
            st.rerun()
        if st.button("ما تأثير تفاعلات ميلارد على جودة الأغذية؟", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "ما تأثير تفاعلات ميلارد على جودة الأغذية؟"})
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
            chat_completion = Groq(api_key=st.secrets["GROQ_API_KEY"]).chat.completions.create(
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
