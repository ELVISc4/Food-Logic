import streamlit as st
from groq import Groq
import random

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

# 3. اختيار مجال الاستشارة التخصصي (بدون مصطلحات معقدة ومجالات أوسع)
domain = st.selectbox(
    "اختر مجال الاستشارة التخصصي:",
    [
        "كيمياء وتحليل الأغذية",
        "سلامة وصحة الغذاء وتأمين الجودة",
        "هندسة وتصنيع خطوط الإنتاج",
        "التغذية البشرية والتغذية العلاجية",
        "تطوير المنتجات والابتكار الغذائي",
        "ميكروبيولوجيا والأحياء الدقيقة للأغذية"
    ],
    key="expert_domain"
)

# تعزيز الالتزام التام بالمجال المختار في دستور النظام (System Prompt)
system_prompt = (
    f"أنت 'Nutri'، خبير ومستشار ذكي متخصص حصرياً وفي العمق في مجال: '{domain}'. "
    f"يجب أن تكون إجاباتك موجهة وممركزة بشكل كامل وصرام حول هذا المجال المحدد فقط، وتجنب الخروج عنه إلا لربطه بالسياق المباشر. "
    f"حدودك الصارمة: لا تقدم تشخيصاً طبياً بشرياً علاجياً للمرضى بل استشارات تخصصية. أسلوبك: دقيق، علمي، ومنظم كالمهندس."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
else:
    st.session_state.messages[0]["content"] = system_prompt

# 4. بنك الأسئلة المتنوعة بدون اختصارات وبناءً على المجالات المحدثة
question_bank = [
    "كيف نتحكم في التفاعلات الكيميائية وتغيرات الألوان أثناء تصنيع المنتجات الغذائية؟",
    "ما هي المعايير الأساسية للرقابة على الجودة وضمان سلامة الأغذية المصنعة؟",
    "كيف يتم تصميم وتطوير خطوط إنتاج وتعبئة الأغذية بكفاءة عالية؟",
    "ما هي تأثيرات عمليات الحفظ والحرارة على القيمة الغذائية للمنتج؟",
    "كيف نبتكر وصفات وتركيبات (Formulation) جديدة تناسب متطلبات الأسواق؟",
    "ما هي الطرق العلمية المتبعة للسيطرة على نمو الميكروبات وفساد الأغذية؟"
]

random_suggestions = random.sample(question_bank, 3)

# توسيط شريط الأدوات بالكامل في منتصف الشاشة
_, col_btn1, col_btn2, col_btn3, _ = st.columns([1.5, 1, 1, 1, 1.5])

with col_btn1:
    if st.button("🗑️ مسح", use_container_width=True, help="مسح المحادثة وبدء حوار جديد"):
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        st.rerun()

with col_btn2:
    chat_export = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages if msg['role'] != 'system'])
    st.download_button(
        label="📥 حفظ",
        data=chat_export,
        file_name="nutri_chat_history.txt",
        mime="text/plain",
        help="تصدير المحادثة",
        use_container_width=True
    )

with col_btn3:
    with st.popover("💡 مقترحة", use_container_width=True, help="أسئلة تقنية تتجدد عند كل تحديث"):
        st.markdown("**أسئلة مقترحة متجددة:**")
        for q in random_suggestions:
            if st.button(q, use_container_width=True, key=q):
                st.session_state.messages.append({"role": "user", "content": q})
                st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 5. عرض رسائل الشات السابقة
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# الآلية الموحدة للرد التلقائي مع التركيز الصارم على المجال
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
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

# صندوق الإدخال التقليدي
user_input = st.chat_input("اسأل Nutri عن تخصصك المختار...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# 6. التوقيع الهندسي في الأسفل
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-family: Cairo; font-size: 13px;'>Designed & Developed 🚀 by <b>Hazem El-Helw</b></p>", 
    unsafe_allow_html=True
)
