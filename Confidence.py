import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

st.set_page_config(page_title="Confidence Interval Calculator",layout='wide')
hide_style ="""
<style>
      #MainMenu {visibility:hidden}
      footer {visibility:hidden}
      header {visibility:hidden}


"""
st.markdown(hide_style,unsafe_allow_html=True)
st.title("Confidence Interval Calculator for Z Procedure")

st.write('''Máy tính khoảng tin cậy cho thủ tục Z. Ứng dụng này tính toán khoảng tin cậy cho trung bình tổng thể bằng cách sử dụng quy trình Z và hiển thị biểu đồ về khoảng đó.''')

with st.sidebar:
    st.header("Thông số đầu vào")
    conf_level = st.slider("Mức độ tin cậy(%)",0,100,95,1)
    sample_mean = st.number_input("Trung bình mẫu",value=0.0)
    pop_std_dev = st.number_input("Độ lệch chuẩn tổng thể",value=1.0)
    sample_size = st.number_input("Cỡ mẫu",value=30,min_value=1,step=1)


#Calculate the critical value and margin of error
z_score = stats.norm.ppf(1-(1-conf_level/100)/2)
margin_of_error = z_score*(pop_std_dev/np.sqrt(sample_size))

#Calculate the confidence interval
lower_limit = sample_mean - margin_of_error
upper_limit = sample_mean + margin_of_error

#DIsplay the result
st.write(f"Giá trị giới hạn (z-score):{z_score:.2f}")
st.write(f"Biên độ lỗi:{margin_of_error:.2f}")
st.write(f"Khoảng tin cậy:({lower_limit:.2f},{upper_limit:.2f})")

#Plot the confidence interval
fig,ax=plt.subplots(figsize=(3,2))

ax.bar(['Lower Limit',"Upper Limit"],[lower_limit,upper_limit],color='lightblue')
ax.plot(['Lower Limit',"Upper Limit"],[lower_limit,upper_limit],color='red',linewidth=2)
ax.axhline(sample_mean,color='green',linestyle='--',label="Sample Mean")

ax.set_ylabel("Value")
ax.set_title("Confidence Interval")
ax.legend()

st.pyplot(fig)