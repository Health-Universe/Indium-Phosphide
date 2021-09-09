"""
This is where the user interface is made using the streamlit package.
"""
import base64
import numpy as np
import pandas as pd
import streamlit as st
import pathlib

from datetime import date

today = date.today()

#Title
st.title('InP Quantum Dots Synthesis Project  - Cossairt Laboratory')
st.header('Department of Chemistry - University of Washington')

#User's name
User = st.text_input(label='What\'s your name?')
st.markdown('****')

#Text explaining
st.header('Data Input')
st.markdown(
    'In this section, you will input synthetic conditions and some properties of the quantum dots. **Please strictly follow these rules for data entry:**')
st.markdown('- Please enter EVERYTHING in lowercase!')
st.markdown('- Please no trailing spaces')
st.markdown('- Please do not enter any information twice')
st.markdown('- Please type "None" if the paper doesn\'t provide the information')
st.markdown('- If there are additional important details in the paper that you do not see a place to enter, please let Hao or Florence know')
st.markdown('- For numerical entries, please follow the unit in parentheses and ONLY type in the number. You may have to do some calculations')
st.markdown('****')

#getting user's doi
st.subheader('DOI')
st.markdown(
    'First, you will need to paste the DOI of the paper you are about to use. Check if someone has already input that paper.')

DOI = st.text_input(
    label='1. Type or paste a DOI name into the text box below. E.g. 10.1000/xyz123')

#putting doi and user's name in a list then convert to a class
doi_input = [DOI, User]

doi_df = pd.DataFrame(np.array(doi_input).reshape(1, -1), columns=['DOI', 'User'])

#Check if doi exists in current doi list and deposit new doi
df = pd.read_csv('InP/doi.csv')

st.write('Your DOI:')
st.write(doi_df)
if st.button('Click here to check your DOI'):
    if (df['DOI'] == DOI).any():
        st.markdown('**This paper has already been used. Please make sure NOT to repeat entries!**')
    else:
        doi_df.to_csv('InP/doi.csv', mode='a', header=False, index=False)
        st.markdown('**DOI list is updated**')

st.write('Current DOI list:')
st.write(pd.read_csv('InP/doi.csv'))
st.markdown('****')

#Questions for synthetic conditions
st.subheader('Precursors')

Cluster = st.radio('2. Is this a cluster heat-up synthesis?', ('Yes', 'No'))

if Cluster == 'Yes':
    Cluster_source = "In37P20"
else:
    Cluster_source = "None"

Cluster_amount = st.number_input(label='3. How much cluster is used? (mmol)', value=0.0)
Cluster_ligand = st.text_input(label='4. What is the ligand on the cluster? (eg. myristate, oleate)')
Cluster_ligand_amount = Cluster_amount*51

st.markdown('If this was a cluster synthesis, please treat the remaining precursor questions as those *other than the cluster*')
st.markdown('****')

In_source = st.text_input(label='6. What is the indium source? (e.g. indium acetate, indium chloride, etc.)')
In_amount = st.number_input(label='7. How much In source is used? (mmol)', value=0.0)
st.markdown('****')

Acid_source = st.text_input(label='8. What acid is used? (e.g. lauric acid, mystiric acid, palmitic acid, etc.)')
Acid_amount = st.number_input(label='9. How much acid is used? (mmol)', value=0.0)
st.markdown('****')

P_source = st.text_input(label='10. What is the phosphorus source? (e.g. tris(trimethylsilyl)phosphine, tris(dimethylamino)phenol, etc.)')
P_amount = st.number_input(label='11. How much phosphorus source is used? (mmol)', value=0.0)
st.markdown('****')

st.subheader('Solvents')

Sol_1 = st.text_input(label='12. What is the first solvent? (e.g. octadecene, trioctylphosphine, etc.)')
Sol_1_amount = st.number_input(label='13. How much of the first solvent is used?', value=0.0)
Sol_1_unit = st.radio('14. What unit?', ('None', 'g', 'mL', 'mmol'))
st.markdown('****')

Sol_2 = st.text_input(label='15. What is the second solvent? (e.g. octadecene, trioctylphosphine, etc.)')
Sol_2_amount = st.number_input(label='16. How much of the second is used?', value=0.0)
Sol_2_unit = st.radio('17. What unit?', ('None', 'g', 'mL', 'mmol'))
st.markdown('****')

