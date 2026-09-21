from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
import io

app = FastAPI()


# ============================================================
# DATASET ANALYSIS
# ============================================================

def generate_description_from_bytes(contents, file_name):

    try:

        # ----------------------------------------------------
        # Read Dataset
        # ----------------------------------------------------

        if file_name.lower().endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))

        elif file_name.lower().endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))

        else:
            return "Please upload a valid CSV or Excel file."

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
        # Missing Values
        # ----------------------------------------------------

        missing_by_column = df.isnull().sum()

        missing_columns = {
            col: int(val)
            for col, val in missing_by_column.items()
            if val > 0
        }

        if missing_columns:

            missing_details = "\n".join(
                f"- {col}: {val}"
                for col, val in missing_columns.items()
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
        # Research Description
        # ----------------------------------------------------

        return f"""
============================================================
        RESEARCH DATASET DESCRIPTION
============================================================

1. DATASET OVERVIEW
------------------------------------------------------------

The uploaded dataset contains {rows} records and
{columns} variables.

The dataset has been automatically analyzed using
Python and Pandas.


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


7. AUTOMATED ANALYSIS
------------------------------------------------------------

The system automatically analyzed:

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

    except Exception as error:

        return f"""
Error processing dataset.

Technical Error:

{error}
"""


# ============================================================
# FRONTEND
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def main_page():

    return """

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
AI Automation | Research Dataset Generator
</title>


<style>

/* =========================================================
   GLOBAL
   ========================================================= */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {

    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    color: #e8f1ff;

    min-height: 100vh;

    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(37, 99, 235, 0.20),
            transparent 30%
        ),

        radial-gradient(
            circle at 85% 20%,
            rgba(14, 165, 233, 0.15),
            transparent 28%
        ),

        radial-gradient(
            circle at 50% 100%,
            rgba(59, 130, 246, 0.12),
            transparent 35%
        ),

        #020617;

    overflow-x: hidden;
}


/* Ambient glow */

body::before {

    content: "";

    position: fixed;

    width: 500px;
    height: 500px;

    top: -200px;
    left: -150px;

    background:
        rgba(37, 99, 235, 0.12);

    filter: blur(100px);

    border-radius: 50%;

    pointer-events: none;
}


/* =========================================================
   MAIN CONTAINER
   ========================================================= */

.container {

    width: min(1180px, 92%);

    margin: auto;

    padding:
        30px 0 70px;
}


/* =========================================================
   NAVBAR
   ========================================================= */

.navbar {

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 18px 0 35px;
}


.logo {

    display: flex;

    align-items: center;

    gap: 10px;

    font-weight: 700;

    letter-spacing: 0.5px;

    color: #f8fbff;
}


.logo-icon {

    width: 38px;
    height: 38px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 12px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #06b6d4
        );

    box-shadow:
        0 0 25px rgba(37, 99, 235, 0.35);
}


.status {

    display: flex;

    align-items: center;

    gap: 8px;

    padding: 8px 14px;

    border-radius: 30px;

    font-size: 13px;

    color: #bfdbfe;

    background:
        rgba(15, 23, 42, 0.7);

    border:
        1px solid rgba(96, 165, 250, 0.18);
}


.status-dot {

    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #22c55e;

    box-shadow:
        0 0 10px #22c55e;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {

    text-align: center;

    padding: 55px 20px 45px;
}


.badge {

    display: inline-flex;

    align-items: center;

    gap: 8px;

    padding: 8px 15px;

    border-radius: 30px;

    font-size: 12px;

    font-weight: 600;

    letter-spacing: 1px;

    color: #93c5fd;

    background:
        rgba(30, 64, 175, 0.15);

    border:
        1px solid rgba(96, 165, 250, 0.20);

    margin-bottom: 24px;
}


.hero h1 {

    font-size:
        clamp(42px, 6vw, 76px);

    line-height: 1.05;

    letter-spacing: -3px;

    font-weight: 800;

    color: #f8fafc;
}


