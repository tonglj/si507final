# Project Submission Doc

## Project Code
Link: https://github.com/tonglj/si507final
Instruction:
Run the python file, and grab the url displayed in the console panel, which should look like http://127.0.0.1:8050/. There are four parts to this web. The first part is an interactive pie chart that displays the number of players who made into the world ranking list by country (top 10 country only). You can use the dropdown menu to select either to display man single or woman single players. The second part is a searching program that allows you to use the dropdown menu to select a player’s name abbreviation and see his or her personal information. The third part is a static bar chart that displays the number of players who made into the world ranking (single player) by gender. The last scatter plot displays the age spread of the players who made into the world ranking list (single player). You can use the drop down menu to display age spread by gender.
Required Packages:
Dash, plotly, pandas, collections

## Data Source
Source URL and documentation:
https://developer.sportradar.com/docs/read/baseline_sports_coverage/Badminton_v2#badminton-api-overview
Format: json
Description:
I signed up an account at sportradar and requested an personal API token in order to access the data I need. And I used caching for it.
Summary of data:
Available: approximately more 2000 records
Retrieved: about 1000 records after processing
The original json file contains three sections: man-single, woman-single, and men-double. Each section is sorted by ranking number and contains ranking, points, name. name abbreviation, data of birth, country, country abbreviation, and id. All these fields are very straightforward.

## Data Structure
Trees
The class Node is defined in the si507final.py.
Screenshot of the class:
![image](https://user-images.githubusercontent.com/113567689/207674759-0229d80b-ceba-4e12-bae7-98efda60f473.png)
Screenshot of the structure:
![image](https://user-images.githubusercontent.com/113567689/207674831-8b2fbf27-e05c-4ebb-b182-a3b413c4e56d.png)

## Interaction and Presentation Options
There are four parts to this web. The first part is an interactive pie chart that displays the number of players who made into the world ranking list by country (top 10 country only). You can use the dropdown menu to select either to display man single or woman single players. The second part is a searching program that allows you to use the dropdown menu to select a player’s name abbreviation and see his or her personal information. The third part is a static bar chart that displays the number of players who made into the world ranking (single player) by gender. The last scatter plot displays the age spread of the players who made into the world ranking list (single player). You can use the drop-down menu to display age spread by gender.
Technology used: Plotyl, Dash

## Video Demo Link
https://vimeo.com/781203371
