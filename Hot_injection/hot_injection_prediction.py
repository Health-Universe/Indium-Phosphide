  
"""
This is where the user interface is made using the streamlit package.
"""
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

st.set_page_config(layout="wide")


# Make titles
st.markdown("<h1 style='text-align: center; color: MediumAquaMarine;'>Machine Learning for Hot Injection Syntheses of Quantum Dots</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: indigo; font-size:22px;'>Cossairt Laboratory - University of Washington</h1>", unsafe_allow_html=True)
st.markdown('***')

def amount_test (chemical, chemical_amount):
    # Raise error if none chemical with amount OR 0.00 amount with chemical
    if chemical == 'None' and chemical_amount != 0.00:
        st.error('None cannot have an amount !!')

    if chemical == 'None':
        chemical_amount = 0.00
        
    if chemical_amount == 0.00 and chemical != 'None':
        st.error('Amount of ' + chemical + ' needed !!')



# Session states
if "current" not in st.session_state:

    st.session_state.current = None

if "inp" not in st.session_state:

    st.session_state.inp = False

if "cdse" not in st.session_state:

    st.session_state.cdse = False


# Create 2 buttons for 2 syntheses
row0_1, row0_2, row0_3, row0_4, row0_5 = st.columns(5)
with row0_2:
    st.write('Choose a synthesis:')
with row0_3:
    inp = st.button("Indium Phosphide")
with row0_4:
    cdse = st.button("Cadmium Selenide")


# Set session states for the two buttons so users can switch between buttons
if inp:

    st.session_state.current = "inp"

if cdse:

    st.session_state.current = "cdse"




