import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import io

# Load diabetes_model.pkl file
diabetes_model = pickle.load(open('diabetes_model.pkl', 'rb'))

# Initialize session state for diabetic status
if 'diabetic' not in st.session_state:
    st.session_state['diabetic'] = False
    st.session_state['features'] = None  # To store the input features
    st.session_state['feature_importance'] = None  # To store the importance of features

# Function to save plot as image
def save_plot_as_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Diabetes Prediction System',
                          ['Diabetes Prediction', 'Graphs/Charts'],
                          icons=['activity', 'bar-chart'],
                          default_index=0)

# Function to set title with color
def colored_title(title, color):
    st.markdown(f"<h1 style='color:{color};'>{title}</h1>", unsafe_allow_html=True)

# Graphs/Charts Page
if selected == 'Graphs/Charts':
    
    # Page title with color
    colored_title('Diabetes Predictions Charts/Graphs', '#007bff')  # Adjust color as needed
    
    # Check if the user has a diagnosis
    if st.session_state['features']:
        features = st.session_state['features']
        feature_names = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Diabetes Pedigree Function', 'Age']
        feature_importance = st.session_state['feature_importance']

        # Sort features by their importance (in this case, just their values)
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        sorted_feature_names, sorted_feature_values = zip(*sorted_features)

        # Create two columns for the charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart for all features
            fig, ax = plt.subplots(figsize=(10, 6))
            color = 'red' if st.session_state['diabetic'] else 'green'
            ax.barh(sorted_feature_names, sorted_feature_values, color=color)
            ax.set_title('Feature Values' if st.session_state['diabetic'] else 'Feature Values for Non-Diabetic Case')
            ax.set_xlabel('Value')
            ax.set_ylabel('Feature')
            st.pyplot(fig)  # Display the chart
            
            # Save bar chart as image
            bar_chart_image = save_plot_as_image(fig)
            st.download_button(label='Download Bar Chart', data=bar_chart_image, file_name='bar_chart.png', mime='image/png')

        with col2:
            # Pie chart for feature distribution
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(sorted_feature_values, labels=sorted_feature_names, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
            ax.set_title('Feature Distribution' if st.session_state['diabetic'] else 'Feature Distribution for Non-Diabetic Case')
            st.pyplot(fig)  # Display the pie chart
            
            # Save pie chart as image
            pie_chart_image = save_plot_as_image(fig)
            st.download_button(label='Download Pie Chart', data=pie_chart_image, file_name='pie_chart.png', mime='image/png')

        # Display detailed feature values below the charts
        st.write("### Detailed Feature Values:")
        for name, value in zip(sorted_feature_names, sorted_feature_values):
            st.write(f"- {name}: {value:.2f}")

        # Social media sharing with icons
        st.markdown("""
            ### Share your results!
            <a href="https://twitter.com/intent/tweet?text=Check%20out%20my%20diabetes%20prediction%20results%20with%20Streamlit%20app!%20%23DiabetesPrediction%20%23Streamlit" target="_blank">
            <img src="https://img.icons8.com/ios-filled/50/000000/twitter.png" alt="Twitter" style="vertical-align:middle; width: 30px; height: 30px;"/></a>
            <a href="https://www.facebook.com/sharer/sharer.php?u=your_app_url" target="_blank">
            <img src="https://img.icons8.com/ios-filled/50/000000/facebook.png" alt="Facebook" style="vertical-align:middle; width: 30px; height: 30px;"/></a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=your_app_url" target="_blank">
            <img src="https://img.icons8.com/ios-filled/50/000000/linkedin.png" alt="LinkedIn" style="vertical-align:middle; width: 30px; height: 30px;"/></a>
            <a href="https://wa.me/?text=Check%20out%20my%20diabetes%20prediction%20results%20with%20Streamlit%20app!%20%23DiabetesPrediction%20%23Streamlit" target="_blank">
            <img src="https://img.icons8.com/ios-filled/50/000000/whatsapp.png" alt="WhatsApp" style="vertical-align:middle; width: 30px; height: 30px;"/></a>
            """, unsafe_allow_html=True)
