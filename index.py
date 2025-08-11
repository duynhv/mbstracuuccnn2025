import streamlit as st
import pandas as pd

st.set_page_config(page_title="KẾT QUẢ QUY ĐỔI CHỨNG CHỈ NGOẠI NGỮ, ĐIỂM CỘNG", layout="wide")
st.markdown(
    """
    <div style="text-align: center;">
        <p style="color: #003366; font-weight: bold; font-size: 30px; margin: 0;">
            BỘ GIÁO DỤC VÀ ĐÀO TẠO
        </p>
        <p style="color: #003366; font-weight: bold; font-size: 40px; margin: 0;">
            TRƯỜNG ĐẠI HỌC MỞ THÀNH PHỐ HỒ CHÍ MINH
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Tiêu đề chính
st.markdown(
    "<h1 style='text-align: center; color: #003366; font-size: 28px;'>KẾT QUẢ QUY ĐỔI CHỨNG CHỈ NGOẠI NGỮ, ĐIỂM CỘNG 2025</h1>",
    unsafe_allow_html=True
)


st.markdown("""
    <style>
    /* Màu nền và bo góc cho tab */
    .stTabs [role="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        font-weight: 900; /* siêu đậm */
        font-size: 16px;  /* to hơn một chút */
        color: black;     /* màu chữ */
    }
    /* Tab 1 */
    .stTabs [role="tab"]:nth-child(1) {
        background-color: #ffcccc;
    }
    /* Tab 2 */
    .stTabs [role="tab"]:nth-child(2) {
        background-color: #ccffcc;
    }
    /* Tab 3 */
    .stTabs [role="tab"]:nth-child(3) {
        background-color: #ccccff;
    }
    /* Khi tab được chọn thì viền nổi bật */
    .stTabs [role="tab"][aria-selected="true"] {
        border: 2px solid #000;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    /* Tăng cỡ chữ toàn bộ giao diện */
    html, body, [class*="css"]  {
        font-size: 20px !important;
    }

    /* Label của các input */
    label {
        font-size: 20px !important;
        font-weight: bold;
    }

    /* Ô nhập số */
    .stNumberInput input {
        font-size: 20px !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

sheet_id = "17Iw8SOtKuF2xITDPygIfRcTQCyDGcVztTsPZrROeg40"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"

@st.cache_data
def load_data():
    df = pd.read_csv(url, dtype={"Số ĐDCN": str})  
    df.columns = df.columns.str.strip() 
    df["Số ĐDCN"] = df["Số ĐDCN"].str.strip().str.upper()
    return df

df = load_data()

ddcn = st.text_input("Thí sinh nhập số ĐDCN:", key="ddcn_input").strip().upper()

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #007BFF;
        color: white;
        height: 48px;
        font-size: 18px;
        width: 100%;
        border-radius: 5px;
    }
    div.stButton > button:first-child:hover {
        background-color: #0056b3;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

if ("searched_once" not in st.session_state) and ddcn:
    st.session_state["searched_once"] = True
    search_trigger = True
else:
    search_trigger = st.button("Tra cứu")

if search_trigger:
    if not ddcn:
        st.warning("Vui lòng nhập số ĐDCN.")
    else:
        ket_qua = df[df["Số ĐDCN"] == ddcn]
        if ket_qua.empty:
            st.error("Không tìm thấy kết quả cho số ĐDCN này.")
        else:
            cols_to_show = ["Số ĐDCN", "Họ tên", "Loại chứng chỉ ngoại ngữ", "Quy đổi ngoại ngữ", "ĐIỂM CỘNG"]
            ket_qua = ket_qua[cols_to_show].copy()
            ket_qua["ĐIỂM CỘNG"] = ket_qua["ĐIỂM CỘNG"].replace({None: ""}).fillna("")
            row = ket_qua.iloc[0]

            # Bảng HTML canh giữa
            html_table = f"""
            <div style="display: flex; justify-content: center;">
                <table border="1" style="border-collapse: collapse; font-size: 22px; color: #003366;">
                    <tr><td style="padding: 10px;"><b>Số ĐDCN:</b></td><td style="padding: 10px;">{row['Số ĐDCN']}</td></tr>
                    <tr><td style="padding: 10px;"><b>Họ và tên:</b></td><td style="padding: 10px;">{row['Họ tên']}</td></tr>
                    <tr><td style="padding: 10px;"><b>Loại chứng chỉ ngoại ngữ:</b></td><td style="padding: 10px;">{row['Loại chứng chỉ ngoại ngữ']}</td></tr>
                    <tr><td style="padding: 10px;"><b>Quy đổi ngoại ngữ:</b></td><td style="padding: 10px;">{row['Quy đổi ngoại ngữ']}</td></tr>
                    <tr><td style="padding: 10px;"><b>ĐIỂM CỘNG:</b></td><td style="padding: 8px;">{row['ĐIỂM CỘNG']}</td></tr>
                </table>
            </div>
            """
            st.markdown(html_table, unsafe_allow_html=True)

            # Ghi chú sau bảng
           # Ghi chú sau bảng với màu xanh
            st.markdown("""
            <div style="color: #003366; font-size: 20px;">
            <b>Lưu ý:</b><br>
            - Thí sinh trúng tuyển cần nộp minh chứng cho Trường để tiến hành thẩm tra theo quy định.<br>
            - Trường hợp Thí sinh không cung cấp minh chứng, Trường sẽ ra quyết định kỷ luật.
            </div>
            """, unsafe_allow_html=True)


