# To run program simply 
# 1) Install the necessary libraries, which are found in the requirements.txt file (https://github.com/dmsmiley/Analytics-with-Streamlit/blob/main/requirements.txt).
# 2) Download the file "London.csv" in this repository (https://github.com/dmsmiley/Analytics-with-Streamlit/blob/main/data/London.csv).
# 3) Navigate to the appropriate dictionary in your terminal.
# 4) Execute the following in the terminal: "streamlit run Regression_London-Housing.py"
# 5) Open your web browser to the local host as directed by the terminal.
# 6) Use the parameter settings on the sidebar and dream about living in The Square Mile

# For additional help below is the documentation for Streamlit
# https://docs.streamlit.io/en/stable/

# Please do not hesitate to ask for advice or report a bug!


import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor

st.write("""
# London House Price Prediction App
Use the sidebar to set your parameters for:
- Square footage
- Num. of Bedrooms
- Num. of Bathrooms
- Num. of Receptions
""")
st.write('---')

st.image('data/westminster.jpg', use_column_width=True)
st.write("[Photo by Eva Dang](https://unsplash.com/@evantdang?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText)")


# Loads the Boston House Price Dataset
london = pd.read_csv('data/London.csv', index_col=0)
# Drops non-numeric columns
london = london.drop(columns=['Property Name', 'House Type', 'Location', 'City/County', 'Postal Code'])
# Renames existing columns
london = london.rename(columns={'Price':'PRICE', 'Area in sq ft': 'SQFT', 'No. of Bedrooms': 'BEDS', 'No. of Bathrooms' : 'BATHS', 'No. of Receptions': "RECS"})
# Turns all columns in df to float dtype
london = london.astype(float)

# Preparing training and testing datasets
X = london.drop(columns=['PRICE'])
Y = london['PRICE']

# Sidebar
# Header of Specify Input Parameters
st.sidebar.header('Specify Input Parameters')
def user_input_features():
    SQFT = st.sidebar.slider('SQFT', min_value=int(X.SQFT.min()), max_value=int(X.SQFT.max()),
                             value=int(X.SQFT.mean()))
    BEDS = st.sidebar.number_input('BEDS', min_value=int(X.BEDS.min()), max_value=int(X.BEDS.max()),
                             value=int(X.BEDS.mean()))
    BATHS = st.sidebar.number_input('BATHS', min_value=int(X.BATHS.min()), max_value=int(X.BATHS.max()),
                             value=int(X.BATHS.mean()))
    RECS = st.sidebar.number_input('RECS',min_value=int(X.RECS.min()), max_value=int(X.RECS.max()),
                             value=int(X.RECS.mean()))
    data = {'SQFT': SQFT,
            'BEDS': BEDS,
            'BATHS': BATHS,
            'RECS': RECS}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

# Main Panel
# Print specified input parameters
st.header('Specified Input parameters')
st.write(df)
st.write('---')

# Build Regression Model
model = RandomForestRegressor()
model.fit(X, Y)

# Apply Model to Make Prediction
prediction = model.predict(df)

#Reformat predication score from np.array to $ amount
st.header('Prediction of PRICE')
prediction_float = "£{:,.2f}".format(prediction.item(0))
st.write(prediction_float)
st.write('---')


# Explaining the model's predictions using SHAP values
# https://github.com/slundberg/shap
#explainer = shap.TreeExplainer(model)
#shap_values = explainer.shap_values(X)

#st.header('Feature Importance')
#plt.title('Feature importance based on SHAP values')
#shap.summary_plot(shap_values, X)
#st.set_option('deprecation.showPyplotGlobalUse', False)
#st.pyplot(bbox_inches='tight')
#st.write('---')

#plt.title('Feature importance based on SHAP values (Bar)')
#shap.summary_plot(shap_values, X, plot_type="bar")
#st.pyplot(bbox_inches='tight')
