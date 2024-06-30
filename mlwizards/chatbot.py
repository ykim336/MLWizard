# mlwizard/chatbot.py

import openai
import pytesseract
from pdf2image import convert_from_path
import json
from bs4 import BeautifulSoup
import re
import requests
from requests_html import HTMLSession
import time

class ChatBot:
    def __init__(self, api_key, model, organization=None, project=None):
        self.api_key = api_key
        self.model = model
        self.conversation_history = []
        self.client = openai.OpenAI(api_key=api_key)
        if organization:
            self.client.organization = organization
        if project:
            self.client.project = project
    def generate(self, prompt, system_prompt=""):
        if not self.api_key or not self.model:
            raise ValueError("API key and model must be set.")
        
        try:
            messages = self.conversation_history + [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            assistant_message = response.choices[0].message.content.strip()

            return assistant_message
        except Exception as e:
            return f"An error occurred: {e}"
    def add_to_history(self, role, content):
        if role not in ['user', 'assistant']:
            raise ValueError("Role must be 'user' or 'assistant'.")
        self.conversation_history.append({"role": role, "content": content})
    def reset_conversation(self):
        self.conversation_history = []
    def scrape_with_requests_html(self, url):
        return
        session = HTMLSession()
        response = session.get(url)
        response.html.render(sleep=3)  # Render the JavaScript
        return response.html.html
    def remove_irrelevant_content(self, soup):
        return
        # Remove common irrelevant sections
        for script in soup(["script", "style", "header", "footer", "nav", "aside"]):
            script.decompose()

        # Optionally, remove elements by class or id
        for element in soup.find_all(class_=re.compile(r"advertisement|footer|header|nav|aside", re.I)):
            element.decompose()
        for element in soup.find_all(id=re.compile(r"advertisement|footer|header|nav|aside", re.I)):
            element.decompose()

        # Extract text and remove irrelevant whitespace
        text = ' '.join(soup.stripped_strings)

        return soup
    def search_internet(self, query, num_results=7):
        return
        search_url = f"https://www.google.com/search?q={query}&num={num_results * 3}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for item in soup.find_all('a'):
            href = item.get('href')
            if href and 'url?q=' in href and not 'webcache' in href:
                link = href.split('url?q=')[1].split('&sa=U')[0]
                links.append(link)
            if len(links) >= num_results * 3:
                break
        
        website_content = {}
        successful_links = 0
        for link in links:
            if successful_links >= num_results:
                break
            try:
                page_source = self.scrape_with_requests_html(link)
                page_soup = BeautifulSoup(page_source, 'html.parser')
                page_soup = self.remove_irrelevant_content(page_soup)
                text = ' '.join([p.text for p in page_soup.find_all('p')])
                if len(text.strip()) == 0:
                    # print(f"Empty content at {link}")
                    continue
                website_content[link] = text
                successful_links += 1
            except Exception as e:
                # print(f"Error retrieving content from {link}: {e}")
                continue
            time.sleep(1)  # Sleep for 1 second to avoid hitting request limits

        if successful_links < num_results:
            print(f"Only {successful_links} successful links found.")

        search_results_summary = "\n".join([f"Website: {k}\nContent: {v}" for k, v in website_content.items()])
        prompt = f"Based on the following search results, answer the query: {query}\n\n{search_results_summary}"
        response = self.generate(prompt)
        return response

def fine_tune_model(api_key, training_file_id, model='gpt-3.5-turbo', organization=None, project=None, suffix=None, hyperparameters=None):
    client = openai.OpenAI(api_key=api_key)
    if organization:
        client.organization = organization
    if project:
        client.project = project

    try:
        # Prepare the payload with necessary fields
        payload = {
            "model": model,
            "training_file": training_file_id,
        }
        if suffix:
            payload["suffix"] = suffix
        if hyperparameters:
            payload["hyperparameters"] = hyperparameters

        fine_tune_response = client.fine_tuning.jobs.create(**payload)
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
def preprocess_text(text):
    # Example preprocessing steps:
    # - Remove unnecessary whitespace
    # - Additional text processing steps as needed

    # Remove unnecessary whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    
    # Additional custom preprocessing steps can be added here

    return text.strip()
def extract_pdf(pdf_path, tesseract_cmd=None):
    return
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    # Convert PDF to images
    pages = convert_from_path(pdf_path)

    # Perform OCR on each image and preprocess the text
    extracted_text = []
    for page in pages:
        text = pytesseract.image_to_string(page)
        extracted_text.append(text)
    # Combine all extracted text
    combined_text = "\n".join(extracted_text)
    
    # Preprocess the combined text
    preprocessed_text = preprocess_text(combined_text)
    return preprocessed_text