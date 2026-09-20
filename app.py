import gradio as gr
import pandas as pd


# ============================================================
# FUNCTION: Generate Research Dataset Description
# ============================================================

def generate_description(file):

    if file is None:
        return "Please upload a CSV or Excel dataset."

    try:

        # Gradio type="filepath" can return a string path
        # This also supports file objects for compatibility
        file_path = file if isinstance(file, str) else file.name

        # ----------------------------------------------------
        # Read Dataset
        # ----------------------------------------------------

        if file_path.lower().endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file_path.lower().endswith(".xlsx"):
            df = pd.read_excel(file_path)

        else:
            return "Please upload a CSV or Excel file."

        # ----------------------------------------------------
        # Dataset Information
        # ----------------------------------------------------

        rows, columns = df.shape

        column_names = list(df.columns)

        numerical_columns = list(
            df.select_dtypes(include="number").columns
        )

        categorical_columns = list(
            df.select_dtypes(exclude="number").columns
        )

        missing_values = int(
            df.isnull().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        # ----------------------------------------------------
        # Missing Values by Column
        # ----------------------------------------------------

        missing_by_column = df.isnull().sum()

        missing_columns = {
            column: int(value)
            for column, value in missing_by_column.items()
            if value > 0
        }

        if missing_columns:
            missing_details = "\n".join(
                f"- {column}: {value}"
                for column, value in missing_columns.items()
            )
        else:
            missing_details = "No missing values detected."

        # ----------------------------------------------------
        # Numerical Statistics
        # ----------------------------------------------------

        if numerical_columns:

            numerical_summary = (
                df[numerical_columns]
                .describe()
                .round(2)
                .to_string()
            )

        else:

            numerical_summary = (
                "No numerical columns available."
            )

        # ----------------------------------------------------
        # Research Dataset Description
        # ----------------------------------------------------

        description = f"""
============================================================
        RESEARCH DATASET DESCRIPTION
============================================================

1. DATASET OVERVIEW
------------------------------------------------------------

The uploaded dataset contains {rows} records and
{columns} variables.

The dataset has been automatically analyzed using
Python and Pandas.

The dataset may be used for exploratory data analysis,
statistical investigation, data visualization, and
machine learning research depending on its subject area.


2. DATASET STRUCTURE
------------------------------------------------------------

Column Names:

{", ".join(map(str, column_names))}


3. DATA TYPES
------------------------------------------------------------

Numerical Columns:

{", ".join(map(str, numerical_columns))
if numerical_columns else "None"}


Categorical / Non-Numerical Columns:

{", ".join(map(str, categorical_columns))
if categorical_columns else "None"}


4. DATA QUALITY ANALYSIS
------------------------------------------------------------

Total Missing Values: {missing_values}

Duplicate Records: {duplicate_rows}


Missing Values by Column:

{missing_details}


5. NUMERICAL STATISTICS
------------------------------------------------------------

{numerical_summary}


6. RESEARCH APPLICATIONS
------------------------------------------------------------

This dataset may be useful for:

• Exploratory Data Analysis
• Statistical Analysis
• Data Visualization
• Pattern Identification
• Machine Learning
• Research Studies
• Predictive Analysis

The actual suitability depends on the subject area,
quality, size, and characteristics of the dataset.


7. AUTOMATED ANALYSIS
------------------------------------------------------------

The dataset description was automatically generated
by the Automated Research Dataset Description Generator.

The system analyzes:

• Dataset dimensions
• Column names
• Data types
• Numerical variables
• Categorical variables
• Missing values
• Duplicate records
• Numerical statistics


8. VALIDATION NOTE
------------------------------------------------------------

The generated description is based on the uploaded
dataset and should be reviewed by the researcher
before being used in a formal research publication.


============================================================
                 END OF DESCRIPTION
============================================================
"""

        return description

    except Exception as error:

        return f"""
Error processing dataset.

Please make sure that:
• The file is a valid CSV or Excel file.
• The file is not corrupted.
• The dataset contains readable data.

Technical Error:
{error}
"""


# ============================================================
# CUSTOM CSS
# ============================================================

css = """
footer {
    display: none !important;
}
"""


# ============================================================
# GRADIO INTERFACE
# ============================================================

with gr.Blocks(
    title="Automated Research Dataset Description Generator"
) as demo:

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    gr.Markdown(
        """
        # 🤖 Automated Research Dataset Description Generator

        ### Agentic AI & Automation Mini Project

        Upload a **CSV or Excel dataset** and automatically
        generate a structured, research-oriented description
        of the dataset.

        **The system analyzes dataset structure, data types,
        missing values, duplicate records, and numerical
        statistics.**
        """
    )

    gr.Markdown("---")

    # --------------------------------------------------------
    # Dataset Upload
    # --------------------------------------------------------

    file_input = gr.File(
        label="📂 Upload CSV or Excel Dataset",
        file_types=[".csv", ".xlsx"],
        type="filepath"
    )

    # --------------------------------------------------------
    # Generate Button
    # --------------------------------------------------------

    generate_button = gr.Button(
        "🚀 Generate Dataset Description",
        variant="primary"
    )

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    output = gr.Textbox(
        label="📄 Generated Research Dataset Description",
        lines=35,
        max_lines=50
    )

    # --------------------------------------------------------
    # Button Action
    # --------------------------------------------------------

    generate_button.click(
        fn=generate_description,
        inputs=file_input,
        outputs=output
    )

    # --------------------------------------------------------
    # Footer Information
    # --------------------------------------------------------

    gr.Markdown(
        """
        ---
        **Project:** Automated Research Dataset Description Generator  
        **Technology:** Python • Pandas • Gradio  
        **Course:** Agentic AI & Automation
        """
    )


# ============================================================
# LAUNCH APPLICATION
# ============================================================

demo.launch()