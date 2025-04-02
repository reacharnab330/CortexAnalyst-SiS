# CortexAnalyst-SiS

This is a Streamlit in Snowflake (SiS) based AI chatbot powered by Cortex Analyst. This chatbot hosted within SiS and uses validated_ev_data table from the implementation given in the following repo : https://github.com/reacharnab330/EVPopulation-Snowflake

# High level data flow

<img src="https://github.com/reacharnab330/CortexAnalyst-SiS/blob/main/data-flow.PNG">

User Input: User types a question in the Streamlit chat interface (e.g., "How many EVs were registered in 2023?")  
Prompt Processing: process_message sends the prompt to send_message  
Cortex Analyst API Call: send_message invokes the Cortex Analyst API, passing the prompt and semantic model  
SQL Generation: Cortex Analyst uses the YAML to map the prompt to the underlying table and generates an SQL query (e.g., SELECT COUNT(*) FROM ev_registration_details WHERE model_year = '2023')  
SQL Execution: In display_content, the generated SQL is executed via session.sql(), querying the table in Snowflake  
Results Display: The results are returned and displayed in Streamlit  

# Project overview

The script abstracts the table reference into the semantic model, which is a deliberate design choice.  
Cortex Analyst Abstraction: The API handles translating natural language to SQL, so the Python code doesn’t need to know the table name directly. This results into the following advantages :
  1. Flexibility: Changing the table only requires updating the YAML, not the code.
  2. Reusability: The same script can work with different datasets by swapping the semantic model file.

# How to use this project

Prerequisite : Ensure validated_ev_data is present ( as part of https://github.com/reacharnab330/EVPopulation-Snowflake)  

1. Clone this repo
2. Set up the Streamlit in Snowflake (SiS) app using the code in ev_registration_cortex_chat_app.py
3. Place the yaml file in stage and ensure accessibility from the Streamlit app
4. Run the SiS app
