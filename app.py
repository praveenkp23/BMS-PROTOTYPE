"""
BMS — Bone & Implant Measurement System (educational prototype)
Run: streamlit run app.py

IMPORTANT:
- This is a prototype for demonstration and education only.
- It is NOT validated for clinical use and must not be used to choose implants
  or guide patient care.
- Fluoroscopy calibration is sensitive to marker depth, projection geometry,
  distortion, image quality, and endpoint selection.
"""

import io
import json
from datetime import datetime

import streamlit as st
from PIL import Image

st.set_page_config(page_title="BMS | Bone & Implant Measurement System",
                   page_icon="🦴", layout="wide")

st.title("🦴 BMS — Bone & Implant Measurement System")
st.caption("AI-assisted bone measurement and preoperative implant-planning support • Prototype")

st.warning(
    "Demonstration prototype only — not clinically validated. "
    "Do not use these results to select an implant or make treatment decisions. "
    "All measurements require review by a qualified clinician."
)

with st.sidebar:
    st.header("Case information")
    case_id = st.text_input("Case / demo ID", value="DEMO-001")
    modality = st.selectbox("Image type", ["Fluoroscopy / X-ray", "CT / DICOM", "Other image"])
    reviewer = st.text_input("Reviewer (optional)")
    st.divider()
    st.markdown("**Workflow**")
    st.markdown("1. Upload image")
    st.markdown("2. Calibrate scale")
    st.markdown("3. Enter measured pixel spans")
    st.markdown("4. Review and export report")

uploaded = st.file_uploader(
    "Upload a de-identified medical image (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"],
    help="For this prototype, use a de-identified image. DICOM support is not implemented in this basic version."
)

image_name = None
if uploaded:
    image_name = uploaded.name
    try:
        img = Image.open(uploaded).convert("RGB")
        col1, col2 = st.columns([1.3, 1])
        with col1:
            st.subheader("Image preview")
            st.image(img, caption=image_name, use_container_width=True)
            st.caption(f"Image dimensions: {img.width} × {img.height} pixels")
        with col2:
            st.subheader("1. Calibration")
            st.write("Enter the known physical length and its measured span in the image.")
            known_mm = st.number_input("Known marker length (mm)", min_value=0.1, value=25.0, step=0.5)
            marker_px = st.number_input("Marker span (pixels)", min_value=0.1, value=100.0, step=1.0)
            mm_per_px = known_mm / marker_px if marker_px > 0 else 0
            st.metric("Calculated scale", f"{mm_per_px:.5f} mm/pixel")
            st.caption(
                "Use a marker close to the anatomy and at a similar depth. "
                "This simple scale does not correct for perspective, distortion, or depth differences."
            )
    except Exception as e:
        st.error(f"Could not read the uploaded image: {e}")
        img = None
else:
    img = None
    st.info("Upload an image to begin. Do not upload identifiable patient information.")

st.divider()
st.subheader("2. Measurement entries")
st.write(
    "This version uses manually entered pixel spans. It does not automatically segment bones "
    "or identify anatomical landmarks."
)

if uploaded and img is not None:
    known_mm = st.session_state.get("known_mm", 25.0) if False else None
    # Re-read widgets' current values from session state, with safe defaults.
    known_mm = float(st.session_state.get("Known marker length (mm)", 25.0))
    marker_px = float(st.session_state.get("Marker span (pixels)", 100.0))
    scale = known_mm / marker_px if marker_px > 0 else 0.0
else:
    scale = 0.0

measurement_rows = []
if scale > 0:
    st.caption(f"Current scale: **{scale:.5f} mm/pixel**")
    labels = ["Bone length / span", "Bone width", "Other dimension"]
    cols = st.columns(3)
    for i, label in enumerate(labels):
        with cols[i]:
            px = st.number_input(f"{label} (pixels)", min_value=0.0, value=0.0, step=1.0, key=f"px_{i}")
            mm = px * scale
            st.metric(f"{label} estimate", f"{mm:.2f} mm" if px > 0 else "—")
            if px > 0:
                measurement_rows.append({"measurement": label, "pixels": px, "estimated_mm": round(mm, 3)})
else:
    st.info("Upload an image and enter a valid calibration to calculate estimated dimensions.")

st.divider()
st.subheader("3. Planning notes (clinician review only)")
fracture_region = st.text_input("Region / fracture context (optional)", placeholder="e.g., demo entry only")
notes = st.text_area(
    "Review notes",
    placeholder="Record assumptions, image quality, calibration source, and items requiring clinician verification."
)
st.markdown(
    "**Planning reminder:** implant sizing depends on the full anatomy, fracture pattern, fixation strategy, "
    "verified manufacturer catalogue data, and clinician judgement. This prototype does not recommend an implant."
)

report = {
    "system": "BMS — Bone & Implant Measurement System",
    "prototype_notice": "Educational demonstration only; not validated for clinical use.",
    "generated_at": datetime.now().isoformat(timespec="seconds"),
    "case_id": case_id,
    "modality": modality,
    "image_filename": image_name,
    "image_dimensions_px": (
        {"width": img.width, "height": img.height} if img is not None else None
    ),
    "calibration": {
        "method": "manual known-length marker",
        "known_marker_length_mm": round(float(st.session_state.get("Known marker length (mm)", 25.0)), 4),
        "marker_span_px": round(float(st.session_state.get("Marker span (pixels)", 100.0)), 4),
        "scale_mm_per_px": round(scale, 8) if scale > 0 else None,
        "limitations": "Does not correct for perspective, distortion, or marker/anatomy depth mismatch."
    },
    "measurements": measurement_rows,
    "region_or_fracture_context": fracture_region,
    "reviewer": reviewer,
    "review_notes": notes,
    "clinical_use": "Not for clinical use or autonomous implant selection."
}

col_a, col_b = st.columns(2)
with col_a:
    if st.button("Prepare report preview", type="primary"):
        st.session_state["show_report"] = True
with col_b:
    json_bytes = json.dumps(report, indent=2).encode("utf-8")
    st.download_button(
        "Download report (JSON)",
        data=json_bytes,
        file_name=f"bms_report_{case_id.replace(' ', '_')}.json",
        mime="application/json"
    )

if st.session_state.get("show_report"):
    st.subheader("Report preview")
    st.json(report)

st.divider()
st.caption(
    "BMS prototype • Manual measurements only • No AI segmentation, DICOM geometry validation, "
    "implant catalogue integration, or clinical validation is included."
)
