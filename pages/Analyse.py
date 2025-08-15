import streamlit as st
import base64
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np

def img_to_bytes(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = img_to_bytes("Images/full5.jpg")   # Main app background
simg = img_to_bytes("Images/side.jpg")   # Sidebar background

custom_css = f"""
<style>
/* Main app background */
.stApp {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
    background-attachment: fixed;
}}

/* Sidebar background */
section[data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{simg}");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center center;
    background-attachment: scroll;
    min-height: 100vh;
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
st.set_page_config(layout="centered",page_title="Analyse",page_icon="💤")
st.title("See What Affects your Sleep")
show = st.checkbox("Show Graph", value=True)


# cleaning data
df1 = pd.read_csv("pages/Sleep_health_and_lifestyle_dataset.csv") #paths are relative to main directory only so need to mention pages
df2 = pd.read_csv("pages/student_habits_performance.csv")
df3 = pd.read_csv("pages/student_sleep_patterns.csv")

df1.replace("Normal Weight","Normal",inplace=True)

df1.drop("Person ID",axis=1,inplace=True)
df2.drop("student_id",axis=1,inplace=True)
df3.drop("Student_ID",axis=1,inplace=True)


def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

load_lottieurl1=load_lottieurl("https://lottie.host/7f779a67-5d6e-498d-bac5-7e18784f60f0/Cx52XuHV7L.json")

load_lottieurl2=load_lottieurl("https://lottie.host/22afb872-a230-465b-a0bc-0b60301dbc1e/vfYETY5zTh.json")

def constructSingle(chart_type, x, hue):
    if show:
        if chart_type == "Histogram":
            fig = px.histogram(data, x=x, color=hue)
            st.plotly_chart(fig)
            # sns.histplot(data=data, x=x, hue=hue)
            # st.pyplot(plt.gcf())  # plt.gcf() = get current figure

        elif chart_type == "Count Plot":
            if hue is None or hue==x:
                count_data = data[x].value_counts().reset_index()
                count_data.columns = [x, 'count']
                fig = px.bar(count_data, x=x, y='count', color=x)
            else:
                count_data = data.groupby([x, hue]).size().reset_index(name='count')
                fig = px.bar(count_data, x=x, y='count', color=hue, barmode='group')
            st.plotly_chart(fig)
        else:
            fig = px.pie(data, names=x_col, color=hue)
            st.plotly_chart(fig)

# DOUBLE AXIS CHARTS
def constructDouble(chart_type, x, y, hue):
    if show:
        if chart_type == "Bar Chart":
            if hue and hue!=x:
                grouped_data = data.groupby([x, hue], as_index=False)[y].mean()
            else:
                grouped_data = data.groupby(x, as_index=False)[y].mean()

            fig = px.bar(grouped_data, x=x, y=y, color=hue)
            st.plotly_chart(fig)

        elif chart_type == "Box Plot":
            fig = px.box(data, x=x, y=y, color=hue)
            st.plotly_chart(fig)

        elif chart_type == "Violin Plot":
            fig = px.violin(data, x=x, y=y, color=hue, box=True, points="all")
            st.plotly_chart(fig)

        elif chart_type == "Cat Plot":
            fig = px.strip(data, x=x, y=y, color=hue)
            st.plotly_chart(fig)

        elif chart_type == "Scatter Plot":
            fig = px.scatter(data, x=x, y=y, color=hue)
            st.plotly_chart(fig)

        elif chart_type == "Line Plot":
            sns.lineplot(data, x=x, y=y, hue=hue)
            st.pyplot(plt.gcf())

# MULTI AXIS CHARTS
def constructHeatmap(cols):
    if show:
        if len(cols) >= 2:
            corr = data[cols].corr().values

            # Format annotations to 3 decimal places
            annotations = [[f"{val:.3f}" for val in row] for row in corr]

            fig = ff.create_annotated_heatmap(
                z=corr,
                x=cols,
                y=cols,
                annotation_text=annotations,
                colorscale="Viridis",
                showscale=True
            )
            st.plotly_chart(fig)
        else:
            st.warning("Please select at least two numerical columns.")


# PAIR PLOT
def constructPairplot(data,Hue):
    if show:
        st.info("All numerical columns will be used for pair plotting.")
        sns.pairplot(data, hue=Hue)
        st.pyplot(plt.gcf())  # plt.gcf() = get current figure

data=0
with st.sidebar.title("Navigation"):
    if load_lottieurl1:
        st_lottie(load_lottieurl1)
    else:
        st.write("Error")
dataset_choice = st.sidebar.radio("Select Dataset", ("Dataset 1: Adult Lifestyle", "Dataset 2: School Student Lifestyle", "Dataset 3: College Student Lifestyle"))

if dataset_choice == "Dataset 1: Adult Lifestyle":
    entries  = st.sidebar.slider("Number of entries from top: ", min_value=0, max_value=len(df1), value=100)
    data = df1.head(entries)
    df_label = "df1"
    
elif dataset_choice == "Dataset 2: School Student Lifestyle":
    entries  = st.sidebar.slider("Number of entries from top: ", min_value=0, max_value=len(df2), value=100)
    data = df2.head(entries)
    df_label = "df2"
else:
    entries  = st.sidebar.slider("Number of entries from top: ", min_value=0, max_value=len(df3), value=100)
    data = df3.head(entries)
    df_label = "df3"
    
if data.empty==False:
    cat_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    num_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # Include numeric columns with < 10 unique values as categorical
    low_cardinality_cols = [col for col in num_cols if data[col].nunique() <= 10]

    # Add them to cat_cols (if not already there)
    cat_cols += [col for col in low_cardinality_cols if col not in cat_cols]

    chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart", "Histogram", "Box Plot", "Count Plot","Line Plot","Scatter Plot","Cat Plot","Violin Plot","Heat Map","Pair Plot"])

    single_axis_charts = ["Count Plot", "Pie Chart", "Histogram"]
    double_axis_charts = ["Bar Chart", "Box Plot", "Line Plot", "Scatter Plot", "Cat Plot", "Violin Plot"]
    no_axis_charts = ["Pair Plot"]
    multi_axis_charts = ["Heat Map"]

    hue = st.sidebar.selectbox("Select Hue",cat_cols+[None])

    if chart_type in single_axis_charts:
        if chart_type == "Histogram":
            x_col = st.sidebar.selectbox("Select a numerical column", num_cols)
            constructSingle(chart_type,x_col,hue)

        else:
            x_col = st.sidebar.selectbox("Select a categorical column", cat_cols)
            constructSingle(chart_type,x_col,hue)

    elif chart_type in double_axis_charts:
        if chart_type in ["Bar Chart"]:
            x_col = st.sidebar.selectbox("Select X (categorical)", cat_cols)
            y_col = st.sidebar.selectbox("Select Y (numerical)", num_cols)
            constructDouble(chart_type, x_col, y_col, hue)

        elif chart_type in ["Box Plot", "Violin Plot", "Cat Plot"]:
            x_col = st.sidebar.selectbox("Select X (categorical)", cat_cols)
            y_col = st.sidebar.selectbox("Select Y (numerical)", num_cols)
            constructDouble(chart_type, x_col, y_col, hue)

        elif chart_type in ["Scatter Plot","Line Plot"]:
            x_col = st.sidebar.selectbox("Select X (numerical)", num_cols)
            y_col = st.sidebar.selectbox("Select Y (numerical)", num_cols)
            constructDouble(chart_type, x_col, y_col, hue)



    elif chart_type in multi_axis_charts:
        heat_cols = st.sidebar.multiselect("Select numerical columns", num_cols)
        constructHeatmap(heat_cols)

    elif chart_type == "Pair Plot":
        constructPairplot(data,hue)

# with st.sidebar:
#     if load_lottieurl2:
#         st_lottie(load_lottieurl2)
#     else:
#         st.write("Error")
import streamlit.components.v1 as components
with st.sidebar:
    components.html(f"""
        <div style="background: none; width: 100%;">
            <lottie-player src="https://lottie.host/22afb872-a230-465b-a0bc-0b60301dbc1e/vfYETY5zTh.json" 
                           background="transparent" 
                           speed="1" 
                           style="width: 100%; height: 200px;" 
                           loop autoplay>
            </lottie-player>
        </div>
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    """, height=220)



    


if st.checkbox("📄 Show Raw Data"):
    st.dataframe(data)
    