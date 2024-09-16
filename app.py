import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Load diabetes_model.pkl file
diabetes_model = pickle.load(open('diabetes_model.pkl', 'rb'))

# Initialize session state for diabetic status
if 'diabetic' not in st.session_state:
    st.session_state['diabetic'] = False
    st.session_state['features'] = None  # To store the input features

# Function to save plot as image
def save_plot_as_image(fig, filename='plot.png'):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Diabetes Prediction System',
                          ['Diabetes Prediction', 'Graphs/Charts'],
                          icons=['activity', 'bar-chart'],
                          default_index=0)

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    
    # Page title
    st.title('Predicting Diabetes Onset using ML')
    
    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Pregnancies = st.text_input('Number of Pregnancies', help="Enter the number of times the patient has been pregnant.")
        
    with col2:
        Glucose = st.text_input('Glucose Level', help="Enter the plasma glucose concentration measured two hours after an oral glucose tolerance test.")
    
    with col3:
        BloodPressure = st.text_input('Blood Pressure value', help="Enter the diastolic blood pressure value in mm Hg. This is the blood pressure when the heart is resting between beats.")
    
    with col1:
        SkinThickness = st.text_input('Skin Thickness value', help="Enter the thickness of the triceps skin fold in mm. This value helps in estimating body fat.")
    
    with col2:
        Insulin = st.text_input('Insulin Level', help="Enter the 2-hour serum insulin level in mu U/ml. This helps in assessing insulin production and resistance.")
    
    with col3:
        BMI = st.text_input('BMI value', help="Enter the Body Mass Index (BMI) value, calculated as weight in kg divided by the square of height in meters. It indicates body fat and health risk.")
    
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value', help="Enter the diabetes pedigree function value, a measure of the genetic risk of diabetes based on family history.")
    
    with col2:
        Age = st.text_input('Age of the Person', help="Enter the age of the patient in years. This value should be a whole number.")
    
    # Code for prediction
    diab_diagnosis = ''

    # Creating a button for Prediction
    if st.button('Diabetes Test Result'):
        with st.spinner('Predicting...'):
            # Check if all fields are filled
            if Pregnancies == '' or Glucose == '' or BloodPressure == '' or SkinThickness == '' or Insulin == '' or BMI == '' or DiabetesPedigreeFunction == '' or Age == '':
                st.warning('Please fill in all the input fields to get an accurate prediction.')
            else:
                # Convert inputs to float
                features = [float(Pregnancies), float(Glucose), float(BloodPressure), float(SkinThickness), float(Insulin), float(BMI), float(DiabetesPedigreeFunction), float(Age)]
                
                # Perform prediction
                diab_prediction = diabetes_model.predict([features])

                if diab_prediction[0] == 1:
                    diab_diagnosis = 'The person is diabetic'
                    st.session_state['diabetic'] = True  # Store the result in session state
                else:
                    diab_diagnosis = 'The person is not diabetic'
                    st.session_state['diabetic'] = False  # Store the result in session state

                # Store the features in session state for use on the Graphs/Charts page
                st.session_state['features'] = features

    # Display the diagnosis
    st.write(diab_diagnosis)
    st.info('Please fill in all the input fields with the appropriate values to get an accurate prediction.', icon="ℹ️")

    # Button to navigate to the Graphs/Charts page
    st.markdown("[Go to Graphs/Charts Page](?selected=Graphs/Charts)")

# Diabetes Charts or Graphs Page
if selected == 'Graphs/Charts':
    
    # Page title
    st.title('Diabetes Predictions Charts/Graphs')
    
    # Check if the user is diagnosed as diabetic
    if 'diabetic' in st.session_state and st.session_state['diabetic']:
        st.write("The person is diabetic. Here are the detailed charts and graphs showing factors contributing to diabetes.")
        
        # Check if features are available
        if st.session_state['features']:
            features = st.session_state['features']
            feature_names = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Diabetes Pedigree Function', 'Age']
            
            # Bar chart for diabetic factors
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(feature_names, features, color='red')
            ax.set_title('Factors Contributing to Diabetes Diagnosis')
            ax.set_xlabel('Value')
            ax.set_ylabel('Feature')
            st.pyplot(fig)  # Display the chart
            
            # Save bar chart as image
            bar_chart_image = save_plot_as_image(fig)
            st.download_button(label='Download Bar Chart', data=bar_chart_image, file_name='bar_chart.png', mime='image/png')

            # Pie chart for feature distribution
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(features, labels=feature_names, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
            ax.set_title('Feature Distribution for Diabetic Case')
            st.pyplot(fig)  # Display the pie chart
            
            # Save pie chart as image
            pie_chart_image = save_plot_as_image(fig)
            st.download_button(label='Download Pie Chart', data=pie_chart_image, file_name='pie_chart.png', mime='image/png')
            
    else:
        st.write("Great news! Based on the provided data, the individual is not diabetic. Here’s a look at some of the healthy feature metrics.")
        
        # Check if features are available
        if st.session_state['features']:
            features = st.session_state['features']
            feature_names = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Diabetes Pedigree Function', 'Age']
            
            # Bar chart for non-diabetic factors
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(feature_names, features, color='green')
            ax.set_title('Factors for Non-Diabetic Case')
            ax.set_xlabel('Value')
            ax.set_ylabel('Feature')
            st.pyplot(fig)  # Display the chart
            
            # Save bar chart as image
            bar_chart_image = save_plot_as_image(fig)
            st.download_button(label='Download Bar Chart', data=bar_chart_image, file_name='non_diabetic_bar_chart.png', mime='image/png')
            
            # Pie chart for feature distribution
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(features, labels=feature_names, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
            ax.set_title('Feature Distribution for Non-Diabetic Case')
            st.pyplot(fig)  # Display the pie chart
            
            # Save pie chart as image
            pie_chart_image = save_plot_as_image(fig)
            st.download_button(label='Download Pie Chart', data=pie_chart_image, file_name='non_diabetic_pie_chart.png', mime='image/png')

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
