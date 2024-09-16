# -*- coding: utf-8 -*-
"""
Created on Sun July 16 05:18:00 2024

@author: Muhammad Hamza
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import numpy as np

# Load diabetes_model.pkl file
diabetes_model = pickle.load(open('diabetes_model.pkl', 'rb'))

# Initialize session state for diabetic status
if 'diabetic' not in st.session_state:
    st.session_state['diabetic'] = False
    st.session_state['features'] = None  # To store the input features

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

# Diabetes Charts or Graphs Page
if selected == 'Graphs/Charts':
    
    # Page title
    st.title('Diabetes Predictions Charts/Graphs')
    
    # Check if the user is diagnosed as diabetic
    if 'diabetic' in st.session_state and st.session_state['diabetic']:
        st.write("The person is diabetic. Showing relevant charts and graphs.")
        
        # Check if features are available
        if st.session_state['features']:
            features = st.session_state['features']
            feature_names = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Diabetes Pedigree Function', 'Age']
            
            # Plot bar chart for diabetic factors
            fig, ax = plt.subplots()
            ax.barh(feature_names, features, color='red')
            ax.set_title('Factors Contributing to Diabetes Diagnosis')
            ax.set_xlabel('Value')
            ax.set_ylabel('Feature')
            
            st.pyplot(fig)  # Display the chart
        
    else:
        st.write("The person is not diabetic. Showing factors for non-diabetic.")
        
        # Check if features are available
        if st.session_state['features']:
            features = st.session_state['features']
            feature_names = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Diabetes Pedigree Function', 'Age']
            
            # Plot bar chart for non-diabetic factors
            fig, ax = plt.subplots()
            ax.barh(feature_names, features, color='green')
            ax.set_title('Factors Contributing to Non-Diabetes')
            ax.set_xlabel('Value')
            ax.set_ylabel('Feature')
            
            st.pyplot(fig)  # Display the chart
