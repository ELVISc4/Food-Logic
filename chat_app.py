import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import random
import time

# 1. إعداد الواجهة
st.set_page_config(page_title="Nutri - AI Advisor", page_icon="🍏", layout="centered")

# --- إدارة حالة الثيم ---
if "theme" not in st.session_state:
    if "theme" in st.query_params:
        st.session_state.theme = st.query_params["theme"]
    else:
        st.session_state.theme = "light"

def toggle_theme():
    new_theme = "dark" if st.session_state.theme == "light" else "light"
    st.session_state.theme = new_theme
    st.query_params["theme"] = new_theme

# --- الألوان والصناديق ---
if st.session_state.theme == "dark":
    bg_gradient = "radial-gradient(circle at center, #061c11 0%, #090a0f 60%, #050505 100%)"
    text_color = "#f8fafc"
    sub_text_color = "#94a3b8"
    btn_bg = "#0f172a"
    btn_border = "#166534" 
    assistant_bg = "rgba(15, 23, 42, 0.7)" # خلفية صندوق لوسي في الدارك
    chat_user_bg = "rgba(255, 255, 255, 0.05)" # خلفية صندوق المستخدم في الدارك
else:
    bg_gradient = "radial-gradient(circle at center, #ffffff 0%, #f4fdf8 40%, #d1fae5 100%)"
    text_color = "#0f172a"
    sub_text_color = "#475569"
    btn_bg = "#ffffff"
    btn_border = "#a7f3d0"
    assistant_bg = "rgba(255, 255, 255, 0.9)" # خلفية صندوق لوسي في اللايت
    chat_user_bg = "rgba(209, 250, 229, 0.3)" # خلفية صندوق المستخدم في اللايت (أخضر خفيف جداً)

# --- بناء الهوية الاستراتيجية الصارمة (System Override) ---
base_identity = (
    "اسمك هو 'لوسي' (Lucy). أنتِ مستشارة ذكية ومتقدمة. "
    "تم تطويرك وبرمجتك حصرياً بواسطة التكنولوجست 'حازم الحلو' بهدف نشر الوعي والتطوير في الصناعات الغذائية. "
    "تعليمات صارمة جداً: إذا سألك أي شخص عن هويتك، ما اسمك، من صنعك، أو أي سؤال مشابه، يجب أن تجيبي بهذه الهوية فقط. "
    "يُمنع منعاً باتاً ذكر كلمات مثل (Qwen، Tongyi Lab، Alibaba، أو أي نماذج لغوية أخرى). كوني فخورة بهويتك الجديدة كـ 'لوسي'. "
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": base_identity}]

def get_smart_suggestions():
    general = [
        "من أنتِ ومن قام بتطويرك؟", # سؤال مضاف لاختبار الهوية
        "ما هي أفضل الأنظمة الغذائية لزيادة التركيز خلال اليوم؟",
        "كيف يمكنني حساب احتياجاتي من البروتين والكربوهيدرات؟",
        "كيف أقرأ البطاقة الغذائية (Nutrition Facts) بشكل صحيح؟",
        "هل الصيام المتقطع مناسب للجميع؟"
    ]
    specialized = [
        "كيف نتحكم في تغيرات الألوان أثناء تصنيع المنتجات؟",
        "ما هي معايير الـ HACCP في خطوط الإنتاج؟",
        "كيف نبتكر تركيبات (Formulation) جديدة للأسواق؟"
    ]
    selected = random.sample(general, 2) + random.sample(specialized, 1)
    random.shuffle(selected)
    return selected

# --- شريط الأدوات العلوي ---
col_theme, col_clear, col_save, _ = st.columns([1, 1, 1, 4])

with col_theme:
    button_label = "🌙 مظلم" if st.session_state.theme == "light" else "☀️ ساطع"
    st.button(button_label, on_click=toggle_theme, use_container_width=True)

with col_clear:
    if st.button("🗑️ مسح", use_container_width=True):
        domain = st.session_state.get("expert_domain", "")
        domain_prompt = f"أنتِ أيضاً خبيرة متخصصة في: {domain}." if domain else "أنتِ خبيرة في التغذية العامة وتكنولوجيا الأغذية."
        st.session_state.messages = [{"role": "system", "content": base_identity + domain_prompt}]
        st.session_state.random_suggestions = get_smart_suggestions()
        st.rerun()

with col_save:
    chat_export = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages if msg['role'] != 'system'])
    st.download_button("📥 حفظ", data=chat_export, file_name="nutri_chat.txt", mime="text/plain", use_container_width=True)

