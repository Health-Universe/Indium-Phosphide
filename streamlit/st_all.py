  
"""
This is where the user interface is made using the streamlit package.
"""
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color: indigo;'>Machine Learning for Quantum Dots Synthesis  - Cossairt Laboratory</h1>", unsafe_allow_html=True)

if "InP_QD" not in st.session_state:
    st.session_state.InP_QD = False
if "CdSe_QD" not in st.session_state:
    st.session_state.CdSe_QD = False

row0_1, row0_2, row0_3, row0_4, row0_5 = st.columns(5)
with row0_2:
    st.write("Choose a quantum dot:")
with row0_3:
    cdse = st.button('Cadmium Selenide')
with row0_4:
    inp = st.button('Indium Phosphide')

if inp or st.session_state.InP_QD:
    st.session_state.InP_QD = True
    st.session_state.CdSe_QD = False

    st.header('Predicting Properties of InP Quantum Dots')

    st.markdown('****')
    st.write('Answer the questions below about your InP quandum dots synthesis and we will predict the diameter, absorbance max, and emission wavelength of your dots.')
    st.markdown('****')

    row1_1, row1_2 = st.columns(2)

    with row1_1:
        st.subheader("Indium precursor")
        
        # Creating indium question

        In = st.radio(
                        "What is the indium source?",
                        ('indium acetate', 
                        'indium bromide', 
                        'indium chloride', 'indium iodide',
                        'indium myristate', 'chloroindium oxalate', 
                        'indium oxalate', 'indium palmitate', 
                        'indium trifluoroacetate'))

    with row1_2:
        st.subheader("Phosphorus precursor")

        # Creating phosphorus question

        P = st.radio(
                        "What is the phosphorus source?",
                        ('tris(trimethylsilyl)phosphine - P(TMS)3',
                        'tris(dimethylamino)phosphine - P(NMe2)3',
                        'tris(diethylamino)phosphine - P(NEt2)3',
                        'bis(trimethylsilyl)phosphine'
                        'phosphine gas',
                        'phosphorus trichloride',
                        'white phosphorus',
                        'sodium phosphide',))
        st.markdown("######")
        st.markdown("##")



    row1a_1, row1a_2 = st.columns(2)

    with row1a_1:
        In_amount = st.number_input(label='How much In source is used in mmol? (mmol)', value=0.00)
    with row1a_2:
        P_amount = st.number_input(label='How much P source is used in mmol? (mmol)', value=0.00)



    st.markdown('****')





    st.subheader("Solvents and ligands")
    row2_1, row2_2, row2_3, row2_4, row2_5 = st.columns(5)


    with row2_1:

        # Creating solvent question
        sol = st.radio(
                        "What is the non-coordinating solvent?",
                        ('None',
                        'octadecene - ODE',
                        'toluene',
                        'mesitylene',
                        'dimethylformamide - DMF',))


    with row2_2:

    # Creating TOP question

        TOP = st.radio(
                        "Do you add trioctylphosphine?",
                        ('No',
                        'Yes',))


    with row2_3:

        # Creating acid question
        acid = st.radio(
                        "Do you add any acid?",
                        ('None',
                        'stearic acid',
                        'myristic acid',
                        'oleic acid',
                        'palmitic acid',))


    with row2_4:

        # Creating amine question
        amine = st.radio(
                        "Do you add any amine?",
                        ('None',
                        'oleylamine',
                        'octylamine',
                        'hexadecylamine',
                        'dioctylamine'))


    with row2_5:

        # Creating thiol question
        thiol = st.radio(
                        "Do you add any thiol?",
                        ('None',
                        'dodecanethiol'))


    row2a_1, row2a_2, row2a_3, row2a_4, row2a_5 = st.columns(5)

    with row2a_1:

        sol_amount = st.number_input(label='How much solvent is used? (mL)', value=0.00)
        if sol == 'None':
            sol_amount = 0.00


    with row2a_2:

        TOP_amount = st.number_input(label='If yes, how much? (mmol)', value=0.00)
        if TOP == 'No':
            TOP = "None"
            TOP_amount = 0.00


    with row2a_3:

        acid_amount = st.number_input(label='How much acid is used in mmol? (mmol)', value=0.00)

        if acid == 'None':
            acid_amount = 0.00


    with row2a_4:

        amine_amount = st.number_input(label='How much amine is used in mmol? (mmol)', value=0.00)
        
        if amine == 'None':
            amine_amount = 0.00


    with row2a_5:

        thiol_amount = st.number_input(label='How much thiol is used? (mmol)', value=0.00)
        if thiol == 'None':
            thiol_amount = 0.00




    st.markdown('****')


    st.subheader("Additives")
    row3_1, row3_2 = st.columns(2)
    with row3_1:
        # Creating zinc question
        zinc = st.radio(
                        "Do you add any zinc?",
                        ('None',
                        'zinc chloride',
                        'zinc bromide',
                        'zinc iodide',
                        'zinc acetate',
                        'zinc octanoate',
                        'zinc oleate',
                        'zinc stearate'))


    with row3_2:
    # Other
        other = st.radio(
                        "Do you add any other compound?",
                        ('None',
                        'trioctylphosphine oxide',
                        'superhydride',
                        'copper bromide',
                        'tetrabutylammonium myristate'))



    row3a_1, row3a_2 = st.columns(2)
    with row3a_1:

        zinc_amount = st.number_input(label='How much zinc is used? (mmol)', value=0.00)
        if zinc == 'None':
            zinc_amount = 0.00


    with row3a_2:

        other_amount = st.number_input(label='How much in mmol? (mmol)', value=0.00)
        if other == 'None':
            other_amount = 0.00



    st.markdown('****')


    st.subheader("Reaction Conditions")
    row4_1, row4_2, row4_3 = st.columns(3)

    with row4_1:
        # Reaction volume
        vol = st.number_input(label='What is the total volume of the reaction? (mL)', value=0.00)

    with row4_2:
        # Reaction temperature
        temp = st.number_input(label='What is the nucleation temperature? (C)', value=0.0)

    with row4_3:
        # Reaction time
        time = st.number_input(label='What is the reaction time (min)?', value=0.0)




    #Rearange users' choice into a list to input to the ML model
    user_input = [ In, In_amount, P, P_amount, sol, sol_amount, 
                TOP, TOP_amount, acid, acid_amount, 
                amine, amine_amount, thiol, thiol_amount,
                zinc, zinc_amount, other, other_amount, 
                vol, temp, time
                ]

    #Naming each choice in the user input
    user_df = pd.DataFrame(np.array(user_input).reshape(1, -1), columns=['in_source',
                                                                        'in_amount_mmol',
                                                                        'p_source',
                                                                        'p_amount_mmol',
                                                                        'sol',
                                                                        'sol_amount_ml',
                                                                        'TOP',
                                                                        'TOP_amount_mmol',
                                                                        'acid',
                                                                        'acid_amount_mmol',
                                                                        'amine',
                                                                        'amine_amount_mmol',
                                                                        'thiol',
                                                                        'thiol_amount_mmol',
                                                                        'zinc',
                                                                        'zinc_amount_mmol',
                                                                        'other',
                                                                        'other_amount_mmol',
                                                                        'total_volume_ml',
                                                                        'temp_c',
                                                                        'time_min'             ])
    #Print user inputs

    st.subheader("Check your input")
    st.write(user_df)

    #Scaling and encoding user input using the raw dataset
    df = pd.read_csv('../dataset/hao_dataset.csv')
    #Separate out initial DataFrame into the input features and output features
    df_input = df.drop(columns =['diameter_nm', 'abs_nm', 'emission_nm','doi','user','date_input'], inplace = False, axis = 1)
    df_output_d = df['diameter_nm']
    df_output_a = df['emission_nm']
    df_output_e = df['abs_nm']


    df_input['temp_c'] = df_input['temp_c'].astype(float)
    input_num_cols = [col for col in df_input.columns if df[col].dtypes !='O']
    input_cat_cols = [col for col in df_input.columns if df[col].dtypes =='O']

    ct = ColumnTransformer([
        ('step1', StandardScaler(), input_num_cols),
        ('step2', OneHotEncoder(sparse=False, handle_unknown='ignore'), input_cat_cols)
    ], remainder = 'passthrough')

    ct.fit_transform(df_input)


    #Use same column transformer on user input
    X = ct.transform(user_df)

    diameter_model = joblib.load('model_InP_SO_diameter_DecisionTree.joblib')
    abs_model = joblib.load('model_InP_SO_abs_DecisionTree.joblib')
    emission_model = joblib.load('model_InP_SO_emission_ExtraTrees.joblib')

    diameter_predicted = diameter_model.predict(X)
    abs_predicted = abs_model.predict(X)
    emission_predicted = emission_model.predict(X)

    st.markdown('****')

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col3:
        predict = st.button('PREDICT')
    c1, c2, c3 =  st.columns([1,1,1])
    if predict:
        with c2:
            st.write('Predicted diameter is', round(diameter_predicted[0], 3))
            st.write('Predicted absorbance max is', round(abs_predicted[0], 3))
            st.write('Predicted emission is', round(emission_predicted[0], 3))






