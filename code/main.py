# Here the file to run to execute the full process in normal (forward) mode

# Load the data and pre-process them

# Feed the data forward in the CNN

#%%
import torch
import tensorflow as tf
import keras
import data
import similarity_learning.models.dielemann.load 
from keras.backend.tensorflow_backend import set_session
import pdb
from pre_processing.chunkify import track_to_chunks
import skimage.transform as skt
from data.sets.audio import DatasetAudio, importAudioData
import numpy as np
import os
import pickle
from sklearn.manifold import TSNE
#%%

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
#config.gpu_options.per_process_gpu_memory_fraction = 0.3
config.gpu_options.visible_device_list = "2"
set_session(tf.Session(config=config))

#%%
audioSet, audioOptions = data.import_data.import_data()
#%%
transform_type, transform_options = audioSet.getTransforms()
audioSet.files = audioSet.files
batch_size = 20
nb_frames = 100
mod_options = {
        'activation': 'relu',
        'batchNormConv': True,
        'FC number': 2048,
        'batchNormDense': True,
        'Alphabet size': 10,
        'Freeze layer': False,
        'batch size': batch_size}
model_name = 'genre_full'
model_base, model_options = similarity_learning.models.dielemann.load.load_CNN_model(model_name)


#%%
X_embed = [[]]
for file_id in range(20):
    file = audioSet.files[file_id]
    downbeat = audioSet.metadata['downbeat'][file_id][0]
    Fs = 44100
    chunks = track_to_chunks(file_id, Fs, downbeat)
    data = []
    meta = []

    #print('loading '+ dataIn[idx
    for i in range(len(chunks)):
        chunk = chunks[i].get_cqt(audioSet, audioOptions)
        nbBins = chunk.shape[0]
        chunk = skt.resize(chunk, (nbBins, 100), mode='reflect')
        data.append(chunk)
        meta.append(chunks[i].get_meta(audioSet,'genre'))


    x = np.zeros((len(data), data[0].shape[0], data[0].shape[1]))
    for i in range(len(data)):
        x[i] = data[i]
    x = np.swapaxes(np.array(data),1,2)

    data_out = model_base.predict(x, verbose = 1)
    
    '''
    file_dir = './similarity_learning/Datasets/gtzan/CNN/'+model_name+'/'
    
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_dump = open(file_dir+'file_no_'+str(file_id), 'wb')
    pickle.dump(data_out, file_dump)
    file_dump.close()
    '''
    for i in range(data_out.shape[0]):
        X_embed[file_id][i] = TSNE().fit_transform(x[i])
    
filename = './tsne'
file = open(filename, 'wb')
pickle.dump(X_embed, filename)
    


# Feed the data to the VAE

# Re-synthetize data (auto-DJ)