# For InP synthesis
if st.session_state.current != None:

    if st.session_state.current == "inp":

        st.header('Predicting Properties of InP Quantum Dots')

        st.markdown('****')

        st.write('Answer the questions below about your InP quandum dots synthesis and we will predict the diameter, absorbance max, and emission wavelength of your dots.')
        
        st.markdown('****')

        row1_1, row1_2 = st.columns(2)

        with row1_1:
            st.subheader("Indium precursor")
            
            # Create question for indium source

            In = st.radio(
                            "What is the indium source?",
                            ('indium acetate', 
                            'indium bromide', 
                            'indium chloride', 
                            'indium iodide',
                            'indium myristate', 
                            'indium trifluoroacetate'))

        with row1_2:
            st.subheader("Phosphorus precursor")

            # Create question for phosphorus source

            P = st.radio(
                            "What is the phosphorus source?",
                            ('tris(trimethylsilyl)phosphine - P(TMS)3',
                            'tris(dimethylamino)phosphine - P(NMe2)3',
                            'tris(diethylamino)phosphine - P(NEt2)3',
                            'bis(trimethylsilyl)phosphine'
                            ))
            st.markdown("######")
            st.markdown("##")


        row1a_1, row1a_2 = st.columns(2)

        with row1a_1:

            # Create question for indium amount
            In_amount = st.number_input(label='How much In source is used in mmol? (mmol)', value=0.00)

            amount_test(In, In_amount)

        with row1a_2:

            # Create question for P amount
            P_amount = st.number_input(label='How much P source is used in mmol? (mmol)', value=0.00)

            amount_test(P, P_amount)



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
                            ))


        with row2_2:

            # Creating TOP question
            TOP = st.radio("Do you add trioctylphosphine?",
                            ('No',
                            'Yes',))


        with row2_3:

            # Creating acid question
            acid = st.radio(
                            "Do you add any acid?",
                            ('None',
                            'lauric acid',
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
            amount_test(sol, sol_amount)


        with row2a_2:

            TOP_amount = st.number_input(label='If yes, how much? (mmol)', value=0.00)
            if TOP == 'No':
                TOP = "None"
                TOP_amount = 0.00
            else:
                TOP = 'TOP'
            amount_test(TOP, TOP_amount)


        with row2a_3:

            acid_amount = st.number_input(label='How much acid is used in mmol? (mmol)', value=0.00)

            amount_test(acid, acid_amount)


        with row2a_4:

            amine_amount = st.number_input(label='How much amine is used in mmol? (mmol)', value=0.00)
            
            amount_test(amine, amine_amount)


        with row2a_5:

            thiol_amount = st.number_input(label='How much thiol is used? (mmol)', value=0.00)
            
            amount_test(thiol, thiol_amount)




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
                            'zinc oleate',
                            'zinc stearate',
                            'zinc undecylenate'))


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
            
            amount_test(zinc, zinc_amount)
            


        with row3a_2:

            other_amount = st.number_input(label='How much in mmol? (mmol)', value=0.00)
            
            amount_test(other, other_amount)



        st.markdown('****')


        st.subheader("Reaction Conditions")
        row4_1, row4_2, row4_3 = st.columns(3)

        with row4_1:

            # Reaction volume
            vol = st.number_input(label='What is the total volume of the reaction? (mL)', value=0.00)
            if vol == 0.0:
                st.error('Reaction volume needs to be greater than 0 mL')

        with row4_2:

            # Reaction temperature
            temp = st.number_input(label='What is the nucleation temperature? (C)', value=0.0)
            if temp == 0.0:
                st.error('Reaction temperature needs to be greater than 0 C')

        with row4_3:

            # Reaction time
            time = st.number_input(label='What is the reaction time (min)?', value=0.0)
            if time == 0.0:
                st.error('Reaction time needs to be greater than 0 mim')



        # Rearange users' choice into a list to input to the ML model
        user_input_InP = [ In, In_amount, P, P_amount, sol, sol_amount, 
                    TOP, TOP_amount, acid, acid_amount, 
                    amine, amine_amount, thiol, thiol_amount,
                    zinc, zinc_amount, other, other_amount, 
                    vol, temp, time
                    ]

        # Naming each choice in the user input
        user_df_InP = pd.DataFrame(np.array(user_input_InP).reshape(1, -1), columns=['in_source',
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
        st.write(user_df_InP)

        #Scaling and encoding user input using the raw dataset
        df_InP_1 = Path(__file__).parents[0] / 'hao_dataset_HI.csv'
        df_InP = pd.read_csv(df_InP_1)

        #Separate out initial DataFrame into the input features and output features
        df_input_InP = df_InP.drop(columns =['diameter_nm', 'abs_nm', 'emission_nm','doi','user','date_input'], inplace = False, axis = 1)
        df_output_d_InP = df_InP['diameter_nm']
        df_output_e_InP = df_InP['emission_nm']
        df_output_a_InP = df_InP['abs_nm']


        df_input_InP['temp_c'] = df_input_InP['temp_c'].astype(float)
        input_num_cols_InP = [col for col in df_input_InP.columns if df_InP[col].dtypes !='O']
        input_cat_cols_InP = [col for col in df_input_InP.columns if df_InP[col].dtypes =='O']

        ct_InP = ColumnTransformer([
            ('step1', StandardScaler(), input_num_cols_InP),
            ('step2', OneHotEncoder(sparse=False, handle_unknown='ignore'), input_cat_cols_InP)
        ], remainder = 'passthrough')

        ct_InP.fit_transform(df_input_InP)


        # Use same column transformer on user input
        X_InP = ct_InP.transform(user_df_InP)

        # Loading ML models for 3 outputs
        diameter_model = joblib.load(Path(__file__).parents[0] / 'model_SO_diameter_ExtraTrees_HI.joblib')
        abs_model = joblib.load(Path(__file__).parents[0] / 'model_SO_abs_ExtraTrees_HI.joblib')
        emission_model = joblib.load(Path(__file__).parents[0] / 'model_SO_emission_DecisionTree_HI.joblib')


        # Make predictions

        diameter_In_predicted = diameter_model.predict(X_InP)
        abs_In_predicted = abs_model.predict(X_InP)
        emission_In_predicted = emission_model.predict(X_InP)

        st.markdown('****')

        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
        with col3:

            predict = st.button('PREDICT')

        c1, c2, c3 =  st.columns([1,1,1])
        if predict:

            with c2:
                st.write("")
                st.write("")
                st.write("")
        
                st.write('Predicted diameter is', round(diameter_In_predicted[0], 3))
                st.write('Predicted absorbance max is', round(abs_In_predicted[0], 3))
                st.write('Predicted emission is', round(emission_In_predicted[0], 3))
    

    else:
        # For CdSe synthesis

        st.header('Predicting Properties of CdSe Quantum Dots')

        st.markdown('****')
        st.write('Answer the questions below about your CdSe quandum dots synthesis and we will predict the diameter, absorbance max, and emission wavelength of your dots.')
        st.markdown('****')


        row4_1, row4_2, row4_3, row4_4 = st.columns(4)

        with row4_1:

        #Questions for reactants
            st.subheader('Cadmium precursor:')
            Cd = st.radio('What is your cadmium source?', 
                        ['cadmium stearate', 
                        'cadmium oxide', 
                        'dimethylcadmium',
                        'cadmium acetate', 
                        'cadmium acetate dihydrate'])
        
        with row4_2:

            st.subheader('Ligand source:')
            Acid = st.radio('What is your carboxylic acid source?', 
                        ['None', 
                        'myrstic acid', 
                        'oleic acid', 
                        'stearic acid',
                        'benzoic acid', 
                        'dodecylphosphonic acid',
                        'ethylphosphonic acid', 
                        'lauric acid'])

        with row4_3:

            st.subheader(' ')
            st.subheader(' ')
            Amine = st.radio('What is your amine source?', 
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

            st.subheader(' ')
            st.subheader(' ')
            Ph = st.radio('What is your phosphine source?', 
                        ['None', 
                        'diphenylphosphine', 
                        'tributylphosphine',
                        'trioctylphosphine', 
                        'triphenylphosphine'])


        row4a_1, row4a_2, row4a_3, row4a_4 = st.columns(4)

        with row4a_1:

            Cd_amount = st.number_input(label='How much Cd source in mmol? (mmol)', value=0.00)

            amount_test(Cd, Cd_amount)
            

        with row4a_2:

            Acid_amount = st.number_input(label='How much acid in mmol? (mmol)', value=0.00)
            
            amount_test(Acid, Acid_amount)


        with row4a_3:

            Amine_amount = st.number_input(label='How much amine in mmol? (mmol)', value=0.00)
            
            amount_test(Amine, Amine_amount)


        with row4a_4:

            Ph_amount = st.number_input(label='How much phosphine in mmol? (mmol)', value=0.00)
            
            amount_test(Ph, Ph_amount)
        

        st.markdown('****')
        st.subheader('Selenium')

        Se_amount = st.number_input(label='5. Selenium power is used; how much Selenium do you plan to use? (mmol)')

        if Se_amount == 0.00:
            st.error('Amount of selenium needed !!')


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
            amount_test(sol1, sol1_amount)
            


        with row5a_2:
            sol2_amount = st.number_input(label='How much second solvent in g? (g)', value=0.00)
            amount_test(sol2, sol2_amount)

        st.markdown('****')


        st.subheader("Reaction Conditions: ")
        row6_1, row6_2 = st.columns(2)
        with row6_1:
            # Reaction temperature
            Temp = st.number_input(label='8. What is the nucleation temperature? (C)', value=0.0)
            if Temp == 0.0:
                st.error('Reaction temperature needs to be greater than 0 C')

        with row6_2:
            # Reaction time
            Time = st.number_input(label='9. What is the reaction time (min)?', value=0.0)
            if Time == 0.0:
                st.error('Reaction time needs to be greater than 0 mim')

        

        #Rearange users' choice into a list to input to the ML model
        user_input_CdSe = [Temp, 
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
        user_df_CdSe = pd.DataFrame(np.array(user_input_CdSe).reshape(1, -1), columns=['Growth Temp (Celsius)',
                                                    'Metal_source', 'Metal_mmol (mmol)',
                                                    'Chalcogen_mmol (mmol)', 'Carboxylic_Acid',
                                                    'CA_mmol (mmol)', 'Amines', 'Amines_mmol (mmol)',
                                                    'Phosphines', 'Phosphines_mmol (mmol)',
                                                    'Solvent I', 'S_I_amount (g)',
                                                    'Solvent II', 'S_II_amount (g)', 'Time_min (min)'
                                                    ])
        #Print user inputs
        st.subheader("Check your input")
        st.write(user_df_CdSe)

        #Scaling and encoding user input using the raw dataset
        # df_CdSe = pd.read_csv('dataset_CdSe_raw.csv')

        df_CdSe_1 = Path(__file__).parents[0] / 'dataset_CdSe_raw.csv'
        df_CdSe = pd.read_csv(df_CdSe_1)

        #Separate out initial DataFrame into the input features and output features
        df_input_CdSe = df_CdSe.drop(columns =['Injection Temp (Celsius)', 'Metal_amount (g)',
        'Metal_concentration (mmol/g)', 'Chalcogen_amount (g)', 'Chalcogen_concentration (mmol/g)',
        'Metal/Se_ratio', 'CA_amount (g)', 'Cd/CA_ratio', 'Amines_amount (g)', 'Phosphines_amount (g)',
        'Chalcogen/Ph_ratio','Total_amount (g)','Chalcogen_source','diameter_nm', 'abs_nm',
        'emission_nm', 'Diameter from', 'Citation'],
        inplace = False, axis = 1)

        #Checks the column names, and ensures that they do not have any leading or trailing spaces
        df_input_CdSe.columns = df_input_CdSe.columns.str.strip()

        #Converts the values in Growth Temperature Column into float types
        df_input_CdSe['Growth Temp (Celsius)'] = df_input_CdSe['Growth Temp (Celsius)'].astype(float)

        #Initializes 2 lists to contain all of the numerical and categorical input columns
        input_num_cols_CdSe = [col for col in df_input_CdSe.columns if df_CdSe[col].dtypes !='O']
        input_cat_cols_CdSe = [col for col in df_input_CdSe.columns if df_CdSe[col].dtypes =='O']

        ct_CdSe = ColumnTransformer([
            ('step1', StandardScaler(), input_num_cols_CdSe),
            ('step2', OneHotEncoder(sparse=False, handle_unknown='ignore'), input_cat_cols_CdSe)
        ], remainder = 'passthrough')


        ct_CdSe.fit_transform(df_input_CdSe)

        #Use same column transformer on user input
        X_CdSe = ct_CdSe.transform(user_df_CdSe)


        diameter_CdSe_model = joblib.load(Path(__file__).parents[0] / 'model_CdSe_SO_diameter_ExtraTrees.joblib')
        abs_CdSe_model = joblib.load(Path(__file__).parents[0] / 'model_CdSe_SO_abs_DecisionTree.joblib')
        emission_CdSe_model = joblib.load(Path(__file__).parents[0] / 'model_CdSe_SO_emission_DecisionTree.joblib')

        diameter_CdSe_predicted = diameter_CdSe_model.predict(X_CdSe)
        abs_CdSe_predicted = abs_CdSe_model.predict(X_CdSe)
        emission_CdSe_predicted = emission_CdSe_model.predict(X_CdSe)

        st.markdown('****')

        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
        with col3:
            predict = st.button('PREDICT')
        c1, c2, c3 =  st.columns([1,1,1])
        if predict:
            with c2:
                st.write('Predicted diameter is', round(diameter_CdSe_predicted[0], 3))
                st.write('Predicted absorbance max is', round(abs_CdSe_predicted[0], 3))
                st.write('Predicted emission is', round(emission_CdSe_predicted[0], 3))
    


st.subheader('Updated 12/13/2021')
st.write('Contact: haon02@uw.edu')