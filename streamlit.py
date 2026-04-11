import streamlit as st
import requests
import pandas as pd
import numpy as np
import time



st.set_page_config(
    page_title="Product Management System",
      page_icon=":factory:", 
      layout="wide",
      initial_sidebar_state="expanded"
      )

st.title("Manufacturing Defect Prediction System")
st.caption("QUALITY CONTROL ML SYSTEM.")

mode= st.sidebar.selectbox(
    "Select Mode",
    ["Manual input", "Real-time Monitoring"]
)

if mode=="Manual input":

    st.sidebar.header("Input Parameters")
    st.sidebar.subheader("Product Information")
    product_type = st.sidebar.selectbox("Product Type", ["Aluminium Plate", "High Strength Steel","Plastic Component"])
    product_sensitivity = st.sidebar.selectbox("Product Sensitivity", ["High", "Medium", "Low"])
    material_quality = st.sidebar.selectbox("Material Quality", ["High", "Medium", "Low"])
    st.sidebar.subheader("Operator")
    operator_skill_level = st.sidebar.selectbox("Operator Skill Level", ["Expert", "Intermediate", "Beginner"])
    st.sidebar.subheader("Machine Parameters")
    temperature = st.sidebar.slider("Temperature (°C)", min_value=10, max_value=500, value=200)
    vibration = st.sidebar.slider("Vibration (mm/s)", min_value=0.2, max_value=100.0, value=0.5)
    pressure = st.sidebar.slider("Pressure (bar)", min_value=1.0, max_value=100.0, value=1.0)
    machine_speed = st.sidebar.slider("Machine Speed (rpm)", min_value=100.0, max_value=2000.0, value=500.0)
    cooling_rate = st.sidebar.slider("Cooling Rate (°C/min)", min_value=0.0, max_value=350.0, value=10.0)
    cycle_time = st.sidebar.slider("Cycle Time (s)", min_value=5.0, max_value=300.0, value=60.0)
    tool_wear = st.sidebar.slider("Tool Wear (mm)", min_value=0.0, max_value=400.0, value=1.0)
    stress_index = st.sidebar.slider("Stress Index", min_value=1.0, max_value=100.0, value=0.5)

    run=st.sidebar.button("Predict Defect")
    if run:
        data={
            "product_type":product_type,
            "product_sensitivity":product_sensitivity,
            "material_quality":material_quality,
            "operator_skill_level":operator_skill_level,
            "temperature":temperature,
            "vibration":vibration,
            "pressure":pressure,
            "machine_speed":machine_speed,
            "cooling_rate":cooling_rate,
            "cycle_time":cycle_time,
            "tool_wear":tool_wear,
            "stress_index":stress_index
        }
        url=st.secrets["API_URL"]
        try:
            response=requests.post(url,json=data)
            if response.status_code==200:
                result=response.json()
    
        
                if isinstance(result, list):
                    result=result[0]
                def to_float(val):
                    try:
                        return float(val)
                    except (ValueError, TypeError):
                        return 0.0
                prob=to_float(result.get("defect_proba"))
                quality=to_float(result.get("quality"))
                score=to_float(result.get("final_score"))

                st.divider()

                st.metric("Anomaly:",result.get("anomaly_binary"))
                st.metric("Type of Defect:",result.get("defect_type"))

                st.divider()

                col2,col3,col4=st.columns(3)
            
                col2.metric("Defect Probability", f"{prob:.2f}")
                col3.metric("Product Quality", f"{quality:.2f}")
                col4.metric("System Risk Score", f"{score:.2f}")

                st.divider()

                st.subheader("Decision Engine Output")

                st.markdown(f"#### Product Decision: {result.get('product_decision')}")
                st.markdown(f"#### Machine Decision: {result.get('machine_decision')}")
                st.markdown(f"#### Final Decision: {result.get('final_decision')}")

                st.divider()
                if result.get("anomaly_binary")=="ANOMALY DETECTED":
                    st.error("Anomaly Detected! Please check machine immediately.")
                else:
                    st.success("No Anomaly Detected. Machine is stable.")
                history= np.clip(np.random.normal(score, scale=0.1, size=20), 0, 1)
                df=pd.DataFrame({
                    "timestamp":pd.date_range(start="2024-01-01", periods=20, freq="H"),
                    "risk_score":history
                })
                g1, g2 = st.columns(2)
                with g1:
                    st.subheader("Risk Score Trend")
                    st.line_chart(df.set_index("timestamp")["risk_score"])
                with g2:
                    st.subheader("Current Parameter Values")
                    data_frame={
                        "Parameter":["Temperature","Vibration","Pressure","Machine Speed","Cooling Rate","Cycle Time","Tool Wear","Stress Index"],
                        "Value":[temperature/500,vibration/100.0,pressure/100.0,machine_speed/2000.0,cooling_rate/350.0,cycle_time/300.0,tool_wear/400.0,stress_index/100.0]
                    }
                    df=pd.DataFrame(data_frame)
                    st.bar_chart(df.set_index("Parameter"))

        
        except Exception as e:
            st.error(f"Error during prediction: {e}")

