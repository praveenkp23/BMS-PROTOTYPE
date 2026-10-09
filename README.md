# BMS — Bone & Implant Measurement System (Prototype)

This is a small educational/demo web app based on the BMS presentation.

## Features
- Upload and preview a de-identified PNG/JPG/JPEG image
- Calibrate a pixel scale using a known-length marker
- Convert manually entered pixel spans into estimated millimetres
- Add review notes and export a JSON report

## Not included
- Automated AI bone segmentation or landmark detection
- DICOM metadata / CT voxel geometry support
- Implant selection or manufacturer catalogue integration
- Clinical validation, privacy/security hardening, or regulatory approval

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create/activate a virtual environment (recommended).
4. Install dependencies:
   `pip install -r requirements.txt`
5. Start the app:
   `streamlit run app.py`
6. Open the local address printed by Streamlit in your browser.

## Safety
This is a demonstration prototype only. Do not use it for patient care, surgical planning,
or implant selection. Fluoroscopy scale calibration can be inaccurate because of projection
geometry, distortion, and differences between marker depth and anatomy depth. Any future clinical
version needs expert validation, appropriate data protection, usability testing, and regulatory review.
