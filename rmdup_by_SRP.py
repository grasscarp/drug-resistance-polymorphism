#!/usr/bin/env python
# coding: utf-8

# In[2]:


####### This is a script for removing duplications by checking single-resistance polymorphism (SRP) #######
import pandas as pd
import numpy as np

#input
path_in = 'E:/OneDrive - BGI Tech Solutions (Hongkong) Co., Ltd/病原组学研究所/项目组事务/湘雅KP/总表.xlsx'
path_out = 'E:/OneDrive - BGI Tech Solutions (Hongkong) Co., Ltd/病原组学研究所/项目组事务/湘雅KP/总表rmdup.xlsx'
start_col = 15  # No. of the first drug resistance col - 1
end_col = 47  # No. of the last drug resistance col

df = pd.read_excel(path_in)


# In[11]:


#replace(I as R)
temp = df[df.columns[:end_col]].copy()
df2 = temp.fillna('U').replace(['ND','unclear','unknown','I','SDD'], ['U','U','U','R','R'])


# In[13]:


#combine strs, count the U-Number, sort and select the ref
df2["newColumn"] = ""
mlist=df2.columns[start_col:end_col]
for i in mlist:
    df2["newColumn"] += df2[i].map(str)

U_Num=[]
for i in df2.index:
    U_Num.append(df2.loc[i,"newColumn"].count("U"))
df2["U_Num"]=U_Num

df2=df2.sort_values(['U_Num','Date'])
temp=df2.iloc[0]
ref_id=temp['Patient ID']
ref=temp.newColumn

#drop total duplicates by patient ID
df3=df2[["NEWid","Patient ID","newColumn"]]
df4=df3.drop_duplicates(subset=["Patient ID","newColumn"],keep='first')
newid = df4["NEWid"].tolist()
oldid = df3["NEWid"].tolist()
duplicatesID = [x for x in oldid if x not in newid]
print('totally same: ',len(duplicatesID))


# In[16]:


#patient ID with more than 1 samples in different resistance
duplist=pd.DataFrame(df4["Patient ID"].value_counts())
duplist=duplist[duplist["Patient ID"] > 1]
df5=df4[df4['Patient ID'].isin(duplist.index)].copy()

#call SNP 
drugSNP=[]
for i in df5.index:
    SNP=''
    temp=df5.loc[i,'newColumn']
    for j in range(len(temp)):
        if ref[j]==temp[j] or temp[j]=='U':
            SNP+='-'
        else:
            SNP+=temp[j]
    drugSNP.append(SNP)
df5['drugSNP']=drugSNP


# In[17]:


#drop partly duplicates by patient ID
df6=df5.drop_duplicates(subset=["Patient ID","drugSNP"],keep='first')
oldid=df5.NEWid.tolist()
newid=df6.NEWid.tolist()
duplicatesID += [i for i in oldid if i not in newid]

if ref_id in duplist.index:
    temp=df6[df6['Patient ID']==ref_id].copy()
    
    Uloc=[i for i,x in enumerate(ref) if x=='U']
    drugSNP_del=[]
    for SNP in temp.drugSNP:
        l=list(SNP)
        for i in Uloc:
            l[i]='*'
        drugSNP_del.append(''.join([i for i in l if i!='*']))
    temp['drugSNP_del']=drugSNP_del
    
    oldid=temp.NEWid.tolist()
    newid=temp.drop_duplicates(subset=["Patient ID","drugSNP_del"],keep='first').NEWid.tolist()
    duplicatesID += [i for i in oldid if i not in newid]

print('totally same & partly same: ',len(duplicatesID))


# In[146]:


#output
df[~df.NEWid.isin(duplicatesID)].to_excel(path_out,index=False)

