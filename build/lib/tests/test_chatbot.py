import unittest
from mlwizard import ChatBot, fine_tune_model, list_fine_tuning_jobs, retrieve_fine_tuning_job, cancel_fine_tuning_job, upload_file, list_files, retrieve_file, delete_file, retrieve_file_content, extract_pdf_data

class TestChatBot(unittest.TestCase):

    def setUp(self):
        self.bot = ChatBot(api_key="your_api_key")

    def test_generate(self):
        prompt = "Hello, how are you?"
        response = self.bot.generate(prompt)
        self.assertIsInstance(response, str)

    def test_generate_streaming(self):
        prompt = "Hello, how are you?"
        response = self.bot.generate(prompt, stream=True)
        self.assertIsInstance(response, str)

    def test_add_to_history(self):
        self.bot.add_to_history('user', "Hello")
        self.bot.add_to_history('assistant', "Hi there")
        self.assertEqual(len(self.bot.conversation_history), 2)

    def test_reset_conversation(self):
        self.bot.add_to_history('user', "Hello")
        self.bot.reset_conversation()
        self.assertEqual(len(self.bot.conversation_history), 0)

class TestFineTuning(unittest.TestCase):

    def setUp(self):
        self.api_key = "your_api_key"

    def test_fine_tune_model(self):
        training_file_id = "file-abc123"
        response = fine_tune_model(self.api_key, training_file_id)
        self.assertIn("id", response)

    def test_list_fine_tuning_jobs(self):
        response = list_fine_tuning_jobs(self.api_key)
        self.assertIn("data", response)

    def test_retrieve_fine_tuning_job(self):
        job_id = "ftjob-abc123"
        response = retrieve_fine_tuning_job(self.api_key, job_id)
        self.assertIn("id", response)

    def test_cancel_fine_tuning_job(self):
        job_id = "ftjob-abc123"
        response = cancel_fine_tuning_job(self.api_key, job_id)
        self.assertIn("status", response)

class TestFileHandling(unittest.TestCase):

    def setUp(self):
        self.api_key = "your_api_key"

    def test_upload_file(self):
        response = upload_file(self.api_key, "path/to/your/file.jsonl")
        self.assertIn("id", response)

    def test_list_files(self):
        response = list_files(self.api_key)
        self.assertIn("data", response)

    def test_retrieve_file(self):
        file_id = "file-abc123"
        response = retrieve_file(self.api_key, file_id)
        self.assertIn("id", response)

    def test_delete_file(self):
        file_id = "file-abc123"
        response = delete_file(self.api_key, file_id)
        self.assertIn("deleted", response)

    def test_retrieve_file_content(self):
        file_id = "file-abc123"
        response = retrieve_file_content(self.api_key, file_id)
        self.assertIsInstance(response, str)

class TestPDFExtraction(unittest.TestCase):

    def test_extract_pdf_data(self):
        extract_pdf_data("path/to/your/file.pdf", "path/to/your/output.json")
        # Add assertions here to verify the contents of the output JSON file if needed.

if __name__ == '__main__':
    unittest.main()
