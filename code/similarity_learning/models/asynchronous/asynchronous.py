# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 18:06:21 2018

@author: octav
"""

from similarity_learning.models.asynchronous.task import AsynchronousTask
from data.sets.audio import DatasetAudio
import pdb

def asynchronous_learning(audioSet, batch_size = 64, nb_epochs = 5):
    asyncTask = AsynchronousTask(DatasetAudio.getAsynchronousImport(), numWorkers = 4, batch_size = batch_size, shuffle = False)
    asyncTask.createTask(audioSet)
    for batchIDx, (currentData, currentMeta) in enumerate(asyncTask):
        print('[Batch ' + str(batchIDx) + '] Learning step on ' + str(len(currentData)) + ' examples');
        # Perform training on current data 
        dummy_learn(currentData, currentMeta);
    
    return 0

def dummy_learn(currentData, currentMeta):
    pdb.set_trace()
    print(currentData)
    print(currentMeta)
    