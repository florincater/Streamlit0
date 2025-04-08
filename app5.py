import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("CSV Data Explorer 📊")

# 1. Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV with error handling for corrupt files
        df = pd.read_csv(uploaded_file)
        
        # Check if DataFrame is empty
        if df.empty:
            st.error("Error: The uploaded file is empty.")
            st.stop()  # Halt execution
        
        # 2. Display raw data
        st.subheader("Raw Data")
        st.dataframe(df)

        # 3. Select column to plot (only numeric columns allowed)
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        if not numeric_columns:
            st.error("Error: No numeric columns found in the data.")
            st.stop()
        
        column = st.selectbox("Select a column to visualize", numeric_columns)

        # 4. Choose plot type
        plot_type = st.radio("Select plot type", ["Line Chart", "Bar Chart", "Histogram"])

        # 5. Generate the plot
        st.subheader(f"Plot of {column}")
        fig, ax = plt.subplots()

        try:
            if plot_type == "Line Chart":
                ax.plot(df[column])
            elif plot_type == "Bar Chart":
                ax.bar(df.index, df[column])
            elif plot_type == "Histogram":
                ax.hist(df[column], bins=20)
            
            ax.set_title(column)
            st.pyplot(fig)
        
        except Exception as e:
            st.error(f"Plotting failed: {str(e)}")

    except pd.errors.EmptyDataError:
        st.error("Error: The uploaded file is not a valid CSV or is empty.")
    except UnicodeDecodeError:
        st.error("Error: Could not decode the file. Ensure it's a standard CSV.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

else:
    st.warning("Please upload a CSV file to get started.")