elif mode=="Real-time Monitoring":
    import time
    st.title("Real-time Monitoring")
    st.info("This mode will automatically fetch the latest predictions from the system every 10 seconds.")
    placeholder=st.empty()
    while True:
        try:
            df=pd.read_csv(r"C:\Users\user\Desktop\Product_Management_system\predictions.csv")
            df=df.apply(pd.to_numeric, errors='ignore')
            latest=df.iloc[-1]
            with placeholder.container():
                st.subheader("Latest Prediction")
                st.dataframe(df.tail(1))
                st.metric("Latest Anomaly:",latest.get("anomaly_binary"))
                st.metric("Latest Defect Type:",latest.get("defect_type"))
                col1, col2, col3 = st.columns(3)
                col1.metric("Latest Defect Probability", f"{float(latest.get('defect_proba', 0.0)):.2f}")
                col2.metric("Latest Product Quality", f"{float(latest.get('quality', 0.0)):.2f}")
                col3.metric("Latest System Risk Score", f"{float(latest.get('final_score', 0.0)):.2f}")
                st.divider()
                st.subheader("Latest Decision Engine Output")
                st.markdown(f"##### Latest Product Decision: {latest.get('product_decision')}")
                st.markdown(f"##### Latest Machine Decision: {latest.get('machine_decision')}")
                st.markdown(f"##### Latest Final Decision: {latest.get('final_decision')}")
                param_data={
                    "Parameter":[
                        "operator_skill_level",
                        "product_type",
                        "product_sensitivity",
                        "material_quality",
                        "Temperature",
                        "Vibration",
                        "Pressure",
                        "Machine Speed",
                        "Cooling Rate",
                        "Cycle Time",
                        "Tool Wear",
                        "Stress Index"
                    ],
                    "Value":[
                        str(latest.get("operator_skill_level","N/A")),
                        str(latest.get("product_type","N/A")),
                        str(latest.get("product_sensitivity","N/A")),
                        str(latest.get("material_quality","N/A")),
                        str(latest.get("temperature", 0.0)),
                        str(latest.get("vibration", 0.0)),
                        str(latest.get("pressure", 0.0)),
                        str(latest.get("machine_speed", 0.0)),
                        str(latest.get("cooling_rate", 0.0)),
                        str(latest.get("cycle_time", 0.0)),
                        str(latest.get("tool_wear", 0.0)),
                        str(latest.get("stress_index", 0.0))
                    ]
                }
                df_params=pd.DataFrame(param_data)
                numeric_params=df_params[df_params["Parameter"].isin([
                    "Temperature",
                    "Vibration",
                    "Pressure",
                    "Machine Speed",
                    "Cooling Rate",
                    "Cycle Time",
                    "Tool Wear",
                    "Stress Index"])]
                numeric_params=numeric_params.copy()
                numeric_params["Value"]=pd.to_numeric(numeric_params["Value"], errors='coerce').fillna(0)
                col1, col2 = st.columns(2)
                with col1:
                    st.bar_chart(
                        numeric_params.set_index("Parameter")["Value"])
                with col2:
                    st.table(df_params.set_index("Parameter"))
        except Exception as e:
            st.error(f"Error fetching real-time data: {e}")
        time.sleep(10)
st.caption("Built by Justus Omari Kwache| Powered by FastAPI | Deployed on Render & Streamlit")
        
    