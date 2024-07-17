import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px

# Load data from files
dictt = joblib.load("dict.pkl")
dict1 = joblib.load("dict1.pkl")
arr = joblib.load("arr.pkl")

df_impayes = pd.read_csv("df_impayes.csv")

# Set the configuration for the Streamlit page
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Load custom CSS for styling
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Display the logo in the sidebar
st.sidebar.image('logo_ciment.jfif')

# Sidebar options
st.sidebar.subheader('Select Client')
client_name = st.sidebar.selectbox('Client Name', arr)

st.sidebar.subheader('Bar chart parameters')
plot_data = st.sidebar.multiselect('Select data features', ['CA_Annuel_2022', 'CA_Annuel_2023'], ['CA_Annuel_2022', 'CA_Annuel_2023'])

# Display client details
col11, col12, col13 = st.columns(3)
col12.markdown('## Client Details')

col1, col2, col3 = st.columns((4, 3, 3))
col1.metric("Client Name", client_name)
col2.metric("Client Code", dictt[client_name]["client_code"])
col3.metric("Score", dictt[client_name]["rf_pred_numeric"])

# Load combined data
df_combined = pd.read_csv("df_combined.csv")

# Sidebar slider for plot height
plot_height = st.sidebar.slider('Specify plot height', 500, 750, 500)

# Plotting columns
c1, c2 = st.columns((5, 5))

with c1:
    # Create a DataFrame for the selected client
    data = {
        'CA_Annuel_2022': [df_combined[df_combined["Client_2023"] == client_name]["CA_Annuel_2022"].values[0]],
        'CA_Annuel_2023': [df_combined[df_combined["Client_2023"] == client_name]["CA_Annuel_2023"].values[0]]
    }

    df_combined1 = pd.DataFrame(data)

    # Extract the values for the bar plot
    value_1 = df_combined1['CA_Annuel_2022'].iloc[0]
    value_2 = df_combined1['CA_Annuel_2023'].iloc[0]

    # Create a bar plot using Plotly
    categories = plot_data
    values = [value_1, value_2]

    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=['blue', 'green']
    )])

    # Customize the plot
    fig.update_layout(
        title='Bar Plot of CA_Annuel_2022 and CA_Annuel_2023',
        xaxis_title='Category',
        yaxis_title='Value',
        width=plot_height
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

with c2:
    # Example data for another bar plot
    counts = [171, 9, 69, 48, 17]
    scores = ['Score 1', 'Score 2', 'Score 3', 'Score 4', 'Score 5']
    categories = scores
    values = counts

    # Create another bar plot using Plotly
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=['blue', 'green', 'red', 'orange', 'purple']
    )])

    # Customize the plot
    fig.update_layout(
        title='Bar Plot Scores',
        xaxis_title='Category',
        yaxis_title='Value',
        width=plot_height
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)


col1, col2, col3 = st.columns([1,5,4])
# Load impayes data
with col2:
    counts = [590, 322, 105]

    # Create a DataFrame for the pie chart
    data = {
        "Activité": ["BPE", "Ciments", "Granulats"],
        "Counts": counts
    }

    dat = df_impayes[df_impayes["Code"] == dictt[client_name]["client_code"]]["Activité"].value_counts()

    # Adjust counts based on client data
    if "Granulats" in dat.index:
        counts[2] += dat["Granulats"]
    elif "BPE" in dat.index:
        counts[0] += dat["BPE"]
    elif "Ciments" in dat.index:
        counts[1] += dat["Ciments"]

    # Create a DataFrame for the pie chart
    df_impayes = pd.DataFrame(data)

    # Create the pie chart using Plotly with enhanced styling
    fig = px.pie(df_impayes, 
                names='Activité', 
                values='Counts', 
                title='Activité Distribution',
                color_discrete_sequence=px.colors.sequential.RdBu)

    # Update the layout for better aesthetics
    fig.update_layout(
        title_text='Activité Distribution',
        title_x=0.5,
        title_font_size=24,
        legend_title_text='Activité',
        legend_title_font_size=16,
        legend_font_size=14,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # Update the trace for hover info and other settings
    fig.update_traces(
        textinfo='percent+label', 
        textfont_size=14,
        hoverinfo='label+percent+value', 
        marker=dict(line=dict(color='#000000', width=2))
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)
