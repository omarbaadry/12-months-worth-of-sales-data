import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

#12 monthes in single csv 
files=[file for file in os.listdir('C:/Users/win10/Desktop/Sales_Data')]
all_months_data=pd.DataFrame()
for file in files:
    data=pd.read_csv("C:/Users/win10/Desktop/Sales_Data/"+file)
    all_months_data=pd.concat([all_months_data,data])
all_months_data.to_csv("all_data.csv",index=False)

all_data=pd.read_csv("C:/Users/win10/Desktop/all_data.csv")
print(all_data.head())

#Clean up Data
#drop NAN Values
NAN_df=all_data[all_data.isna().any(axis=1)]
all_data=all_data.dropna(how='all')

#Delte duplicated headers
all_data=all_data[all_data['Order Date'].str[0:2] != 'Or']

#convert Col to Correct type
all_data['Quantity Ordered']=all_data['Quantity Ordered'].astype(int)
all_data['Price Each']=all_data['Price Each'].astype(float)
#Order Date DateTime Format
#all_data['Order Date']= pd.to_datetime(all_data['Order Date'])
#all_data['Hour']=all_data['Order Date'].dt.hour
#all_data['Minute']=all_data['Order Date'].dt.minute

#Add Col
#Add Month Col
all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=all_data['Month'].astype('int32')


#add Sales Col
all_data['sales']=all_data['Quantity Ordered'] * all_data['Price Each']


#Add City Col
all_data['City']=all_data['Purchase Address'].apply(lambda x : x.split(',')[1]) +' '+ all_data['Purchase Address'].apply(lambda x : x.split(',')[2].split(' ')[1])



# Best Month for sales, How much was earned that Month #
results=all_data.groupby('Month').sum()
Months = range(1,13)
plt.bar(Months,results['sales'])
plt.ylabel('Sales')
plt.xlabel('Months')
plt.show()

# City of Highest number of sales #
results=all_data.groupby('City').sum()
Cities = [city for city, data in all_data.groupby('City')]
plt.bar(Cities,results['sales'])
plt.xticks(Cities,rotation= 'vertical', size=8)
plt.ylabel('Sales')
plt.xlabel('Cities')
plt.show()


# Products sold the most and why #

product_group = all_data.groupby('Product')
quantity_ordered=product_group.sum()['Quantity Ordered']
products=[product for product, datafr in product_group]

plt.bar(products, quantity_ordered)
plt.ylabel('# Orders')
plt.xticks(products, rotation='vertical', size=8)
plt.show()


prices= all_data.groupby('Product').mean()['Price Each']
fig, ax1=plt.subplots()
ax2=ax1.twinx()
ax1.bar(products,quantity_ordered,color='g')
ax2.plot(products,prices,'b-')
ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered',color='g')
ax2.set_ylabel('price($)',color='b')
plt.show()
# Products most often sold together #
datafr=all_data[all_data['Order ID'].duplicated(keep=False)]
datafr['Grouped']=datafr.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
datafr=datafr[['Order ID','Grouped']].drop_duplicates()

count=Counter()
for row in datafr['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))
for key,value in count.most_common(10):
    print(key,value)

