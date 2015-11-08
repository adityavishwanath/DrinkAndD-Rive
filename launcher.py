import os

#Launches sttClient.py, which performs the Speech to Text Analysis.
#Need to populate recordings with .wav files.
#Output is stored in output directory.
os.system("python ./sttClient.py -credentials bd6b4d7a-896d-4e64-a538-728ca8462521:6L8Rb2Mm6IBx -model en-US_BroadbandModel")