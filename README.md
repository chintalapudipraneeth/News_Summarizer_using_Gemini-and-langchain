# News Chat Summarization Using Gemini LLM

This is a Streamlit application that allows users to enter a news article URL and ask questions related to the content. The application then uses the Google Generative AI (Gemini) model and LangChain to summarize the relevant information from the article and provide an answer to the user's question.

## Features

- **URL Validation**: The application validates the provided URL to ensure it is a valid and accessible web page.
- **Text Splitting**: The article content is split into smaller chunks using LangChain's `RecursiveCharacterTextSplitter` to efficiently process the text.
- **Question Answering**: The application uses LangChain's `load_qa_chain` to generate an answer to the user's question based on the article content.
- **Session Storage**: The application stores the previous links, chat questions, and responses in the browser session, allowing users to review their history.


## Installation

1. Clone the repository:
2. Navigate to the project directory
3. Create a virtual environment and install the required dependencies
4. Set up the Google API key:
   - Create a `.env` file in the project root directory.
   - Add your Google API key to the `.env` file: `GOOGLE_API_KEY=your-api-key`

## Usage

1. **Run the Application**: Execute the Streamlit application by running:
    ```bash
    streamlit run app.py
    ```

2. **Input News Article Link**: Provide a link to a news article in the text input field labeled "News Article link."

3. **Engage in Chat**: Enter your questions related to the news article in the "Chat" text input field and submit.

4. **View Summarized Responses**: The application will process the input and display the summarized responses. Previous interactions are stored below for reference.

