#create bucket using default settings, bucket name is the same as project id
gsutil mb -l 'asia-southeast1' -b on gs://${PROJECT_ID}

#create bigquery dataset & table to strore our output
gcloud alpha bq datasets create week3 

# I would like to run the script.sh every day at 00:00
# not completed yet
# * 0 * * * bash src/script.sh 