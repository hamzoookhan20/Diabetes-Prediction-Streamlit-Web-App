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
import seaborn as sns

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
            
            # Pie chart for feature distribution
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(features, labels=feature_names, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
            ax.set_title('Feature Distribution for Diabetic Case')
            st.pyplot(fig)  # Display the pie chart
            
            # Scatter plot to visualize relationships between some features
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(features[1], features[5], color='blue', label='Glucose vs BMI')
            ax.set_xlabel('Glucose Level')
            ax.set_ylabel('BMI')
            ax.set_title('Scatter Plot: Glucose Level vs BMI')
            ax.legend()
            st.pyplot(fig)  # Display the scatter plot
            
            # Histogram for each feature
            fig, ax = plt.subplots(figsize=(14, 8))
            for i, feature in enumerate(features):
                ax.hist(features[i], bins=10, alpha=0.5, label=feature_names[i])
            ax.set_title('Histogram of Features for Diabetic Case')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.legend(loc='upper right')
            st.pyplot(fig)  # Display the histogram

            # Box plot for each feature
            fig, ax = plt.subplots(figsize=(14, 8))
            data = np.array(features).reshape(-1, 1)
            ax.boxplot(data, labels=feature_names, patch_artist=True)
            ax.set_title('Box Plot of Features for Diabetic Case')
            ax.set_xlabel('Feature')
            ax.set_ylabel('Value')
            st.pyplot(fig)  # Display the box plot
        
    else:
        st.write("Great news! Based on the provided data, the individual is not diabetic. Here’s a look at some of the healthy feature metrics.")
        
        # Check if features are available
        if st.session_state['features']:
            features = st.session_state['features']
            feature_names = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Diabetes Pedigree Function', 'Age']
            
            # Bar chart for non-diabetic factors
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(feature_names, features, color='green')
            ax.set_title('Factors Contributing to Non-Diabetes')
            ax.set_xlabel('Value')
            ax.set_ylabel('Feature')
            st.pyplot(fig)  # Display the chart
            
            # Pie chart for feature distribution
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(features, labels=feature_names, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
            ax.set_title('Feature Distribution for Non-Diabetic Case')
            st.pyplot(fig)  # Display the pie chart
            
            # Scatter plot to visualize relationships between some features
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(features[1], features[5], color='green', label='Glucose vs BMI')
            ax.set_xlabel('Glucose Level')
            ax.set_ylabel('BMI')
            ax.set_title('Scatter Plot: Glucose Level vs BMI')
            ax.legend()
            st.pyplot(fig)  # Display the scatter plot
            
            # Histogram for each feature
            fig, ax = plt.subplots(figsize=(14, 8))
            for i, feature in enumerate(features):
                ax.hist(features[i], bins=10, alpha=0.5, label=feature_names[i])
            ax.set_title('Histogram of Features for Non-Diabetic Case')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.legend(loc='upper right')
            st.pyplot(fig)  # Display the histogram

            # Box plot for each feature
            fig, ax = plt.subplots(figsize=(14, 8))
            data = np.array(features).reshape(-1, 1)
            ax.boxplot(data, labels=feature_names, patch_artist=True)
            ax.set_title('Box Plot of Features for Non-Diabetic Case')
            ax.set_xlabel('Feature')
            ax.set_ylabel('Value')
            st.pyplot(fig)  # Display the box plot