.hero h1 span {

    background:
        linear-gradient(
            90deg,
            #60a5fa,
            #38bdf8,
            #818cf8
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


.hero p {

    max-width: 680px;

    margin: 24px auto 0;

    font-size: 17px;

    line-height: 1.7;

    color: #94a3b8;
}


/* =========================================================
   HERO CHIPS
   ========================================================= */

.chips {

    display: flex;

    justify-content: center;

    flex-wrap: wrap;

    gap: 10px;

    margin-top: 28px;
}


.chip {

    padding: 7px 13px;

    border-radius: 20px;

    font-size: 12px;

    color: #bfdbfe;

    background:
        rgba(15, 23, 42, 0.7);

    border:
        1px solid rgba(96, 165, 250, 0.15);
}


/* =========================================================
   GLASS CARDS
   ========================================================= */

.card {

    background:
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.82),
            rgba(8, 18, 38, 0.70)
        );

    border:
        1px solid rgba(96, 165, 250, 0.15);

    border-radius: 22px;

    box-shadow:
        0 20px 70px rgba(0, 0, 0, 0.25),

        inset 0 1px 0
        rgba(255,255,255,0.03);

    backdrop-filter:
        blur(20px);

}


/* =========================================================
   WORKSPACE
   ========================================================= */

.workspace {

    display: grid;

    grid-template-columns:
        1.15fr
        0.85fr;

    gap: 20px;

    margin-top: 25px;
}


.card-content {

    padding: 30px;
}


.card-title {

    font-size: 18px;

    font-weight: 700;

    margin-bottom: 8px;

    color: #f8fafc;
}


.card-description {

    color: #64748b;

    font-size: 14px;

    line-height: 1.6;

    margin-bottom: 25px;
}


/* =========================================================
   UPLOAD BOX
   ========================================================= */

.upload-box {

    position: relative;

    min-height: 220px;

    display: flex;

    align-items: center;

    justify-content: center;

    flex-direction: column;

    border-radius: 18px;

    border:
        1px dashed
        rgba(96, 165, 250, 0.35);

    background:
        rgba(15, 23, 42, 0.55);

    transition:
        all 0.3s ease;

    cursor: pointer;
}


.upload-box:hover {

    border-color:
        rgba(96, 165, 250, 0.75);

    background:
        rgba(30, 64, 175, 0.10);

    transform:
        translateY(-2px);

    box-shadow:
        0 0 35px
        rgba(37, 99, 235, 0.10);
}


.upload-icon {

    width: 58px;
    height: 58px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 16px;

    font-size: 25px;

    background:
        rgba(37, 99, 235, 0.15);

    border:
        1px solid
        rgba(96, 165, 250, 0.20);

    margin-bottom: 15px;
}


.upload-title {

    font-size: 15px;

    font-weight: 600;

    color: #dbeafe;
}


.upload-subtitle {

    margin-top: 7px;

    font-size: 12px;

    color: #64748b;
}


/* Hide native input */

#datasetFile {

    position: absolute;

    inset: 0;

    opacity: 0;

    cursor: pointer;
}


/* =========================================================
   BUTTON
   ========================================================= */

.generate-button {

    width: 100%;

    margin-top: 18px;

    padding: 15px 20px;

    border: none;

    border-radius: 13px;

    color: white;

    font-size: 14px;

    font-weight: 700;

    cursor: pointer;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #3b82f6
        );

    box-shadow:
        0 10px 30px
        rgba(37, 99, 235, 0.25);

    transition:
        all 0.25s ease;
}


.generate-button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 15px 40px
        rgba(37, 99, 235, 0.38);
}


.generate-button:active {

    transform:
        translateY(0);
}


/* =========================================================
   ANALYSIS LIST
   ========================================================= */

.analysis-list {

    display: flex;

    flex-direction: column;

    gap: 12px;

    margin-top: 25px;
}


.analysis-item {

    display: flex;

    align-items: center;

    gap: 13px;

    padding: 14px;

    border-radius: 13px;

    background:
        rgba(15, 23, 42, 0.55);

    border:
        1px solid
        rgba(96, 165, 250, 0.08);
}


.check {

    width: 28px;
    height: 28px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 9px;

    background:
        rgba(37, 99, 235, 0.13);

    color: #60a5fa;

    font-size: 13px;
}


.analysis-item span {

    font-size: 13px;

    color: #cbd5e1;
}


/* =========================================================
   OUTPUT
   ========================================================= */

.output-section {

    margin-top: 20px;
}


