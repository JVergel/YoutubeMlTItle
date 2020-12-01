#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


# In[2]:


CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


# In[3]:


client = get_authenticated_service()


# In[4]:


def youtube_keyword(client, **kwargs):    
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.search().list(
        **kwargs
        ).execute()    
    return response


# In[5]:


def youtube_keyword(client, **kwargs):    
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.search().list(
        **kwargs
        ).execute()    
    return response


# In[8]:





# In[6]:


def youtube_search (criteria,max_res):   
    #create lists and empty dataframe
    titles = []
    videoIds = []
    channelIds = []
    resp_df = pd.DataFrame()
    
    while len(titles) < max_res:
        token = None
        response = youtube_keyword(client,
                        part='id,snippet',
                        maxResults=50,
                        q=criteria,
                        videoCaption='closedCaption',
                        type='video', 
                        videoDuration='long',
                        pageToken=token) 
                                         
        for item in response['items']:        
            titles.append(item['snippet']['title'])
            channelIds.append(item['snippet']['channelTitle'])
            videoIds.append(item['id']['videoId'])
        
        token = response['nextPageToken']
        
    resp_df['title'] = titles
    resp_df['channelId'] = channelIds
    resp_df['videoId'] = videoIds
    resp_df['subject'] = criteria
    
    return resp_df


# In[9]:


MyStory = youtube_search('[my+story+animated]',1000)
MyStory.shape

MyStory.head()


# In[7]:


def playlist_items_list_by_playlist_id(client, **kwargs):
    # See full sample for function
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.playlistItems().list(**kwargs).execute()
    return response

def get_vid_ids (play_lists):
    titles = []
    descriptions = []
    channelids = []
    vidids = []
    playlist_ids = []
    video_df = pd.DataFrame()
    for play_list in play_lists:
        #request playlist items
        state=True 
        pl_data = playlist_items_list_by_playlist_id(client,
                            part='snippet,contentDetails',
                            maxResults=50,
                            playlistId=play_list)
        token=pl_data['nextPageToken']
        
        #extract information about each video in the playlist
        
        for item in pl_data['items']:
                titles.append(item['snippet']['title'])
                descriptions.append(item['snippet']['description'])
                channelids.append(item['snippet']['channelTitle'])
                vidids.append(item['snippet']['resourceId']['videoId'])
                playlist_ids.append(item['snippet']['playlistId'])
        
        
        while state:
            try:
                pl_data = playlist_items_list_by_playlist_id(client,
                            part='snippet,contentDetails',
                            maxResults=50,
                            playlistId=play_list,pageToken=token)
                token=pl_data['nextPageToken']
                
                for item in pl_data['items']:
                    titles.append(item['snippet']['title'])
                    descriptions.append(item['snippet']['description'])
                    channelids.append(item['snippet']['channelTitle'])
                    vidids.append(item['snippet']['resourceId']['videoId'])
                    playlist_ids.append(item['snippet']['playlistId'])
                
                
            except:
                state = False 
                
            
                
    video_df['title'] = titles
    video_df['description'] = descriptions
    video_df['channelid'] = channelids
    video_df['videoids'] = vidids
    video_df['playlist_id'] = playlist_ids
            
                
    return video_df


# Aqui playlist_df lee un cvs con la siguiente estructura, la primer fila la descripcion de la columna
# que debe ser PlaylistID y LectureName
# 
# luego en la primer columna va el identificador de una lista de reproducion y en la segunda columna el nombre que queramos para esa lista 

# In[8]:


playlist_df = pd.read_csv('listas.csv')
playlist_df.head()


# In[9]:


video_df = get_vid_ids(playlist_df.PlaylistID)
video_df.shape

#check results
video_df


# In[8]:


video_df.to_excel('All.xlsx',index=False)


# In[10]:


video_df.drop(video_df[video_df['title']=='Private video'].index,inplace=True)  

video_df = video_df.reset_index()

video_df


# In[11]:


Complete=' '
i=0
while i<529:
    Complete +=  video_df['title'][i]+ " \n " 
    i+=1
    
Complete
    


# In[16]:


Complete= Complete.replace('😎','e')
Complete = Complete.replace('| This is my story',' ')
Complete= Complete.replace('(r/AskReddit | Reddit Stories)',' ')
Complete


# In[17]:


text_file = open("sample.txt", "w")
n = text_file.write(Complete)
text_file.close()

