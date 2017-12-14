#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/scripts/vision for blinds-952cefcb99f2.json"
gcloud compute copy-files /home/pi/scripts/im_source.jpg cloud-computer:/home/pi/tfIm/im_source.jpg \
--zone europe-west1-b
gcloud compute ssh cloud-computer --command="/home/pi/scripts/tensorflow_im2txt" --zone europe-west1-b 
gcloud compute copy-files cloud-computer:/home/pi/scripts/out/im2txt.txt /home/pi/im2txt_out/im2txt.txt --zone europe-west1-b
