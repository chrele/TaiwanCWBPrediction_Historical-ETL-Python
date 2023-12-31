# Taiwan CWB Prediction and Historical ETL Python

This project is part of the base pipelines on Renewable Energy research I have done during my master.

## Background
Taiwan Central Weather Beureau (CWB) provide a 3-hourly prediction data based on their current sensors reading. However, they just experimenting with this prediction data and not really storing the data. The only way to get them is via their API.

I was working on a Deep Learning algorithm to produce a short-time Wind Speed prediction. The CWB's prediction data is used as one of the variables or attributes of the prediction model. Since the data saved is needed for analysis purposes, the final form of the data is ```.CSV``` files

## How to Run
1. ```git clone``` this repository or download it as zip. (Recommended) Fork this repository, then clone it from your own github.
2. Download [PYTHON](https://www.python.org/downloads/windows/) and install it on your PC.
3. Open the folder on your IDE. (Recommended) Download [Visual Studio Code](https://code.visualstudio.com/).
4. Run ```pip install requirement.txt``` to automatically install any necessary package from Python.
5. Open ```CWBPredictionETL.py``` and insert your API key on ```API_KEY``` variable.
6. Run the program by executing ```python CWBPredictionETL.py``` on CMD/Terminal. The program will extract the data from CWB's official API.
7. You can modify the dataSource list by selecting your needed data from [CWB's API Documentation](https://opendata.cwb.gov.tw/dist/opendata-swagger.html)
8. You can also customize the city as needed too! Make sure to check the available cities~
9. The program will load the transformed data with ```.csv``` extension on ```./outputs/``` folder.