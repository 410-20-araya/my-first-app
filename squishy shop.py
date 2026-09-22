import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ร้าน chubby squishy", layout="centered")

# สไตล์ CSS ปรับแต่งความสวยงาม
st.markdown("""
    <style>
    .title-text {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .promo-box-active {
        background-color: #d4edda;
        color: #155724;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin-bottom: 8px;
        font-weight: bold;
    }
    .promo-box-inactive {
        background-color: #f8f9fa;
        color: #6c757d;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 8px;
    }
    .summary-container {
        background-color: #fbf3d5;
        padding: 15px;
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

# ตัวแปรคำนวณ
total_items = 0
total_price = 0
items_20_30_count = 0

# ----------------------------------------------------
# ส่วนเลือกสินค้า
# ----------------------------------------------------
col_prod, col_cart = st.columns([3.2, 1.3])

with col_prod:
    st.subheader("เลือกสินค้า")
    with st.container(border=True):
        for idx, item in enumerate(products):
            c_check, c_num = st.columns([3, 1.2])
            
            # เช็คสภาวะ checkbox
            is_checked = st.session_state.get(f"chk_{idx}", False)
            
            with c_check:
                checked = st.checkbox(item["name"], key=f"chk_{idx}")
            
            # ถ้าติ๊กเลือก ให้ตั้งค่าเริ่มต้นเป็น 1 ถ้าไม่ติ๊กให้เป็น 0
            if checked:
                # ถ้าเพิ่งติ๊กครั้งแรกให้เริ่มที่ 1
                if f"qty_{idx}" not in st.session_state or st.session_state[f"qty_{idx}"] == 0:
                    st.session_state[f"qty_{idx}"] = 1
                
                with c_num:
                    qty = st.number_input(
                        "จำนวน", 
                        min_value=1, 
                        value=st.session_state[f"qty_{idx}"], 
                        key=f"qty_{idx}", 
                        label_visibility="collapsed"
                    )
                
                # สะสมค่าคำนวณ
                total_items += qty
                total_price += item["price"] * qty
                
                # นับจำนวนสินค้าประเภท 20/30 บาท
                if item["price"] in [20, 30]:
                    items_20_30_count += qty
            else:
                # หากไม่เลือกสินค้า ให้ตั้งค่าจำนวนเป็น 0
                st.session_state[f"qty_{idx}"] = 0

with col_cart:
    # แสดงจำนวนสินค้าในตะกร้า
    st.markdown(f"### 🛒 จำนวนสินค้าในตะกร้า :green[{total_items}]")

st.write("")

# ----------------------------------------------------
# ตรวจสอบเงื่อนไขโปรโมชั่น
# ----------------------------------------------------
promo1_active = total_price >= 99 and total_price > 0
promo2_active = total_items >= 6
promo3_active = items_20_30_count >= 3

# คำนวณส่วนลดและค่าจัดส่ง
shipping_cost = 0 if promo1_active else (35 if total_items > 0 else 0)
discount = 10 if promo3_active else 0
final_total = max(0, total_price + shipping_cost - discount)

# ----------------------------------------------------
# ส่วนโปรโมชั่น & สรุปยอดชำระเงิน
# ----------------------------------------------------
col_promo, col_summary = st.columns([2, 1.5])

with col_promo:
    st.subheader("โปรโมชั่น & ส่วนลดพิเศษ")
    with st.container(border=True):
        # โปรโมชั่น 1
        p1_class = "promo-box-active" if promo1_active else "promo-box-inactive"
        p1_icon = "✅" if promo1_active else "⬜"
        st.markdown(f"<div class='{p1_class}'>{p1_icon} ซื้อครบ 99 บาท จัดส่งฟรี</div>", unsafe_allow_html=True)
        
        # โปรโมชั่น 2
        p2_class = "promo-box-active" if promo2_active else "promo-box-inactive"
        p2_icon = "✅" if promo2_active else "⬜"
        st.markdown(f"<div class='{p2_class}'>{p2_icon} เก็บสะสมแต้ม/ซื้อครบ 6 ชิ้น รับ สกุชชี่ชีส เพิ่ม 1 ชิ้น ฟรี!!</div>", unsafe_allow_html=True)
        
        # โปรโมชั่น 3
        p3_class = "promo-box-active" if promo3_active else "promo-box-inactive"
        p3_icon = "✅" if promo3_active else "⬜"
        st.markdown(f"<div class='{p3_class}'>{p3_icon} ซื้อสกุชชี่ ราคา 20/30 บาท ครบ 3 ชิ้น รับส่วนลด 10 บาท!!</div>", unsafe_allow_html=True)

with col_summary:
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center;'>สรุปยอดชำระเงิน</h4>", unsafe_allow_html=True)
        st.write("---")
        st.write(f"**ราคารวมสินค้า:** {total_price} บาท")
        st.write(f"**ค่าส่ง:** {shipping_cost} บาท")
        st.write(f"**ส่วนลดโปรโมชั่น:** -{discount} บาท")
        
        st.markdown(f"""
            <div class='total-box'>
                ⭐ ยอดสุทธิที่ต้องจ่าย: [ {final_total} บาท ]
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("ยืนยันการสั่งซื้อ (ชำระเงิน)", type="primary", use_container_width=True):
            if total_items > 0:
                st.success("ทำรายการสำเร็จ!")
            else:
                st.warning("กรุณาเลือกสินค้าอย่างน้อย 1 ชิ้น")
