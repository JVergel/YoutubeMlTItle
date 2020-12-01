#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import numpy as np
from tensorflow.keras.models import Sequential


# In[2]:


Titulos = open("sample.txt", "r")
Texto= Titulos.read()
TextoS=Texto.split("\n")


# In[3]:


TextoS


# In[4]:


tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(TextoS)
word_index= tokenizer.word_index



# In[5]:


total_words=len(tokenizer.word_index)+1


# In[6]:


inputSequences=[]
for line in TextoS:
    tokenList=tokenizer.texts_to_sequences([line])[0]
    for i in range(1,len(tokenList)):
        nGramSequence= tokenList[:i+1]
        inputSequences.append(nGramSequence)


# In[7]:


maxSequenceLen = max([len(x)for x in inputSequences])
inputSequences= np.array(pad_sequences(inputSequences,maxlen=maxSequenceLen,padding='pre'))


# In[8]:


xs= inputSequences[:,:-1]
labels= inputSequences[:,-1]


# In[9]:


ys= tf.keras.utils.to_categorical(labels,num_classes=total_words)


# In[28]:


model= tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(total_words,480,input_length=maxSequenceLen-1))
model.add(tf.keras.layers.LSTM(150))
model.add(tf.keras.layers.Dense(total_words, activation='softmax'))
adam= tf.keras.optimizers.Adam(lr=0.01)
model.compile(loss='categorical_crossentropy',optimizer=adam,metrics=['accuracy'])


# In[29]:


history= model.fit(xs,ys,epochs=70,verbose=1)


# In[33]:


seedText= " most"
nextWords=15


for _ in range(nextWords):
    tokenList = tokenizer.texts_to_sequences([seedText])[0]
    tokenList= pad_sequences([tokenList],maxlen=maxSequenceLen-1,padding='pre')
    predicted= model.predict_classes(tokenList,verbose=0)
    outpudWord=""
    for word, index in tokenizer.word_index.items():
        if index== predicted:
            outpudWord= word
            break
    seedText+= " "+ outpudWord
print(seedText)


# In[ ]:





# In[ ]:




