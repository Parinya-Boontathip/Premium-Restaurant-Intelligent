# -*- coding: utf-8 -*-
"""Restuarant intelligent MVP2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iuyAZLcbQpkZRzF5XbwS7dHV40X2sW-p
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Set page config
st.set_page_config(page_title="Restaurant Ordering System", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .meal-button {
        padding: 10px 20px;
        margin: 5px;
        border-radius: 5px;
    }
    .meal-button-active {
        background-color: #4CAF50;
        color: white;
    }
    .menu-item {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin: 5px 0;
    }
    .header {
        text-align: center;
        padding: 10px;
        background-color: #f8f9fa;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sample data - Customer database
@st.cache_data
def load_customer_data():
    return {
        "C001": {"name": "สมชาย", "surname": "รักดี", "tel": "0811234567",
                "history": ["ข้าวผัดกระเพราหมู", "ต้มยำกุ้ง", "ผัดไทย"],
                "allergies": "กุ้ง"},
        "C002": {"name": "วันดี", "surname": "มีสุข", "tel": "0822345678",
                "history": ["ส้มตำไทย", "ข้าวมันไก่", "แกงเขียวหวานไก่"],
                "allergies": "ถั่ว"},
        "C003": {"name": "นภา", "surname": "ใจดี", "tel": "0833456789",
                "history": ["ข้าวผัดกระเพรากุ้ง", "ต้มข่าไก่", "ปลาทอดน้ำปลา"],
                "allergies": ""},
        "C004": {"name": "ประพันธ์", "surname": "รักษา", "tel": "0844567890",
                "history": ["ยำวุ้นเส้น", "ผัดซีอิ๊วหมู", "ข้าวผัดปู"],
                "allergies": "หอย"},
        "C005": {"name": "กมลา", "surname": "ศรีวิไล", "tel": "0855678901",
                "history": ["ข้าวเหนียวมะม่วง", "ไก่ทอด", "ส้มตำปูปลาร้า"],
                "allergies": "นม"}
    }

# Sample menu data
@st.cache_data
def load_menu_data():
    return {
        "อาหารหลัก": [
            {"name": "ข้าวผัดกระเพราหมู", "price": 80, "image": "https://i.ibb.co/WDGV6p1/pad-krapow.jpg"},
            {"name": "ข้าวมันไก่", "price": 85, "image": "https://i.ibb.co/MnLzh1j/khao-man-kai.jpg"},
            {"name": "ผัดไทย", "price": 90, "image": "https://i.ibb.co/F4RcGxF/pad-thai.jpg"},
            {"name": "ต้มยำกุ้ง", "price": 120, "image": "https://i.ibb.co/DCQpZpJ/tom-yum-kung.jpg"},
            {"name": "แกงเขียวหวานไก่", "price": 95, "image": "https://i.ibb.co/6RJbQ5Y/green-curry.jpg"},
            {"name": "ผัดซีอิ๊วหมู", "price": 80, "image": "https://i.ibb.co/KL2YZmB/pad-see-ew.jpg"}
        ],
        "ของหวาน": [
            {"name": "ข้าวเหนียวมะม่วง", "price": 75, "image": "https://i.ibb.co/1n58JTZ/mango-sticky-rice.jpg"},
            {"name": "บัวลอย", "price": 60, "image": "https://i.ibb.co/LrBMkGH/bua-loy.jpg"},
            {"name": "ทับทิมกรอบ", "price": 65, "image": "https://i.ibb.co/3FsSzPy/thapthim-krop.jpg"}
        ],
        "เครื่องดื่ม": [
            {"name": "น้ำส้ม", "price": 40, "image": "https://i.ibb.co/Rb5PLpV/orange-juice.jpg"},
            {"name": "ชาเย็น", "price": 35, "image": "https://i.ibb.co/TRJFWfK/thai-tea.jpg"},
            {"name": "กาแฟ", "price": 45, "image": "https://i.ibb.co/kMMvDPd/coffee.jpg"}
        ]
    }

# Load the sample data
customer_data = load_customer_data()
menu_data = load_menu_data()

# App title
st.markdown("<div class='header'><h1>ระบบสั่งอาหารร้านอาหารไทย</h1></div>", unsafe_allow_html=True)

# Initialize session state if not already done
if 'customer' not in st.session_state:
    st.session_state.customer = None
if 'meal_type' not in st.session_state:
    st.session_state.meal_type = None
if 'people_count' not in st.session_state:
    st.session_state.people_count = 1
if 'children_count' not in st.session_state:
    st.session_state.children_count = 0
if 'elderly_count' not in st.session_state:
    st.session_state.elderly_count = 0
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'order_sent' not in st.session_state:
    st.session_state.order_sent = False

# Customer identification section
st.sidebar.header("ค้นหาข้อมูลลูกค้า")

# Create two columns for input fields
col1, col2 = st.sidebar.columns(2)

with col1:
    # Dropdown for customer ID
    customer_ids = list(customer_data.keys())
    selected_id = st.selectbox("รหัสลูกค้า", [""] + customer_ids)

with col2:
    tel_number = st.text_input("เบอร์โทรศัพท์")

# Enter button
if st.sidebar.button("ค้นหา"):
    # Check if customer ID is selected
    if selected_id:
        st.session_state.customer = customer_data[selected_id]
        st.session_state.customer_id = selected_id
    # Or check if telephone number matches any customer
    elif tel_number:
        found = False
        for cid, cdata in customer_data.items():
            if cdata["tel"] == tel_number:
                st.session_state.customer = cdata
                st.session_state.customer_id = cid
                found = True
                break
        if not found:
            st.sidebar.error("ไม่พบข้อมูลลูกค้า")
    else:
        st.sidebar.warning("กรุณาระบุรหัสลูกค้าหรือเบอร์โทรศัพท์")

# Clear button
if st.sidebar.button("ล้างข้อมูล"):
    st.session_state.customer = None
    st.session_state.meal_type = None
    st.session_state.cart = {}
    st.session_state.order_sent = False

# Reset cart button
if st.sidebar.button("ล้างตะกร้า"):
    st.session_state.cart = {}
    st.session_state.order_sent = False

# Display customer info if available
if st.session_state.customer:
    st.sidebar.header("ข้อมูลลูกค้า")
    st.sidebar.write(f"ชื่อ: {st.session_state.customer['name']} {st.session_state.customer['surname']}")
    st.sidebar.write(f"เบอร์โทร: {st.session_state.customer['tel']}")

    if st.session_state.customer['allergies']:
        st.sidebar.warning(f"แพ้อาหาร: {st.session_state.customer['allergies']}")

    # Date and time of reservation
    st.sidebar.header("วันเวลาที่จอง")
    st.sidebar.write(datetime.now().strftime("%Y-%m-%d %H:%M"))

    # Meal type selection
    st.sidebar.header("ประเภทมื้อ")
    meal_col1, meal_col2, meal_col3 = st.sidebar.columns(3)

    with meal_col1:
        breakfast_class = "meal-button meal-button-active" if st.session_state.meal_type == "อาหารเช้า" else "meal-button"
        if st.button("อาหารเช้า", key="breakfast"):
            st.session_state.meal_type = "อาหารเช้า"

    with meal_col2:
        lunch_class = "meal-button meal-button-active" if st.session_state.meal_type == "อาหารกลางวัน" else "meal-button"
        if st.button("อาหารกลางวัน", key="lunch"):
            st.session_state.meal_type = "อาหารกลางวัน"

    with meal_col3:
        dinner_class = "meal-button meal-button-active" if st.session_state.meal_type == "อาหารเย็น" else "meal-button"
        if st.button("อาหารเย็น", key="dinner"):
            st.session_state.meal_type = "อาหารเย็น"

    # Table details
    st.sidebar.header("รายละเอียดโต๊ะ")

    # People count
    p_col1, p_col2, p_col3 = st.sidebar.columns(3)
    with p_col1:
        st.write("จำนวนคนทั้งหมด")
    with p_col2:
        if st.button("-", key="dec_people"):
            st.session_state.people_count = max(1, st.session_state.people_count - 1)
    with p_col3:
        if st.button("+", key="inc_people"):
            st.session_state.people_count += 1
    st.sidebar.write(f"จำนวนคน: {st.session_state.people_count}")

    # Children count
    c_col1, c_col2, c_col3 = st.sidebar.columns(3)
    with c_col1:
        st.write("จำนวนเด็ก")
    with c_col2:
        if st.button("-", key="dec_children"):
            st.session_state.children_count = max(0, st.session_state.children_count - 1)
    with c_col3:
        if st.button("+", key="inc_children"):
            st.session_state.children_count += 1
    st.sidebar.write(f"จำนวนเด็ก: {st.session_state.children_count}")

    # Elderly count
    e_col1, e_col2, e_col3 = st.sidebar.columns(3)
    with e_col1:
        st.write("จำนวนผู้สูงอายุ")
    with e_col2:
        if st.button("-", key="dec_elderly"):
            st.session_state.elderly_count = max(0, st.session_state.elderly_count - 1)
    with e_col3:
        if st.button("+", key="inc_elderly"):
            st.session_state.elderly_count += 1
    st.sidebar.write(f"จำนวนผู้สูงอายุ: {st.session_state.elderly_count}")

    # Display shopping cart
    st.sidebar.header("ตะกร้าสินค้า")
    total_price = 0
    if st.session_state.cart:
        for item, quantity in st.session_state.cart.items():
            # Find the price from menu data
            price = 0
            for category in menu_data.values():
                for dish in category:
                    if dish["name"] == item:
                        price = dish["price"]
                        break

            st.sidebar.write(f"{item} x {quantity} = ฿{price * quantity}")
            total_price += price * quantity

        st.sidebar.write(f"**รวมทั้งสิ้น: ฿{total_price}**")

        # Send order button
        if st.sidebar.button("ส่งออเดอร์ไปยังครัว"):
            st.session_state.order_sent = True
    else:
        st.sidebar.write("ยังไม่มีรายการอาหารที่สั่ง")

    # Order confirmation message
    if st.session_state.order_sent:
        st.sidebar.success("ส่งออเดอร์ไปยังครัวเรียบร้อยแล้ว!")

    # Main content - Only show if customer is selected
    # Favorite dishes section
    st.header("เมนูที่สั่งบ่อย")
    fav_cols = st.columns(3)

    for i, dish_name in enumerate(st.session_state.customer["history"]):
        with fav_cols[i % 3]:
            # Find dish details
            dish_details = None
            for category in menu_data.values():
                for dish in category:
                    if dish["name"] == dish_name:
                        dish_details = dish
                        break
                if dish_details:
                    break

            if dish_details:
                st.markdown(f"""
                <div class="menu-item">
                    <h3>{dish_details['name']}</h3>
                    <p>฿{dish_details['price']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Number input for quantity
                quantity = st.number_input(f"จำนวน {dish_name}",
                                          min_value=0,
                                          value=st.session_state.cart.get(dish_name, 0),
                                          step=1,
                                          key=f"fav_qty_{dish_name}")

                # Add to cart button
                if st.button("เพิ่มลงตะกร้า", key=f"fav_{dish_name}"):
                    if quantity > 0:
                        st.session_state.cart[dish_name] = quantity
                    elif dish_name in st.session_state.cart:
                        del st.session_state.cart[dish_name]
                    st.session_state.order_sent = False
                    st.experimental_rerun()

    # Recommended dishes (randomly selected)
    st.header("เมนูแนะนำ")
    rec_cols = st.columns(3)

    # Get all dishes excluding favorites
    all_dishes = []
    for category, dishes in menu_data.items():
        for dish in dishes:
            if dish["name"] not in st.session_state.customer["history"]:
                all_dishes.append(dish)

    # Select random dishes to recommend
    if all_dishes:
        recommended = random.sample(all_dishes, min(3, len(all_dishes)))

        for i, dish in enumerate(recommended):
            with rec_cols[i % 3]:
                st.markdown(f"""
                <div class="menu-item">
                    <h3>{dish['name']}</h3>
                    <p>฿{dish['price']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Number input for quantity
                quantity = st.number_input(f"จำนวน {dish['name']}",
                                          min_value=0,
                                          value=st.session_state.cart.get(dish['name'], 0),
                                          step=1,
                                          key=f"rec_qty_{dish['name']}")

                # Add to cart button
                if st.button("เพิ่มลงตะกร้า", key=f"rec_{dish['name']}"):
                    if quantity > 0:
                        st.session_state.cart[dish['name']] = quantity
                    elif dish['name'] in st.session_state.cart:
                        del st.session_state.cart[dish['name']]
                    st.session_state.order_sent = False
                    st.experimental_rerun()

    # Allergy information input
    st.header("ข้อมูลการแพ้อาหาร")
    allergy_info = st.text_area("โปรดระบุการแพ้อาหารหรือข้อจำกัดในการรับประทานอาหาร",
                              value=st.session_state.customer["allergies"])

    if st.button("บันทึกข้อมูลการแพ้อาหาร"):
        # In a real app, this would update the database
        st.success("บันทึกข้อมูลการแพ้อาหารเรียบร้อยแล้ว")

    # Main menu section
    st.header("เมนูอาหาร")

    # Create tabs for different menu categories
    tabs = st.tabs(list(menu_data.keys()))

    # Fill each tab with menu items
    for i, (category, dishes) in enumerate(menu_data.items()):
        with tabs[i]:
            # Create 3 columns for menu items
            for j in range(0, len(dishes), 3):
                menu_cols = st.columns(3)
                for k in range(3):
                    idx = j + k
                    if idx < len(dishes):
                        dish = dishes[idx]
                        with menu_cols[k]:
                            st.image(dish["image"], width=150)
                            st.subheader(dish["name"])
                            st.write(f"ราคา: ฿{dish['price']}")

                            # Number input for quantity - directly input numbers
                            quantity = st.number_input(f"จำนวน",
                                                     min_value=0,
                                                     value=st.session_state.cart.get(dish['name'], 0),
                                                     step=1,
                                                     key=f"menu_qty_{category}_{dish['name']}")

                            # Add to cart button - updates based on the number input
                            if st.button("อัพเดทตะกร้า", key=f"upd_{category}_{dish['name']}"):
                                if quantity > 0:
                                    st.session_state.cart[dish['name']] = quantity
                                elif dish['name'] in st.session_state.cart:
                                    del st.session_state.cart[dish['name']]
                                st.session_state.order_sent = False
                                st.experimental_rerun()
else:
    st.info("กรุณาระบุรหัสลูกค้าหรือเบอร์โทรศัพท์เพื่อเริ่มการสั่งอาหาร")