.output-header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 15px;
}


.output-status {

    font-size: 11px;

    padding: 6px 10px;

    border-radius: 20px;

    color: #86efac;

    background:
        rgba(34, 197, 94, 0.08);

    border:
        1px solid
        rgba(34, 197, 94, 0.12);
}


#output {

    width: 100%;

    min-height: 420px;

    padding: 25px;

    border-radius: 16px;

    border:
        1px solid
        rgba(96, 165, 250, 0.10);

    background:
        #020617;

    color: #cbd5e1;

    font-family:
        "JetBrains Mono",
        Consolas,
        monospace;

    font-size: 13px;

    line-height: 1.75;

    white-space: pre-wrap;

    overflow-x: auto;

    display: none;

    box-shadow:
        inset 0 0 30px
        rgba(37, 99, 235, 0.04);
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    text-align: center;

    margin-top: 45px;

    color: #475569;

    font-size: 12px;

}


.footer span {

    color: #60a5fa;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 850px) {

    .workspace {

        grid-template-columns: 1fr;

    }

    .hero h1 {

        letter-spacing: -2px;

    }

    .hero {

        padding-top: 35px;

    }

}


@media (max-width: 500px) {

    .container {

        width: 94%;

    }

    .navbar {

        padding-bottom: 15px;

    }

    .status {

        display: none;

    }

    .card-content {

        padding: 22px;

    }

}

</style>

</head>


<body>


<div class="container">


    <!-- =====================================================
         NAVBAR
         ===================================================== -->

    <nav class="navbar">

        <div class="logo">

            <div class="logo-icon">
                ✦
            </div>

            <div>
                AI Automation
            </div>

        </div>


        <div class="status">

            <div class="status-dot"></div>

            System Ready

        </div>

    </nav>


    <!-- =====================================================
         HERO
         ===================================================== -->

    <section class="hero">

        <div class="badge">

            ✦ AGENTIC AI &nbsp; • &nbsp; DATA AUTOMATION

        </div>


        <h1>

            Automated Research<br>

            <span>
                Dataset Description Generator
            </span>

        </h1>


        <p>

            Transform raw CSV and Excel datasets into
            structured, research-ready descriptions
            using automated data analysis.

        </p>


        <div class="chips">

            <div class="chip">
                CSV
            </div>

            <div class="chip">
                Excel
            </div>

            <div class="chip">
                Python
            </div>

            <div class="chip">
                Pandas
            </div>

            <div class="chip">
                Automated Analysis
            </div>

        </div>

    </section>


    <!-- =====================================================
         WORKSPACE
         ===================================================== -->

    <section class="workspace">


        <!-- UPLOAD CARD -->

        <div class="card">

            <div class="card-content">

                <div class="card-title">

                    01 · Upload Dataset

                </div>


                <div class="card-description">

                    Select a CSV or Excel dataset
                    to begin automated analysis.

                </div>


                <div class="upload-box">

                    <div class="upload-icon">

                        ↑

                    </div>


                    <div class="upload-title">

                        Drop your dataset here

                    </div>


                    <div class="upload-subtitle">

                        CSV or XLSX · Maximum recommended size 10MB

                    </div>

<input
    type="file"
    id="datasetFile"
    accept=".csv,.xlsx"
    onchange="showSelectedFile(this)"
