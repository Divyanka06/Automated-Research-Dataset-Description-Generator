from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
import io

app = FastAPI()

def generate_description_from_bytes(contents, file_name):
    try:
        if file_name.lower().endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif file_name.lower().endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            return "Please upload a valid CSV or Excel file."

        rows, columns = df.shape
        column_names = list(df.columns)
        numerical_columns = list(df.select_dtypes(include="number").columns)
        categorical_columns = list(df.select_dtypes(exclude="number").columns)
        missing_values = int(df.isnull().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        missing_by_column = df.isnull().sum()
        missing_columns = {col: int(val) for col, val in missing_by_column.items() if val > 0}
        
        if missing_columns:
            missing_details = "\n".join(f"- {col}: {val}" for col, val in missing_columns.items())
        else:
            missing_details = "No missing values detected."

        if numerical_columns:
            numerical_summary = df[numerical_columns].describe().round(2).to_string()
        else:
            numerical_summary = "No numerical columns available."

        return f"""============================================================
        RESEARCH DATASET DESCRIPTION
============================================================

1. DATASET OVERVIEW
------------------------------------------------------------
The uploaded dataset contains {rows} records and {columns} variables.
The dataset has been automatically analyzed using Python and Pandas.

2. DATASET STRUCTURE
------------------------------------------------------------
Column Names:
{", ".join(map(str, column_names))}

3. DATA TYPES
------------------------------------------------------------
Numerical Columns:
{", ".join(map(str, numerical_columns)) if numerical_columns else "None"}

Categorical / Non-Numerical Columns:
{", ".join(map(str, categorical_columns)) if categorical_columns else "None"}

4. DATA QUALITY ANALYSIS
------------------------------------------------------------
Total Missing Values: {missing_values}
Duplicate Records: {duplicate_rows}

Missing Values by Column:
{missing_details}

5. NUMERICAL STATISTICS
------------------------------------------------------------
{numerical_summary}

============================================================
                 END OF DESCRIPTION
============================================================
"""
    except Exception as error:
        return f"Error processing dataset.\n\nTechnical Error:\n{error}"

@app.get("/", response_class=HTMLResponse)
async def main_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Automated Dataset Description Generator</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background-color: #f9fafb; color: #1f2937; }
            h1 { color: #111827; }
            .card { background: white; padding: 24px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e5e7eb; }
            input[type="file"] { margin: 16px 0; display: block; }
            button { background-color: #2563eb; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; }
            button:hover { background-color: #1d4ed8; }
            pre { background: #1e293b; color: #f8fafc; padding: 16px; border-radius: 6px; overflow-x: auto; white-space: pre-wrap; font-family: monospace; margin-top: 24px; display: none; }
        </style>
    </head>
    <body>
        <h1>🤖 Automated Research Dataset Description Generator</h1>
        <p>Upload a CSV or Excel dataset to generate a structured, research-oriented description.</p>
        <div class="card">
            <input type="file" id="datasetFile" accept=".csv, .xlsx">
            <button onclick="uploadFile()">🚀 Generate Dataset Description</button>
            <pre id="output"></pre>
        </div>

        <script>
            async def uploadFile() {
                const fileInput = document.getElementById('datasetFile');
                const outputBlock = document.getElementById('output');
                if (!fileInput.files[0]) { alert('Please select a file first!'); return; }
                
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                outputBlock.style.display = 'block';
                outputBlock.innerText = 'Analyzing dataset, please wait...';
                
                try {
                    const response = await fetch('/analyze', { method: 'POST', body: formData });
                    const result = await response.text();
                    outputBlock.innerText = result;
                } catch (err) {
                    outputBlock.innerText = 'An error occurred during submission.';
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    contents = await file.read()
    description = generate_description_from_bytes(contents, file.filename)
    return HTMLResponse(content=description, status_code=200)
