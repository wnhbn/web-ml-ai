import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


st.title("Confidence Interval Simulation: ")
hide_style ="""
<style>
      #MainMenu {visibility:hidden}
      footer {visibility:hidden}
      header {visibility:hidden}


"""
st.markdown(hide_style,unsafe_allow_html=True)
#Set parameters
sample_size = st.sidebar.slider("Cỡ mẫu",min_value=2,max_value=100,value=10)
population_mean  = st.sidebar.slider("Số bình quân tổng thể",min_value=0,max_value=100,value=50)
population_standard_deviation = st.sidebar.slider("Độ lệch chuẩn",min_value=1,max_value=100,value=15)
num_simulations = st.sidebar.slider('Số lượng mô phỏng',min_value=1,max_value=1000,value=100)
confidence_level = st.sidebar.slider("Mức độ tin cậy(%)",min_value=50,max_value=99,value=95)
method  = st.sidebar.selectbox("Method",["Z with sigma","Z with s","T with s"])

#Run Simulations
np.random.seed(42)
conf_int_capt = 0
lower_bounds=[]
upper_bounds=[]

for _ in range(num_simulations):
    sample = np.random.normal(loc=population_mean,scale=population_standard_deviation,size=sample_size)
    sample_mean = np.mean(sample)
    sample_std_dev = np.std(sample,ddof=1)

    if method =="Z with sigma":
        critical_value = stats.norm.ppf((1+confidence_level/100)/2)
        margin_of_error = critical_value*(population_standard_deviation/np.sqrt(sample_size))
    elif method =='Z with s':
        critical_value = stats.norm.ppf((1+confidence_level/100)/2)
        margin_of_error = critical_value*(sample_std_dev/np.sqrt(sample_size))
    else:
        critical_value = stats.t.ppf((1+confidence_level/100)/2,df=sample_size-1)
        margin_of_error = critical_value*(sample_std_dev/np.sqrt(sample_size))

    lower_bound = sample_mean - margin_of_error
    upper_bound = sample_mean + margin_of_error

    lower_bounds.append(lower_bound)
    upper_bounds.append(upper_bound)

    if lower_bound<=population_mean<=upper_bound:
        conf_int_capt+=1


plt.figure(figsize=(10,6))

for i in range(num_simulations):
    if lower_bounds[i] <= population_mean<=upper_bounds[i]:
        color='blue'
    else:
        color='orange'
    plt.plot([i,i],[lower_bounds[i],upper_bounds[i]],color=color)

plt.hlines(population_mean,0,num_simulations,colors='r',label='Population Mean')

plt.scatter(range(num_simulations),lower_bounds,label="Lower Bound",marker='_',s=100)
plt.scatter(range(num_simulations),upper_bounds,label="Upper Bounds",marker='_',s=100)
plt.legend()

st.pyplot(plt.gcf())

st.write(f"Captured Population Mean in {conf_int_capt} of {num_simulations} simulations ({100 * conf_int_capt / num_simulations}%)")