st.subheader('Ligands')

Ligand_source = st.text_input(label='18. Any ligand used in addition to acid source or solvent? (eg. amine, thiol)')
Ligand_amount = st.number_input(label='19. How much ligand is used? (mmol)', value=0.0)
st.markdown('****')

st.subheader('Other reagents')

Other1 = st.text_input(label='20. Other compound 1 (e.g. zinc chloride)')
Other1_amount = st.number_input(label='21. Amount', value=0.0)
Other1_unit = st.radio('22. What unit?', ('None', 'mg', 'mL', 'mmol'))
st.markdown('****')

Other2 = st.text_input(label='23. Other compound 2 (e.g. zinc chloride)')
Other2_amount = st.number_input(label='24. Amount', value=0.0)
Other2_unit = st.radio('25. What unit?', ('None', 'mg', 'mL', 'mmol'))
st.markdown('****')

st.subheader('Conditions')

Air_free = st.radio('26. Is this an air-free synthesis?', ('Yes', 'No'))

Temp = st.number_input(label='27. What is the growth temperature? (Celsius)', value=0.0)

Time = st.number_input(label='28. What is the growth time? (minute)', value=0.0)

Workup_solvent = st.text_input(label='29. What is the workup solvent?')
Workup_anti = st.text_input(label='30. What is the workup anti-solvent?')

#Outcomes
st.subheader('Properties')

Diameter = st.text_input(label='31. What is the reported **TEM** diameter? (nm)')
Abs = st.text_input(label='32. What is the reported absorbance max? (nm)')
Emission = st.text_input(label='33. What is the reported emission? (nm)')
PLQY = st.text_input(label='34. What is the reported quantum yield? (%)')
st.markdown('****')

#Converting user's inputs to a datarow
user_input = [ User, DOI, 
               Cluster_source, Cluster_amount, 
               Cluster_ligand, Cluster_ligand_amount,
               In_source, In_amount, 
               P_source, P_amount, 
               Sol_1, Sol_1_amount, Sol_1_unit,
               Sol_2, Sol_2_amount, Sol_2_unit, 
               Acid_source, Acid_amount, 
               Ligand_source, Ligand_amount, 
               Other1, Other1_amount, Other1_unit, 
               Other2, Other2_amount, Other2_unit,
               Air_free, Temp, Time, 
               Workup_solvent, Workup_anti, 
               Diameter, Abs, Emission, 
               PLQY, today
             ]

user_df = pd.DataFrame(np.array(user_input).reshape(1, -1), columns=[
        'User', 'DOI', 
        'Cluster source', 'Cluster amount (mmol)', 
        'Cluster ligand', 'Cluster ligand (mmol)',
        'In source',	'In (mmol)',
        'P source',	'P (mmol)',
        'First solvent',	'First sol amount', 'First sol unit',
        'Second solvent',	'Second sol amount', 'Second sol unit',
        'Acid source',	'Acid (mmol)',
        'Other ligand',	'Other ligand (mmol)',
        'Other1',	'Other1 amount', 'Other1 unit',
        'Other2',	'Other2 amount', 'Other2 unit',
        'Airfree?', 'Temp (C)', 'Time (min)', 
        'Workup solvent', 'Workup antisolvent', 
        'diameter (nm)', 'Absorbance (nm)', 'Emission (nm)',
        'PLQY (%)', 'Date input'                             
        ])


#Print user inputs
st.write('Double-check your input, maybe?')
st.write(user_df)

#Inputing user's input to current InP csv
st.write('Click submit when you\'re done')

if st.button('Submit Data'):
    user_df.to_csv('InP/InP_data.csv', mode='a', header=False, index=False)
    st.markdown('***Data submitted!***')

st.write('Current InP data:')
st.write(pd.read_csv('InP/InP_data.csv'))
st.markdown('****')

df = pd.read_csv('InP/InP_data.csv')

csv = df.to_csv(index=False)

b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
# href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
href = f'<a href="data:file/csv;base64,{b64}" download="InP_data.csv">Download csv file</a>'
st.markdown(href, unsafe_allow_html=True)


st.write('Thank you!')

st.write('Updated 04/30/2021')
