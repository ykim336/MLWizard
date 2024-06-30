# mlwizard/chatbot.py

import openai
import pytesseract
from pdf2image import convert_from_path
import json

class ChatBot:
    def __init__(self, api_key, model='gpt-3.5-turbo', organization=None, project=None):
        self.api_key = api_key
        self.model = model
        self.conversation_history = []
        self.client = openai.OpenAI(api_key=api_key)
        if organization:
            self.client.organization = organization
        if project:
            self.client.project = project

    def generate(self, prompt, stream=False):
        if not self.api_key or not self.model:
            raise ValueError("API key and model must be set.")
        
        try:
            messages = self.conversation_history + [{"role": "user", "content": prompt}]
            if stream:
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=True,
                )
                response = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        response += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content, end="")
                return response
            else:
                response = self.client.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                )
                assistant_message = response.choices[0].message['content'].strip()
                return assistant_message
        except Exception as e:
            return f"An error occurred: {e}"

    def add_to_history(self, role, content):
        if role not in ['user', 'assistant']:
            raise ValueError("Role must be 'user' or 'assistant'.")
        self.conversation_history.append({"role": role, "content": content})

    def reset_conversation(self):
        self.conversation_history = []

def fine_tune_model(api_key, training_file_id, model='gpt-3.5-turbo', organization=None, project=None, suffix=None, hyperparameters=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        fine_tune_response = client.fine_tuning.jobs.create(
            model=model,
            training_file=training_file_id,
            suffix=suffix,
            hyperparameters=hyperparameters
        )
        return fine_tune_response
    except Exception as e:
        return f"An error occurred: {e}"

def list_fine_tuning_jobs(api_key, organization=None, project=None, limit=20, after=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        fine_tuning_jobs = client.fine_tuning.jobs.list(limit=limit, after=after)
        return fine_tuning_jobs
    except Exception as e:
        return f"An error occurred: {e}"

def retrieve_fine_tuning_job(api_key, job_id, organization=None, project=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        fine_tuning_job = client.fine_tuning.jobs.retrieve(job_id)
        return fine_tuning_job
    except Exception as e:
        return f"An error occurred: {e}"

def cancel_fine_tuning_job(api_key, job_id, organization=None, project=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        canceled_job = client.fine_tuning.jobs.cancel(job_id)
        return canceled_job
    except Exception as e:
        return f"An error occurred: {e}"

def upload_file(api_key, file_path, purpose='fine-tune', organization=None, project=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        with open(file_path, 'rb') as f:
            response = client.files.create(file=f, purpose=purpose)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

def list_files(api_key, purpose=None, organization=None, project=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        files = client.files.list(purpose=purpose)
        return files
    except Exception as e:
        return f"An error occurred: {e}"

def retrieve_file(api_key, file_id, organization=None, project=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        file_info = client.files.retrieve(file_id)
        return file_info
    except Exception as e:
        return f"An error occurred: {e}"

def delete_file(api_key, file_id, organization=None, project=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        response = client.files.delete(file_id)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

def retrieve_file_content(api_key, file_id, organization=None, project=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        content = client.files.content(file_id)
        return content
    except Exception as e:
        return f"An error occurred: {e}"

def extract_pdf_data(pdf_path, json_path, tesseract_cmd=None):
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    pages = convert_from_path(pdf_path)
    extracted_text = []
    for page in pages:
        text = pytesseract.image_to_string(page)
        extracted_text.append(text.strip())

    combined_text = "\n".join(extracted_text)
    json_data = [{"prompt": s.strip(), "completion": ""} for s in combined_text.split('.') if s.strip()]

    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
