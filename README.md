# MLWizards

MLWizards is a Python library designed to simplify the process of creating chatbots and fine-tuning models using OpenAI. It also includes features for extracting and processing text from PDFs. 

## Features

- **ChatBot**: Easily create and interact with chatbots using OpenAI's GPT models.
- **Model Fine-Tuning**: Fine-tune OpenAI models with your own data.
- **PDF Text Extraction**: Extract and preprocess text from PDF files using OCR.

## Installation

1. **Install the required Python packages**:
   ```sh
   pip install pytesseract pdf2image pillow requests-html openai beautifulsoup4
   ```

2. **Install Poppler**:

   ### Windows
   - Download `Poppler` from [here](http://blog.alivate.com.au/poppler-windows/).
   - Extract the contents to a directory, e.g., `C:\poppler`.
   - Add `C:\poppler\bin` to your system's PATH.

   ### macOS
   - Use `Homebrew` to install `Poppler`:
     ```sh
     brew install poppler
     ```

   ### Linux
   - Use the package manager to install `Poppler`:
     ```sh
     sudo apt-get install poppler-utils
     ```

3. **Install Tesseract OCR**:
   - Follow the instructions [here](https://github.com/tesseract-ocr/tesseract) to install Tesseract OCR on your operating system.

## Usage

### ChatBot

Create and interact with a chatbot using OpenAI's GPT models.

```python
from mlwizards import ChatBot

api_key = "your_openai_api_key"
bot = ChatBot(api_key=api_key)

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
    response = bot.generate(user_input)
    bot.add_to_history('user', user_input)
    bot.add_to_history('assistant', response)
    print("Bot:", response)
```

### Model Fine-Tuning

Fine-tune OpenAI models with your own data.

```python
from mlwizards import fine_tune_model, upload_file

api_key = "your_openai_api_key"
training_file_path = "path/to/your/training_data.jsonl"

# Upload the training file
upload_response = upload_file(api_key, training_file_path)
training_file_id = upload_response['id']

# Fine-tune the model
fine_tune_response = fine_tune_model(api_key, training_file_id)
print(f"Fine-tuning job started. Response: {fine_tune_response}")
```

### PDF Text Extraction

Extract and preprocess text from PDF files using OCR.

```python
from mlwizards import extract_text_from_pdf

pdf_path = "path/to/your/file.pdf"
tesseract_cmd = "/usr/local/bin/tesseract"  # Update this path to your tesseract executable if needed
extracted_text = extract_text_from_pdf(pdf_path, tesseract_cmd)
print(extracted_text)
```

## Functions

### ChatBot Class

- `__init__(self, api_key, model='gpt-3.5-turbo', organization=None, project=None)`: Initialize the ChatBot with API key and model.
- `generate(self, prompt)`: Generate a response from the chatbot.
- `add_to_history(self, role, content)`: Add a message to the conversation history.
- `reset_conversation(self)`: Reset the conversation history.
- `search_internet(self, query, num_results=5)`: Search the internet and generate a response based on search results.

### Fine-Tuning Functions

- `fine_tune_model(api_key, training_file_id, model='gpt-3.5-turbo', organization=None, project=None, suffix=None, hyperparameters=None)`: Fine-tune a model with the given training file.
- `upload_file(api_key, file_path, purpose='fine-tune', organization=None, project=None)`: Upload a file to OpenAI.

### PDF Text Extraction Functions

- `extract_text_from_pdf(pdf_path, tesseract_cmd=None)`: Extract text from a PDF file using OCR.
- `preprocess_text(text)`: Preprocess extracted text by removing unnecessary whitespace and newlines.

## Contributing

We welcome contributions to MLWizards! Please submit a pull request or open an issue to discuss any changes you would like to make.

## License

This project is licensed under the MIT License.
```

This README provides a comprehensive guide to installing, using, and contributing to the `MLWizards` library. It includes instructions for installing dependencies, examples of how to use the main features, and descriptions of the key functions.