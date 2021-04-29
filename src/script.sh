#define variable for the date
date=$(date '+%Y-%m-%d')

#upload (and move) data to cloud storage
gsutil cp Data/$date.json gs://${PROJECT_ID}

#create dataproc cluster
gcloud beta dataproc clusters create ${PROJECT_ID} \
--region="asia-southeast1" \
--scopes=default \
--master-machine-type n1-standard-2 \
--master-boot-disk-size 20 \
--num-workers 2 \
--worker-machine-type n1-standard-2 \
--worker-boot-disk-size 20 \
--image-version 1.3

#submit jobs
gcloud dataproc jobs submit pyspark src/pysparkjob.py \
--cluster=${PROJECT_ID} \
--region="asia-southeast1" \
-- gs://${PROJECT_ID}/$date.json

#delete dataproc cluster
gcloud dataproc clusters delete ${PROJECT_ID} --region=asia-southeast1