>
                </div>


                <button
                    class="generate-button"
                    onclick="uploadFile()"
                    id="generateButton"
                >

                    🚀 Generate Research Description

                </button>

            </div>

        </div>


        <!-- ANALYSIS CARD -->

        <div class="card">

            <div class="card-content">

                <div class="card-title">

                    02 · Automated Analysis

                </div>


                <div class="card-description">

                    The system automatically examines
                    important characteristics of your dataset.

                </div>


                <div class="analysis-list">


                    <div class="analysis-item">

                        <div class="check">
                            ✓
                        </div>

                        <span>
                            Dataset structure & dimensions
                        </span>

                    </div>


                    <div class="analysis-item">

                        <div class="check">
                            ✓
                        </div>

                        <span>
                            Column names & data types
                        </span>

                    </div>


                    <div class="analysis-item">

                        <div class="check">
                            ✓
                        </div>

                        <span>
                            Numerical & categorical variables
                        </span>

                    </div>


                    <div class="analysis-item">

                        <div class="check">
                            ✓
                        </div>

                        <span>
                            Missing value detection
                        </span>

                    </div>


                    <div class="analysis-item">

                        <div class="check">
                            ✓
                        </div>

                        <span>
                            Duplicate record detection
                        </span>

                    </div>


                    <div class="analysis-item">

                        <div class="check">
                            ✓
                        </div>

                        <span>
                            Statistical summary
                        </span>

                    </div>


                </div>

            </div>

        </div>

    </section>


    <!-- =====================================================
         OUTPUT
         ===================================================== -->

    <section class="output-section card">

        <div class="card-content">


            <div class="output-header">

                <div>

                    <div class="card-title">

                        03 · Generated Research Description

                    </div>

                    <div class="card-description"
                         style="margin-bottom:0;">

                        Your automated dataset profile
                        will appear below.

                    </div>

                </div>


                <div
                    class="output-status"
                    id="outputStatus"
                >

                    ● READY

                </div>

            </div>


            <pre id="output"></pre>

        </div>

    </section>


    <!-- =====================================================
         FOOTER
         ===================================================== -->

    <footer class="footer">

        Automated Research Dataset Description Generator

        <br>

        Built with
        <span>FastAPI</span>
        ·
        <span>Pandas</span>
        ·
        Python

    </footer>


</div>


<script>

/* =========================================================
   FILE UPLOAD + ANALYSIS
   ========================================================= */
function showSelectedFile(input) {
    if (!input.files || input.files.length === 0) {
        return;
    }

    const file = input.files[0];

    const title = document.querySelector(".upload-title");
    const subtitle = document.querySelector(".upload-subtitle");

    title.innerText = "✓ " + file.name;

    const sizeKB = file.size / 1024;

    subtitle.innerText =
        sizeKB < 1024
            ? sizeKB.toFixed(1) + " KB • Dataset selected"
            : (sizeKB / 1024).toFixed(2) + " MB • Dataset selected";
}
async function uploadFile() {


    const fileInput =
        document.getElementById("datasetFile");


    const outputBlock =
        document.getElementById("output");


    const button =
        document.getElementById("generateButton");


    const status =
        document.getElementById("outputStatus");


    const file =
        fileInput.files[0];


    /* -----------------------------------------------------
       Validate file
       ----------------------------------------------------- */

    if (!file) {

        alert(
            "Please select a CSV or Excel dataset first."
        );

        return;

    }


    /* -----------------------------------------------------
       Prepare UI
       ----------------------------------------------------- */

    outputBlock.style.display = "block";

    outputBlock.innerText =
        "Analyzing your dataset...\\n\\n" +
        "Please wait while the system generates your research description.";


    button.disabled = true;

    button.innerText =
        "⏳ Analyzing Dataset...";


    status.innerText =
        "● ANALYZING";

    status.style.color =
        "#facc15";


    /* -----------------------------------------------------
       Prepare request
       ----------------------------------------------------- */

    const formData =
        new FormData();


    formData.append(
        "file",
        file
    );


    /* -----------------------------------------------------
       Send to FastAPI
       ----------------------------------------------------- */

    try {


        const response =
            await fetch(
                "/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );


        const result =
            await response.text();


        if (!response.ok) {

            throw new Error(
                "Server returned an error."
            );

        }


        /* -------------------------------------------------
           Display result
           ------------------------------------------------- */

        outputBlock.innerText =
            result;


        status.innerText =
            "● ANALYSIS COMPLETE";


        status.style.color =
            "#4ade80";


    }


    catch (error) {


        outputBlock.innerText =
            "Unable to analyze the dataset.\\n\\n" +
            "Please check your file and try again.";


        status.innerText =
            "● ERROR";


        status.style.color =
            "#f87171";

    }


    finally {


        button.disabled =
            false;


        button.innerText =
            "🚀 Generate Research Description";

    }

}

</script>


</body>

</html>

"""


# ============================================================
# ANALYZE ENDPOINT
# ============================================================

@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...)
):

    contents = await file.read()

    description = generate_description_from_bytes(
        contents,
        file.filename
    )

    return HTMLResponse(
        content=description,
        status_code=200
    )