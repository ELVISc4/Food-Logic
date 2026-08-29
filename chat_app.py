import streamlit as st
from groq import Groq
import random

# 1. إعداد الواجهة والاسم
st.set_page_config(page_title="Nutri - AI Advisor", page_icon="🍏", layout="centered")

# --- إدارة حالة الثيم (Dark/Light Mode) ---
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

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

# --- دالة توليد الأسئلة المقترحة (النسبة: 2 عام : 1 تخصصي) ---
def get_smart_suggestions():
    general_questions = [
        "ما هي أفضل الأنظمة الغذائية لزيادة التركيز والطاقة خلال اليوم؟",
        "كيف يمكنني حساب احتياجاتي اليومية من البروتين والكربوهيدرات والدهون؟",
        "هل المحليات الصناعية آمنة كبديل للسكر الأبيض في الاستخدام اليومي؟",
        "كيف أقرأ البطاقة الغذائية (Nutrition Facts) على المنتجات بشكل صحيح؟",
        "ما هي أفضل الطرق الصحية لحفظ الطعام في المنزل بدون فقد قيمته الغذائية؟",
        "هل الصيام المتقطع مناسب للجميع، وما هي فوائده وأضراره؟",
        "ما هي الأطعمة التي تساعد في تحسين عملية الهضم وصحة الأمعاء؟",
        "كيف يمكنني التفرقة بين الجوع الحقيقي والجوع العاطفي؟"
    ]
    
    specialized_questions = [
        "كيف نتحكم في التفاعلات الكيميائية وتغيرات الألوان أثناء تصنيع المنتجات؟",
        "ما هي المعايير الأساسية لضمان سلامة الأغذية المصنعة (HACCP)؟",
        "كيف نبتكر وصفات وتركيبات (Formulation) جديدة تناسب الأسواق؟",
        "كيف يمكن تقييم كفاءة الأغلفة الصالحة للأكل في إطالة فترة الصلاحية؟",
        "ما هي أحدث تقنيات الرش المتناهي الصغر (Micro-atomization) في الأغذية؟",
        "كيف يمكن استغلال مخلفات التصنيع الغذائي لابتكار منتجات جديدة؟"
    ]
    
    # سحب سؤالين من العام وسؤال من التخصصي لضمان الأولوية
    selected = random.sample(general_questions, 2) + random.sample(specialized_questions, 1)
    random.shuffle(selected) # خلط الترتيب ليكون طبيعياً
    return selected

# --- شريط الأدوات العلوي (Control Panel) ---
col_theme, col_clear, col_save, _ = st.columns([1, 1, 1, 4])

with col_theme:
    button_label = "🌙 مظلم" if st.session_state.theme == "light" else "☀️ ساطع"
    st.button(button_label, on_click=toggle_theme, use_container_width=True)

with col_clear:
    if st.button("🗑️ مسح", use_container_width=True, help="بدء حوار جديد"):
        if "expert_domain" in st.session_state and st.session_state.expert_domain:
            temp_domain = st.session_state.expert_domain
            sys_p = f"أنت 'Nutri'، خبير ومستشار ذكي متخصص في مجال: '{temp_domain}'. وجه إجاباتك بناءً على هذا التخصص بدقة علمية. لا تقدم تشخيصاً طبياً علاجياً."
        else:
            sys_p = f"أنت 'Nutri'، خبير ومستشار ذكي في تكنولوجيا الأغذية والتغذية العامة. لا تقدم تشخيصاً طبياً علاجياً."
        
        st.session_state.messages = [{"role": "system", "content": sys_p}]
        st.session_state.random_suggestions = get_smart_suggestions()
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

# --- التنسيقات البصرية ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {{ font-family: 'Cairo', sans-serif !important; }}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{ background: {bg_gradient} !important; }}
    [data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}

    .stMarkdown .centered-title {{ text-align: center !important; font-weight: 700 !important; color: {text_color} !important; margin-bottom: 0px !important; }}
    .stMarkdown .centered-subtitle {{ text-align: center !important; color: {sub_text_color} !important; font-size: 14px !important; margin-top: 5px !important; direction: rtl !important; }}
    .stMarkdown .centered-footer {{ text-align: center !important; color: #64748b !important; font-size: 13px !important; direction: ltr !important; }}
    .stMarkdown p, .stChatMessage p, li, ul, ol {{ direction: rtl; text-align: right; color: {text_color} !important; }}

    .stButton > button, .stDownloadButton > button {{ background-color: {btn_bg} !important; color: {text_color} !important; border: 1px solid {btn_border} !important; }}
    .stButton > button p, .stDownloadButton > button p {{ color: {text_color} !important; }}

    div[data-testid="stSelectbox"] label p {{ direction: rtl !important; text-align: right !important; }}
    div[data-baseweb="select"] {{ direction: rtl !important; background-color: {btn_bg} !important; border: 1px solid {btn_border} !important; }}
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {{ color: {text_color} !important; }}
    ul[role="listbox"] {{ direction: rtl !important; text-align: right !important; }}

    div[data-testid="stChatInput"] {{ direction: rtl !important; }}
    .stChatInputContainer {{ background-color: {btn_bg} !important; border: 1px solid {btn_border} !important; border-radius: 12px !important; direction: rtl !important; }}
    .stChatInputContainer textarea, .stChatInputContainer p {{ color: {text_color} !important; text-align: right !important; direction: rtl !important; }}
    </style>
""", unsafe_allow_html=True)

# 2. العنوان
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h1 class='centered-title'>🍏 Nutri - AI Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p class='centered-subtitle'>مستشارك الذكي في التغذية وتكنولوجيا الأغذية</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. اختيار مجال الاستشارة
domains = [
    "التغذية البشرية والأنظمة الغذائية",
    "استشارة عامة في الأغذية",
    "كيمياء وتحليل الأغذية",
    "سلامة وصحة الغذاء وتأمين الجودة",
    "هندسة وتصنيع خطوط الإنتاج",
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
        f"أنت 'Nutri'، خبير ومستشار ذكي عام في التغذية وتكنولوجيا وتصنيع الأغذية وكيمياءها. "
        f"حدودك الصارمة: لا تقدم تشخيصاً طبياً بشرياً علاجياً. أسلوبك: دقيق، ومنظم كالمهندس."
    )

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
else:
    st.session_state.messages[0]["content"] = system_prompt

if "random_suggestions" not in st.session_state:
    st.session_state.random_suggestions = get_smart_suggestions()

# 4. عرض الأسئلة المقترحة وزر التحديث
if len(st.session_state.messages) == 1:
    st.markdown("<br>", unsafe_allow_html=True)
    col_sugg_text, col_sugg_refresh = st.columns([5, 1])
    with col_sugg_text:
        st.markdown("<p style='text-align: right; color: #94a3b8; font-size: 14px; margin-bottom: 0px;'>💡 أسئلة مقترحة للبدء:</p>", unsafe_allow_html=True)
    with col_sugg_refresh:
        if st.button("🔄", key="refresh_sugg", help="تحديث المقترحات"):
            st.session_state.random_suggestions = get_smart_suggestions()
            st.rerun()
            
    for q in st.session_state.random_suggestions:
        if st.button(q, use_container_width=True, key=f"sugg_{q}"):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

# 5. عرض الشات
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# الآلية للرد التلقائي
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

# 6. الإدخال
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
