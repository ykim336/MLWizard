from mlwizards import fine_tune_model, upload_file
import time

api_key = "..."

# file_id = upload_file(api_key, "datasets/marv.jsonl")
print(fine_tune_model(api_key, "file-H1BnJBxt7MZTxqqFokTD2Xn1", "gpt-3.5-turbo"))