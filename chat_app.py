import streamlit as st
from groq import Groq
import random

# 1. إعداد الواجهة والاسم
st.set_page_config(page_title="Nutri - AI Advisor", page_icon="🍏", layout="centered")

# --- إدارة حالة الثيم (Dark/Light Mode) ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# تحديد الألوان لضمان التباين (Contrast)
if st.session_state.theme == "dark":
    bg_gradient = "linear-gradient(135deg, #090a0f 0%, #13151f 50%, #0d1117 100%)"
    solid_bg = "#090a0f"
    text_color = "#ffffff"
    sub_text_color = "#94a3b8"
    btn_bg = "#1e293b"
    btn_border = "#334155"
else:
    bg_gradient = "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%)"
    solid_bg = "#f8fafc"
    text_color = "#0f172a"
    sub_text_color = "#475569"
    btn_bg = "#ffffff"
    btn_border = "#cbd5e1"

# --- شريط الأدوات العلوي (Control Panel) ---
# وضعنا الأزرار في مساحة صغيرة في الأعلى لتركيز الانتباه
col_theme, col_clear, col_save, _ = st.columns([1, 1, 1, 4])

with col_theme:
    button_label = "☀️ ساطع" if st.session_state.theme == "dark" else "🌙 مظلم"
    st.button(button_label, on_click=toggle_theme, use_container_width=True)

with col_clear:
    if st.button("🗑️ مسح", use_container_width=True, help="بدء حوار جديد"):
        # عند المسح، نحتفظ فقط ببرومبت النظام ونولد أسئلة جديدة
        if "expert_domain" in st.session_state and st.session_state.expert_domain:
            temp_domain = st.session_state.expert_domain
            sys_p = f"أنت 'Nutri'، خبير ومستشار ذكي متخصص في مجال: '{temp_domain}'. وجه إجاباتك بناءً على هذا التخصص بدقة علمية وهندسية عالية. حدودك الصارمة: لا تقدم تشخيصاً طبياً بشرياً علاجياً. أسلوبك: دقيق، ومنظم."
        else:
            sys_p = f"أنت 'Nutri'، خبير ومستشار ذكي عام في تكنولوجيا وتصنيع الأغذية وكيمياءها. حدودك الصارمة: لا تقدم تشخيصاً طبياً بشرياً علاجياً. أسلوبك: دقيق، ومنظم كالمهندس."
        
        st.session_state.messages = [{"role": "system", "content": sys_p}]
        st.session_state.random_suggestions = random.sample([
            "كيف نتحكم في التفاعلات الكيميائية وتغيرات الألوان أثناء تصنيع المنتجات الغذائية؟",
            "ما هي المعايير الأساسية للرقابة على الجودة وضمان سلامة الأغذية المصنعة؟",
            "كيف يتم تصميم وتطوير خطوط إنتاج وتعبئة الأغذية بكفاءة عالية؟",
            "ما هي تأثيرات عمليات الحفظ والحرارة على القيمة الغذائية للمنتج؟",
            "كيف نبتكر وصفات وتركيبات (Formulation) جديدة تناسب متطلبات الأسواق؟",
            "ما هي الطرق العلمية المتبعة للسيطرة على نمو الميكروبات وفساد الأغذية؟"
        ], 3)
        st.rerun()

with col_save:
    if "messages" in st.session_state:
        chat_export = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages if msg['role'] != 'system'])
        st.download_button(
            label="📥 حفظ",
            data=chat_export,
            file_name="nutri_chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )

# --- التنسيقات البصرية المتقدمة ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Cairo', sans-serif !important;
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        background: {bg_gradient} !important;
    }}

    [data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}

    /* توسيط دقيق */
    .stMarkdown .centered-title {{
        text-align: center !important;
        font-weight: 700 !important;
        color: {text_color} !important;
        margin-bottom: 0px !important;
    }}
    
    .stMarkdown .centered-subtitle {{
        text-align: center !important;
        color: {sub_text_color} !important;
        font-size: 14px !important;
        margin-top: 5px !important;
        direction: rtl !important;
    }}

    .stMarkdown .centered-footer {{
        text-align: center !important;
        color: #64748b !important;
        font-size: 13px !important;
        direction: ltr !important; 
    }}

    /* نصوص المحادثة */
    .stMarkdown p, .stChatMessage p, li, ul, ol {{
        direction: rtl;
        text-align: right; 
        color: {text_color} !important;
    }}

    /* الأزرار العلوية والمقترحات */
    .stButton > button, .stDownloadButton > button {{
        background-color: {btn_bg} !important;
        color: {text_color} !important;
        border: 1px solid {btn_border} !important;
    }}
    .stButton > button p, .stDownloadButton > button p {{
        color: {text_color} !important;
    }}

    /* الحقول والإدخالات */
    div[data-testid="stSelectbox"] label p {{
        direction: rtl !important;
        text-align: right !important;
    }}
    div[data-baseweb="select"] {{
        direction: rtl !important;
        background-color: {btn_bg} !important;
        border: 1px solid {btn_border} !important;
    }}
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {{
        color: {text_color} !important;
    }}
    ul[role="listbox"] {{
        direction: rtl !important;
        text-align: right !important;
    }}

    div[data-testid="stChatInput"] {{
        direction: rtl !important;
    }}
    .stChatInputContainer {{
        background-color: {btn_bg} !important;
        border: 1px solid {btn_border} !important;
        border-radius: 12px !important;
        direction: rtl !important;
    }}
    .stChatInputContainer textarea, .stChatInputContainer p {{
        color: {text_color} !important;
        text-align: right !important;
        direction: rtl !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. العنوان في المنتصف
st.markdown("<br>", unsafe_allow_html=True)
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

# 4. عرض الأسئلة المقترحة في المنتصف (تختفي بمجرد بدء المحادثة)
# إذا كان طول الرسائل 1 (يعني مفيش غير برومبت النظام اللي مش بيظهر للمستخدم)
if len(st.session_state.messages) == 1:
    st.markdown("<p style='text-align: right; color: #94a3b8; font-size: 14px; margin-bottom: 10px;'>💡 أسئلة مقترحة للبدء:</p>", unsafe_allow_html=True)
    for q in st.session_state.random_suggestions:
        if st.button(q, use_container_width=True, key=f"sugg_{q}"):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

# 5. عرض رسائل الشات السابقة
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# الآلية الموحدة للرد التلقائي
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        try:
            stream = Groq(api_key=st.secrets["GROQ_API_KEY"]).chat.completions.create(
                messages=st.session_state.messages,
                model="qwen/qwen3.8-27b",
                temperature=0.2,
                max_tokens=4000,
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

# 6. صندوق الإدخال التقليدي
user_input = st.chat_input("اسأل Nutri عن أي استشارة غذائية...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# التوقيع
st.markdown("---")
st.markdown(
    "<p class='centered-footer'>Designed & Developed 🚀 by <b>Hazem El-Helw</b></p>", 
    unsafe_allow_html=True
)
