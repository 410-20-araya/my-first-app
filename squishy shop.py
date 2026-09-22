import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ร้าน chubby squishy", layout="centered")

# สไตล์ CSS เพิ่มเติมเพื่อปรับแต่งหน้าตาให้ใกล้เคียงกับรูปภาพ
st.markdown("""
    <style>
    .title-text {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .summary-box {
        background-color: #fbf3d5;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0d0a0;
    }
    .total-box {
        border: 2px solid #555;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# หัวข้อหน้าเว็บ
# ----------------------------------------------------
st.markdown("<div class='title-text'>ร้าน chubby squishy</div>", unsafe_allow_html=True)

# รายการสินค้าและราคา
products = [
    {"name": "สกุชชี่ขนมปังชิ้นเล็ก ราคา 10 บาท", "price": 10},
    {"name": "สกุชชี่ขนมปังเหนียวหลากสี(สี่เหลี่ยม/กลม) ขนาดปกติ ราคา 15 บาท", "price": 15},
    {"name": "สกุชชี่เนย ราคา 20 บาท", "price": 20},
    {"name": "สกุชชี่รูปสัตว์ต่างๆ ขนาดปกติ ราคา 20 บาท", "price": 20},
    {"name": "สกุชชี่รูปอาหาร ขนาดปกติ ราคา 20 บาท", "price": 20},
    {"name": "สกุชชี่ชีสเนื้อหนีบ(แบบบีบแล้วไม่คืนตัว) ราคา 20 บาท", "price": 20},
    {"name": "NeeDoh Ice Mini (ก้อนน้ำแข็งบีบเล่นเนื้อซิลิโคน) ราคา 30 บาท", "price": 30},
]

# ----------------------------------------------------
# ส่วนเลือกสินค้า
# ----------------------------------------------------
col_prod, col_cart = st.columns([3, 1.5])

selected_quantities = {}
total_items = 0
total_price = 0

with col_prod:
    st.subheader("เลือกสินค้า")
    with st.container(border=True):
        for idx, item in enumerate(products):
            c_check, c_num = st.columns([3, 1])
            with c_check:
                # Checkbox เลือกสินค้า
                checked = st.checkbox(item["name"], key=f"chk_{idx}")
            with c_num:
                # ตัวเลือกจำนวนสินค้า (+/-)
                qty = st.number_input(
                    "จำนวน", 
                    min_value=1, 
                    value=20 if idx == 0 else 1, 
                    key=f"qty_{idx}", 
                    label_visibility="collapsed"
                )
            
            if checked:
                total_items += qty
                total_price += item["price"] * qty

with col_cart:
    # แสดงจำนวนสินค้าในตะกร้า
    st.markdown(f"### 🛒 จำนวนสินค้าในตะกร้า :green[{total_items}]")

st.write("")

# ----------------------------------------------------
# ส่วนโปรโมชั่น และ สรุปยอดชำระเงิน
# ----------------------------------------------------
col_promo, col_summary = st.columns([2, 1.5])

with col_promo:
    st.subheader("โปรโมชั่น & ส่วนลดพิเศษ")
    with st.container(border=True):
        p1 = st.checkbox("ซื้อครบ 99 บาท จัดส่งฟรี", value=True)
        p2 = st.checkbox("เก็บสะสมแต้มตัวปั๊มครบ 6 แต้ม รับ สกุชชี่ชีส เพิ่ม 1 ชิ้น ฟรี!!")
        p3 = st.checkbox("ซื้อสกุชชี่ ราคา 20/30 บาท ครบ 3 ชิ้น รับส่วนลด 10 บาท!!")

# คำนวณค่าจัดส่งและส่วนลดเบื้องต้น
shipping_cost = 35 if not (p1 and total_price >= 99) else 0
discount = 35 if p1 and total_price >= 99 else 0
final_total = total_price + shipping_cost - discount

with col_summary:
    # กล่องสรุปยอดชำระเงิน
    st.markdown("""
        <div class='summary-box'>
            <h4 style='text-align: center; margin-top: 0;'>สรุปยอดชำระเงิน</h4>
            <hr style='margin: 10px 0;'>
        </div>
    """, unsafe_allow_html=True)
    
    # ใช้ Container ซ้อนเพื่อใส่ข้อมูลตัวเลข
    with st.container(border=True):
        st.write(f"**ราคารวมสินค้า:** {total_price} บาท")
        st.write(f"**ค่าส่ง:** {shipping_cost} บาท")
        st.write(f"**ส่วนลดโปรโมชั่น (2):** -{discount} บาท")
        
        st.markdown(f"""
            <div class='total-box'>
                ⭐ ยอดสุทธิที่ต้องจ่าย: [ {final_total} บาท ]
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("ยืนยันการสั่งซื้อ (ชำระเงิน)", type="primary", use_container_width=True):
            st.success("ทำรายการสำเร็จ!")
