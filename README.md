# Code sample

## This project is to preprocess data for the regression in the working paper: Economic Impact of Transportation Infrastructure Investment under the Belt Road Initiative  (Chen & Li, 2021).

We estimate the elasticity of trade cost using regression analysis. The elasticity of trade cost change as a response to transportation infrastructure investment is estimated through the following regression mode:

$$
\begin{align*} \mathrm{ln}\tau_{i,j,t}=&\beta_0 +\beta_1 \mathrm{ln}pGDP_{i,t} +\beta_2 \mathrm{ln}pGDP_{j,t}+\beta_3 \mathrm{ln}tar_{i,t} +\beta_4 \mathrm{ln}tar_{j,t}+\beta_5 \mathrm{ln}INF_{i,t}\\ & +\beta_6 \mathrm{ln}INF_{j,t}+\beta_7 FTA_{ij} +\epsilon _{i,j,t} 
\end{align*}
$$

where $i$ and $j $ represent region $i$ and $j$, and $t$ denotes the time period. In the regression model, $\tau_{i,j,t}$ denotes the trade cost between region $j$ and region $i $ in year $t$, which is expressed in a tariff-equivalent form (share of CIF prices),  $\mathrm{ln}pGDP_{i,t}$ represents the logged GDP per capita of the country in region $i$, $tar_{i,t}$ denotes tariff in region $i$, and $INF_{i,t}$ represents the value of infrastructure investment. The elasticity of trade cost with respect to transportation infrastructure investment in country $i$ (country $j$) is denoted as $\beta_5$  ($\beta_6$). $FTA_{ij}$ is a dummy variable which equals one if the two countries are in the same free trade area, otherwise $FTA_{ij}$ was equal to zero. 

The trade cost data were collected from the World Bank UNESCAP Trade Costs Database. Other variables, such as GDP, population,  and tariff were collected from the World Bank Open Data Website. The data of transportation infrastructure investment were obtained from both the World Bank Open Data and OECD. 

1. readExcel.py includes functions for reading excel files. 

  To balance the speed and the performance of the packages, I use xlrd, xlwt, and openpyxl to read and save excel files.

  What's more, I try to use multi-processing to speed up the processing in reading data from .xlsx files, since I need to deal with millions of data at one time.

2. readDTA.py includes functions for state data file, .dta.

3. SQLFunction includes functions for MySQL.

  Since I have to deal with millions of data, I base my database on MySQL5.8 to speed up the preprocessing. The structure of the database is as followed.

![Untitled Diagram](https://github.com/judylxm/wp_BRIinv/blob/main/Untitled%20Diagram.png)

4. readExcelToSQL.py,readExcelToSQL2.py and readExcelToSQL3.py are the main functions that reading data from excel to SQL.
5. readCapitalInfoToDB.py is to input every capital's GPS location into the database. I use the pycountry_convert package for geoinformation.

6. findFTA.py is the main function to locate free trade agreements between countries in the world bank database.
7. AEI_Sum.py is the pretreatment of excel data.
8. select&create_temple.sql is a code example for searching in SQL.
9. I use cloud computing to deploy my database. begin.sh is the file to start the cloud computer.
