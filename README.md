# Emotional_AI_Chatbot

## NLP Word Embedding used - Follow the Steps
- Download glove.6B.50d.txt from "https://www.kaggle.com/watts2/glove6b50dtxt"
- Place in the folder where you are performing NLP training

## Kaggle Dataset testing
- Download the Dataset from "https://www.kaggle.com/datasets/parulpandey/emotion-dataset"
- Run the python script "kaggleskip.py". It achieved an accuracy around 35% using LSTM and skip connections
<img width="886" height="500" alt="lstm_cell" src="https://user-images.githubusercontent.com/16485542/167322294-7699c946-d297-4b55-a026-f1e913c8eb1c.png">

## No Context Datasets vs Labelled Context Datasets

## No Context Datasets - Training
### NN1.ipynb in the folder FirstNeuralNetwork:

Contains all the code used to train and test different models for the first part of the project focused on training without any consistent context. In its current form, this is meant to be run in Google Colab. It requires downloading the csv files from the same folder and saving them to your Google Drive. If you want to utilize the same directory and file names as I did, you should name and place folders to match what is in the notebook. For example:

'/content/drive/MyDrive/Emotional_AI_Chatbot/RealTrainData.csv'

'/content/drive/MyDrive/Emotional_AI_Chatbot/RealTestData.csv'

'/content/drive/MyDrive/Emotional_AI_Chatbot/glove.6B.50d.txt' (See section above, titled "NLP Word Embedding used - Follow the Steps")

If your file locations do not match, you will have to change the references to file locations in the code.

### Emotional_AI_Chatbot/FirstNeuralNetwork/plots/

Folder containing plots of the training and validation loss and accuracy for the first neural network, trained on the No Context Dataset.

### csv files

RealTrainData.csv - file with 170 sentences with emotion labels for training

RealTestData.csv - file with 30 sentences with emotion labels for testing

hyp_search.csv - file with the details and results of the hyperparameter search conducted

TrainDataTrim.csv - file with 200 sentences with emotion labels, trimmed to get RealTrainData.csv and RealTestData.csv 

## Labelled Context Datasets - Training
- Goto "LabelledContextTraining" folder. In this folder, the training happens on only the "Labelled Context Datasets"
- Run "mainSecondatch2.py". In this, training is Context/Theme dependent.
-- Training happens on "TrainDTS.csv"
<img width="886" height="500" alt="lstm_cell" src="https://user-images.githubusercontent.com/16485542/167322865-c1646cdf-1629-46f0-a36d-ec49c901f282.png">

- Run "skipconnSecondatch2.py". In this, training is Context/Theme dependent
-- Training happens on "TrainDTS.csv"
<img width="886" height="500" alt="lstm_cell" src="https://user-images.githubusercontent.com/16485542/167322909-b88aff9c-60bc-4e43-816d-858517a68c78.png">

- Run "CustomSecondatch2.py". In this, training is Context/Theme in-dependent
-- Training happens on "TrainDTSil.csv"
<img width="886" height="500" alt="lstm_cell" src="https://user-images.githubusercontent.com/16485542/167322979-21894d9a-21ee-4997-b166-eff1497e6b6d.png">

- Run "CustomIncludeLabels.py". In this, training is Context/Theme in-dependent
-- Training happens on "TrainDTS.csv"
<img width="886" height="500" alt="lstm_cell" src="https://user-images.githubusercontent.com/16485542/167322931-6ba744e4-3308-4371-97e9-dac3da32118a.png">


### Relevant Repository to Check out
https://github.com/omerbsezer/LSTM_RNN_Tutorials_with_Demo


