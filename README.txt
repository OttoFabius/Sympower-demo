This repository is to demo a potential product that enables greenhouse gas owners to operate electric boilers as additional cost-effective source of heat.

The resulting demo can be viewed on electric-greenhouse-heating.streamlit.app. To make and view changes, please run the demo locally.


TO RUN LOCALLY

1. clone this repository (git@github.com:OttoFabius/Sympower-demo.git)

2. install the following dependencies:

	pip install streamlit
	pip install numpy, pandas

3. add the file with the day ahead forecasts to the repository folder 
(dayaheadprices-FI data 2023.xlsx - result.csv)

4. from the command line, navigate to the repository folder and run streamlit:

	streamlit run run_streamlit.py

streamlit will open in a browser tab and any changes to the code will be visible in the resulting app.	