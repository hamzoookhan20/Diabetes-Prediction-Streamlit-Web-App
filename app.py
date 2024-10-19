import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Load diabetes_model.pkl file
diabetes_model = pickle.load(open('diabetes_model.pkl', 'rb'))

# Initialize session state for input values and diabetic status
if 'diabetic' not in st.session_state:
    st.session_state['diabetic'] = False
    st.session_state['Pregnancies'] = ''
    st.session_state['Glucose'] = ''
    st.session_state['BloodPressure'] = ''
    st.session_state['SkinThickness'] = ''
    st.session_state['Insulin'] = ''
    st.session_state['BMI'] = ''
    st.session_state['DiabetesPedigreeFunction'] = ''
    st.session_state['Age'] = ''
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

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    
    # Page title
    st.title('Predicting Diabetes Onset using ML')
    
    # Getting the input data from the user, pre-filling with session state values
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.session_state['Pregnancies'] = st.text_input('Number of Pregnancies', value=st.session_state['Pregnancies'], help="Enter the number of times the patient has been pregnant.")
        
    with col2:
        st.session_state['Glucose'] = st.text_input('Glucose Level', value=st.session_state['Glucose'], help="Enter the plasma glucose concentration measured two hours after an oral glucose tolerance test.")
    
    with col3:
        st.session_state['BloodPressure'] = st.text_input('Blood Pressure value', value=st.session_state['BloodPressure'], help="Enter the diastolic blood pressure value in mm Hg. This is the blood pressure when the heart is resting between beats.")
    
    with col1:
        st.session_state['SkinThickness'] = st.text_input('Skin Thickness value', value=st.session_state['SkinThickness'], help="Enter the thickness of the triceps skin fold in mm. This value helps in estimating body fat.")
    
    with col2:
        st.session_state['Insulin'] = st.text_input('Insulin Level', value=st.session_state['Insulin'], help="Enter the 2-hour serum insulin level in mu U/ml. This helps in assessing insulin production and resistance.")
    
    with col3:
        st.session_state['BMI'] = st.text_input('BMI value', value=st.session_state['BMI'], help="Enter the Body Mass Index (BMI) value, calculated as weight in kg divided by the square of height in meters. It indicates body fat and health risk.")
    
    with col1:
        st.session_state['DiabetesPedigreeFunction'] = st.text_input('Diabetes Pedigree Function value', value=st.session_state['DiabetesPedigreeFunction'], help="Enter the diabetes pedigree function value, a measure of the genetic risk of diabetes based on family history.")
    
    with col2:
        st.session_state['Age'] = st.text_input('Age of the Person', value=st.session_state['Age'], help="Enter the age of the patient in years. This value should be a whole number.")
    
    # Code for Prediction
    diab_diagnosis = ''

    # Creating a button for Prediction
    if st.button('Diabetes Test Result'):
        with st.spinner('Predicting...'):
            # Check if all fields are filled
            if st.session_state['Pregnancies'] == '' or st.session_state['Glucose'] == '' or st.session_state['BloodPressure'] == '' or st.session_state['SkinThickness'] == '' or st.session_state['Insulin'] == '' or st.session_state['BMI'] == '' or st.session_state['DiabetesPedigreeFunction'] == '' or st.session_state['Age'] == '':
                st.warning('Please fill in all the input fields to get an accurate prediction.')
            else:
                # Perform prediction
                diab_prediction = diabetes_model.predict([[float(st.session_state['Pregnancies']), float(st.session_state['Glucose']), float(st.session_state['BloodPressure']), float(st.session_state['SkinThickness']), float(st.session_state['Insulin']), float(st.session_state['BMI']), float(st.session_state['DiabetesPedigreeFunction']), float(st.session_state['Age'])]])
                st.session_state['features'] = {
                    'Pregnancies': float(st.session_state['Pregnancies']),
                    'Glucose': float(st.session_state['Glucose']),
                    'Blood Pressure': float(st.session_state['BloodPressure']),
                    'Skin Thickness': float(st.session_state['SkinThickness']),
                    'Insulin': float(st.session_state['Insulin']),
                    'BMI': float(st.session_state['BMI']),
                    'Diabetes Pedigree Function': float(st.session_state['DiabetesPedigreeFunction']),
                    'Age': float(st.session_state['Age'])
                }
                st.session_state['diabetic'] = (diab_prediction[0] == 1)
                if st.session_state['diabetic']:
                    diab_diagnosis = 'The person is diabetic'
                else:
                    diab_diagnosis = 'The person is not diabetic'
    st.write(diab_diagnosis)
    st.info('Please fill in all the input fields with the appropriate values to get an accurate prediction.', icon="ℹ️")

# Graphs/Charts Page
if selected == 'Graphs/Charts':
    
    # Page title with color
    colored_title('Diabetes Predictions Charts/Graphs', '#007bff')  # Adjust color as needed
    
    # Warning to make predictions first
    st.warning('Please make a prediction on the Diabetes Prediction page before viewing charts here.')
    
    # Check if the user has made predictions
    if st.session_state['features']:
        features = st.session_state['features']
        feature_names = list(features.keys())
        feature_values = list(features.values())
        
        # Calculate feature importance based on input values (for demonstration)
        feature_importance = dict(zip(feature_names, feature_values))
        
        # Sort features by their importance (in this case, just their values)
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        sorted_feature_names, sorted_feature_values = zip(*sorted_features)

        # Display charts in single column layout
        st.write("### Feature Charts")

        # Bar chart for all features
        fig, ax = plt.subplots(figsize=(12, 8))
        color = 'red' if st.session_state['diabetic'] else 'green'
        ax.barh(sorted_feature_names, sorted_feature_values, color=color)
        ax.set_title('Feature Values' if st.session_state['diabetic'] else 'Feature Values for Non-Diabetic Case')
        ax.set_xlabel('Value')
        ax.set_ylabel('Feature')
        plt.tight_layout()  # Ensure layout is tight
        st.pyplot(fig)  # Display the chart
        
        # Save bar chart as image
        bar_chart_image = save_plot_as_image(fig)
        st.download_button(label='Download Bar Chart', data=bar_chart_image, file_name='bar_chart.png', mime='image/png')

        # Pie chart for feature distribution with improved readability
        fig, ax = plt.subplots(figsize=(12, 12))
        explode = [0.1] * len(sorted_feature_values)  # Highlight all slices equally
        wedges, texts, autotexts = ax.pie(
            sorted_feature_values, 
            labels=sorted_feature_names, 
            autopct='%1.1f%%', 
            colors=sns.color_palette('pastel'),
            startangle=140,
            explode=explode
        )
        
        # Improve readability
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=12)
        ax.set_title('Feature Distribution' if st.session_state['diabetic'] else 'Feature Distribution for Non-Diabetic Case')
        plt.tight_layout()  # Ensure layout is tight
        st.pyplot(fig)  # Display the pie chart
        
        # Save pie chart as image
        pie_chart_image = save_plot_as_image(fig)
        st.download_button(label='Download Pie Chart', data=pie_chart_image, file_name='pie_chart.png', mime='image/png')

        # Display detailed feature values below the charts
        st.write("### Detailed Feature Values:")
        for feature, value in feature_importance.items():
            st.write(f"**{feature}**: {value}")

    else:
        st.write("No prediction made yet. Please go to the 'Diabetes Prediction' page and submit your details for prediction.")
