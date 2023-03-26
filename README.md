# Parstep
Python based GUI to help identify data points from a data set consisting of step-like increments or decrements. Especially useful for analysing data of measurements in eperimental setups that yield different average values at different times. For example,

<img src = https://user-images.githubusercontent.com/90126164/227775595-101dc4a7-e120-4cf1-87e4-d5854fcb026e.png width ="400" height = "200">
# Dependencies
`python3`,`matplotlib`,`scipy`,`numpy`. `pandas`

# Usage

The above script can be used to analyse and choose the required data points. The data must be stored in a `.txt` file in the following format:

t \t data1  \
1 \t a1  \
2 \t a2  \
3 \t a3  

Use the following command to analyse the code:

`python3 Parstepy.py <filename>.txt`

<img src = https://user-images.githubusercontent.com/90126164/227777081-e079a5f9-8999-4e98-ae22-d10ca029b345.png width = "700" height = "350">

The red dots indicate the detected points for a given data width. Change the parameters "Height" and "Distance" using the sliders to improve the selection and save button to save the average of each detected data windows to an `.xlsx` file in CWD.


