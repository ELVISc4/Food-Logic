import streamlit as st
from groq import Groq
import random

# 1. إعداد الواجهة والاسم
st.set_page_config(page_title="Nutri - AI Advisor", page_icon="🍏", layout="centered")

# --- التنسيقات البصرية المتقدمة وتوسيط النصوص وإصلاح المحاذاة ---
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

    /* توسيط العنوان الرئيسي والوصف بدقة تامة */
    .centered-title {
        text-align: center !important;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0px;
        width: 100%;
    }
    
    .centered-subtitle {
        text-align: center !important;
        color: #94a3b8;
        font-size: 14px;
        margin-top: 5px;
        width: 100%;
        display: block;
    }

    /* فرض الاتجاه الأيمن ومحاذاة النصوص بالكامل */
    .stMarkdown, .stChatMessage, p, span, div, li, ul, ol {
        direction: rtl !important;
        text-align: right !important;
    }

    /* ضبط مسافات وترتيب قوائم النقاط والترقيم للغة العربية */
    ul, ol {
        padding-right: 20px !important;
        padding-left: 0px !important;
        margin-right: 0px !important;
    }

    li {
        text-align: right !important;
        list-style-position: inside !important;
        margin-bottom: 6px;
    }

    /* تنسيق صندوق الإدخال */
    .stChatInputContainer {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. العنوان والوصف في المنتصف تماماً
st.markdown("<h1 class='centered-title'>🍏 Nutri - AI Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p class='centered-subtitle'>مستشارك الذكي في كيمياء وتكنولوجيا الأغذية</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. اختيار مجال الاستشارة
domains = [
    "استشارة عامة في الأغذية",
    "كيمياء وتحليل الأغذية",
    "سلامة وصحة الغذاء وتأمين الجودة",
    "هندسة وتصنيع خطوط الإنتاج",
    "التغذية البشرية والتغذية العلاجية",
    "تطوير المنتجات والابتكار الغذائي",
    "ميكروبيولوجيا والأحياء الدقيقة للأغذية"
]

domain = st.selectbox(
    "اختر مجال الاستشارة التخصصي:",
    options=domains,
    index=None,
    placeholder="اختر المجال أو اتركه عاماً...",
    key="expert_domain"
)

# تحديد دستور النظام بناءً على اختيار المستخدم أو الوضع العام
if domain:
    system_prompt = (
        f"أنت 'Nutri'، خبير ومستشار ذكي متخصص في مجال: '{domain}'. "
        f"وجه إجاباتك بناءً على هذا التخصص بدقة علمية وهندسية عالية. "
        f"حدودك الصارمة: لا تقدم تشخيصاً طبياً بشرياً علاجياً. أسلوبك: دقيق، ومنظم."
    )
else:
    system_prompt = (
        f"أنت 'Nutri'، خبير ومستشار ذكي عام في تكنولوجيا وتصنيع الأغذية وكيمياءها. "
        f"حدودك الصارمة: لا تقدم تشخيصاً طبياً بشرياً علاجياً. أسلوبك: دقيق، ومنظم كالمهندس."
    )

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
else:
    st.session_state.messages[0]["content"] = system_prompt

# 4. بنك الأسئلة وتثبيت المقترحات في الذاكرة
question_bank = [
    "كيف نتحكم في التفاعلات الكيميائية وتغيرات الألوان أثناء تصنيع المنتجات الغذائية؟",
    "ما هي المعايير الأساسية للرقابة على الجودة وضمان سلامة الأغذية المصنعة؟",
    "كيف يتم تصميم وتطوير خطوط إنتاج وتعبئة الأغذية بكفاءة عالية؟",
    "ما هي تأثيرات عمليات الحفظ والحرارة على القيمة الغذائية للمنتج؟",
    "كيف نبتكر وصفات وتركيبات (Formulation) جديدة تناسب متطلبات الأسواق؟",
    "ما هي الطرق العلمية المتبعة للسيطرة على نمو الميكروبات وفساد الأغذية؟"
]

if "random_suggestions" not in st.session_state:
    st.session_state.random_suggestions = random.sample(question_bank, 3)

# شريط الأدوات المنظم في منتصف الشاشة (مسح، حفظ، واختيار مقترح يغلق تلقائياً)
_, col_btn1, col_btn2, col_btn3, _ = st.columns([1, 1, 1, 1.5, 1])

with col_btn1:
    if st.button("🗑️ مسح", use_container_width=True, help="مسح المحادثة وبدء حوار جديد"):
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        st.session_state.random_suggestions = random.sample(question_bank, 3)
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
    # استخدام selectbox بدلاً من popover لكي تغلق القائمة تلقائياً فور اختيار السؤال
    selected_sugg = st.selectbox(
        "💡 أسئلة مقترحة",
        options=["اختر سؤالاً مقترحاً..."] + st.session_state.random_suggestions,
        key="suggestion_dropdown",
        label_visibility="collapsed"
    )
    if selected_sugg and selected_sugg != "اختر سؤالاً مقترحاً...":
        st.session_state.messages.append({"role": "user", "content": selected_sugg})
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 5. عرض رسائل الشات السابقة
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# الآلية الموحدة للرد التلقائي مع تفعيل أنيميشن الكتابة التدريجية (Streaming Typing Effect)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        try:
            stream = Groq(api_key=st.secrets["GROQ_API_KEY"]).chat.completions.create(
                messages=st.session_state.messages,
                model="qwen/qwen3.8-27b",
                temperature=0.2,
                max_tokens=1024,
                stream=True,
            )
            
            def response_generator():
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content

            answer = st.write_stream(response_generator())
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"حدث خطأ شبكي: {e}")

# صندوق الإدخال التقليدي
user_input = st.chat_input("اسأل Nutri عن أي استشارة غذائية...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# 6. التوقيع الهندسي في الأسفل
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-family: Cairo; font-size: 13px;'>Designed & Developed with 🚀 by <b>Hazem El-Helw</b></p>", 
    unsafe_allow_html=True
)