# --- التنسيقات البصرية لهندسة صناديق الرسائل (Chat Bubbles) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Cairo', sans-serif !important; }}
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{ background: {bg_gradient} !important; }}
    [data-testid="stHeader"], [data-testid="stSidebar"] {{ display: none !important; }}
    [data-testid="stBottom"], [data-testid="stBottom"] > div {{ background-color: transparent !important; }}

    /* هندسة صناديق الرسائل بشكل احترافي */
    div[data-testid="stChatMessage"] {{ 
        background-color: {assistant_bg} !important; 
        border: 1px solid {btn_border} !important; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); /* تظليل ناعم يعطي عمق 3D */
    }}
    div[data-testid="stChatMessage"]:nth-child(even) {{ 
        background-color: {chat_user_bg} !important; 
    }}
    
    .animated-header {{ text-align: center !important; font-weight: 700 !important; color: {text_color} !important; margin-bottom: 0px !important; direction: rtl !important; display: flex; justify-content: center; align-items: center; gap: 10px; }}
    @keyframes popIn {{ 0% {{ transform: scale(0) rotate(-15deg); opacity: 0; }} 70% {{ transform: scale(1.2) rotate(10deg); opacity: 1; }} 100% {{ transform: scale(1) rotate(0deg); opacity: 1; }} }}
    .apple-icon {{ display: inline-block; animation: popIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }}
    
    .stMarkdown p, .stChatMessage p, li, ul, ol {{ direction: rtl; text-align: right; color: {text_color} !important; }}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, h4, h5, h6 {{ color: {text_color} !important; direction: rtl; text-align: right; }}
    table {{ width: 100% !important; color: {text_color} !important; border-collapse: collapse !important; margin-bottom: 15px !important; }}
    th, td {{ border: 1px solid {btn_border} !important; color: {text_color} !important; padding: 8px !important; text-align: right !important; direction: rtl !important; background-color: transparent !important; }}
    th {{ background-color: {btn_bg} !important; font-weight: 700 !important; }}
    
    .stButton > button {{ background-color: {btn_bg} !important; color: {text_color} !important; border: 1px solid {btn_border} !important; }}
    div[data-testid="stSelectbox"] label p {{ direction: rtl !important; text-align: right !important; color: {text_color} !important; }}
    div[data-baseweb="select"], .stChatInputContainer {{ direction: rtl !important; background-color: {btn_bg} !important; border: 1px solid {btn_border} !important; }}
    div[data-baseweb="select"] span, .stChatInputContainer textarea, .stChatInputContainer p {{ color: {text_color} !important; text-align: right !important; direction: rtl !important; }}
    ul[role="listbox"] {{ direction: rtl !important; text-align: right !important; background-color: {btn_bg} !important; }}
    ul[role="listbox"] li {{ color: {text_color} !important; }}
    </style>
""", unsafe_allow_html=True)

st.markdown("<br><h1 class='animated-header'><span class='apple-icon'>🍏</span> Nutri - AI Advisor</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {sub_text_color}; font-size: 14px; direction: rtl;'>مستشارك الذكي في التغذية وتكنولوجيا الأغذية</p><hr>", unsafe_allow_html=True)

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

# تحديث الـ Prompt مع دمج الهوية والمجال
domain_prompt = f"أنتِ أيضاً خبيرة متخصصة في: {domain}." if domain else "أنتِ خبيرة في التغذية العامة وتكنولوجيا الأغذية."
st.session_state.messages[0]["content"] = base_identity + domain_prompt

if "random_suggestions" not in st.session_state:
    st.session_state.random_suggestions = get_smart_suggestions()

if len(st.session_state.messages) == 1:
    col_sugg_text, col_sugg_refresh = st.columns([5, 1])
    with col_sugg_text:
        st.markdown("<p style='text-align: right; color: #94a3b8; font-size: 14px;'>💡 أسئلة مقترحة:</p>", unsafe_allow_html=True)
    with col_sugg_refresh:
        if st.button("🔄", key="refresh_sugg"):
            st.session_state.random_suggestions = get_smart_suggestions()
            st.rerun()
    for q in st.session_state.random_suggestions:
        if st.button(q, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.trigger_scroll = True
            st.rerun()

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("لوسي تحلل البيانات وتصيغ الرد... ⏳"):
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
                        content = chunk.choices[0].delta.content
                        if content is not None:
                            yield content
                            time.sleep(0.015)
                            
                answer = st.write_stream(response_generator())
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"حدث خطأ شبكي: {e}")

user_input = st.chat_input("اسأل لوسي عن أي استشارة غذائية...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.trigger_scroll = True
    st.rerun()

st.markdown("<hr><p style='text-align: center; color: #64748b; font-size: 13px;'>Designed & Developed 🚀 by <b>Hazem El-Helw</b></p>", unsafe_allow_html=True)

if st.session_state.get("trigger_scroll"):
    components.html("""
        <script>
            window.parent.document.querySelector('.main').scrollTo({
                top: window.parent.document.querySelector('.main').scrollHeight,
                behavior: 'smooth'
            });
        </script>
    """, height=0)
    st.session_state.trigger_scroll = False