if cdse or st.session_state.CdSe_QD:
    st.session_state.CdSe_QD = True
    st.session_state.InP_QD = False

    st.header('Predicting Properties of CdSe Quantum Dots')

    st.markdown('****')
    st.write('Answer the questions below about your CdSe quandum dots synthesis and we will predict the diameter, absorbance max, and emission wavelength of your dots.')
    st.markdown('****')


    row4_1, row4_2, row4_3, row4_4 = st.columns(4)
    with row4_1:
        Cd = st.radio('1. What is your cadmium source?', 
                    ['cadmium stearate', 
                     'cadmium oxide', 
                     'dimethylcadmium',
                     'cadmium acetate', 
                     'cadmium acetate dihydrate'])
    with row4_2:
        Acid = st.radio('2. What is your carboxylic acid source?', 
                    ['None', 
                     'myrstic acid', 
                     'oleic acid', 
                     'stearic acid',
                     'benzoic acid', 
                     'dodecylphosphonic acid',
                     'ethylphosphonic acid', 
                     'lauric acid'])
    with row4_3:
        Amine = st.radio('3. What is your amine source?', 
                    ['None', 
                     '2-6-dimethylpyridine', 
                     'aniline', 
                     'benzylamine',
                     'dioctylamine/hexadecylamine', 
                     'dodecylamine',
                     'heptylamine', 
                     'hexadecylamine', 
                     'octadecylamine',
                     'octylamine', 
                     'oleylamine', 
                     'pyridine', 
                     'trioctylamine'])
    with row4_4:
        Ph = st.radio('4. What is your phosphine source?', 
                    ['None', 
                     'diphenylphosphine', 
                     'tributylphosphine',
                     'trioctylphosphine', 
                     'triphenylphosphine'])

    row4a_1, row4a_2, row4a_3, row4a_4 = st.columns(4)
    with row4a_1:
        Cd_amount = st.number_input(label='How much Cd source in mmol? (mmol)', value=0.00)
    with row4a_2:
        Acid_amount = st.number_input(label='How much acid in mmol? (mmol)', value=0.00)
        if Acid == 'None':
            Acid_amount = 0.00
    with row4a_3:
        Amine_amount = st.number_input(label='How much amine in mmol? (mmol)', value=0.00)
        if Amine == 'None':
            Amine_amount = 0.00
    with row4a_4:
        Ph_amount = st.number_input(label='How much phosphine in mmol? (mmol)', value=0.00)
        if Ph == 'None':
            Ph_amount = 0.00

    Se_amount = st.number_input(label='5. Selenium power is used; how much Selenium do you plan to use? (mmol)')


    st.markdown('****')
    st.subheader("Solvents: ")


    row5_1, row5_2 = st.columns(2)
    with row5_1:
        sol1 = st.radio('6. What is your first solvent?',
                        ['None', 
                        'liquid parafin', 
                        'octadecene',
                        'phenyl ether', 
                        'trioctylphosphine oxide'])
    with row5_2:
        sol2 = st.radio('7. What is your second solvent?',
                        ['None', 
                        'phosphinic acid', 
                        'trioctylphosphine oxide'])
    


    row5a_1, row5a_2 = st.columns(2)
    with row5a_1:
        sol1_amount = st.number_input(label='How much first solvent in g? (g)', value=0.00)
        if sol1 == 'None':
            sol1_amount = 0.00
    with row5a_2:
        sol2_amount = st.number_input(label='How much second solvent in g? (g)', value=0.00)
        if sol2 == 'None':
            sol2_amount = 0.00


    st.markdown('****')


    st.subheader("Reaction Conditions: ")
    row6_1, row6_2 = st.columns(2)
    with row6_1:
        # Reaction temperature
        Temp = st.number_input(label='8. What is the nucleation temperature? (C)', value=0.0)

    with row6_2:
        # Reaction time
        Time = st.number_input(label='9. What is the reaction time (min)?', value=0.0)

    

    #Rearange users' choice into a list to input to the ML model
    user_input = [Temp, 
                  Cd, 
                  Cd_amount,
                  Se_amount,
                  Acid,
                  Acid_amount,
                  Amine,
                  Amine_amount,
                  Ph,
                  Ph_amount,
                  sol1,
                  sol1_amount,
                  sol2,
                  sol2_amount,
                  Time]

    #Naming each choice in the user input
    user_df = pd.DataFrame(np.array(user_input).reshape(1, -1), columns=['Growth Temp (Celsius)',
                                                'Metal_source', 'Metal_mmol (mmol)',
                                                'Chalcogen_mmol (mmol)', 'Carboxylic_Acid',
                                                'CA_mmol (mmol)', 'Amines', 'Amines_mmol (mmol)',
                                                'Phosphines', 'Phosphines_mmol (mmol)',
                                                'Solvent I', 'S_I_amount (g)',
                                                'Solvent II', 'S_II_amount (g)', 'Time_min (min)'
                                                ])
    #Print user inputs
    st.write(user_df)

    #Scaling and encoding user input using the raw dataset
    df = pd.read_csv('../CdSe/dataset_CdSe_raw.csv')

    #Separate out initial DataFrame into the input features and output features
    df_input = df.drop(columns =['Injection Temp (Celsius)', 'Metal_amount (g)',
    'Metal_concentration (mmol/g)', 'Chalcogen_amount (g)', 'Chalcogen_concentration (mmol/g)',
    'Metal/Se_ratio', 'CA_amount (g)', 'Cd/CA_ratio', 'Amines_amount (g)', 'Phosphines_amount (g)',
    'Chalcogen/Ph_ratio','Total_amount (g)','Chalcogen_source','diameter_nm', 'abs_nm',
    'emission_nm', 'Diameter from', 'Citation'],
    inplace = False, axis = 1)

    #Checks the column names, and ensures that they do not have any leading or trailing spaces
    df_input.columns = df_input.columns.str.strip()

    #Converts the values in Growth Temperature Column into float types
    df_input['Growth Temp (Celsius)'] = df_input['Growth Temp (Celsius)'].astype(float)

    #Initializes 2 lists to contain all of the numerical and categorical input columns
    input_num_cols = [col for col in df_input.columns if df[col].dtypes !='O']
    input_cat_cols = [col for col in df_input.columns if df[col].dtypes =='O']

    ct = ColumnTransformer([
        ('step1', StandardScaler(), input_num_cols),
        ('step2', OneHotEncoder(sparse=False, handle_unknown='ignore'), input_cat_cols)
    ], remainder = 'passthrough')


    ct.fit_transform(df_input)

    #Use same column transformer on user input
    X = ct.transform(user_df)

    #Load and use ExtraTrees ML model to predict outcomes
    load_Extra_Trees = joblib.load('model_CdSe_MO_ExtraTrees.joblib')
    predicted = load_Extra_Trees.predict(X)
    st.markdown('****')
    st.markdown('****')

    st.write('Predicted diameter is', round(predicted[0, 0], 3))
    st.write('Predicted absorbance max is', round(predicted[0, 1], 3))
    st.write('Predicted emission is', round(predicted[0, 2], 3))



st.subheader('Updated 09/06/2021')
st.write('Contact: haon02@uw.edu')