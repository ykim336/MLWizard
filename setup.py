from setuptools import setup, find_packages

setup(
    name='mlwizards',  # Updated project name
    version='0.1.1',
    description='A simple library for chatbots and model finetuning using OpenAI',
    author='Yvon Kim',
    author_email='kmyn7up@gmail.com',
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        'openai',
        'pytesseract',
        'pdf2image',
        'pillow',
        'googlesearch-python',
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'mlwizard=mlwizards.chatbot:main',  # Updated to match the new name
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
