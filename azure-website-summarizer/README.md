# Azure Website Summarizer

This project is a website summarizer application that utilizes Azure's Text Analytics API to generate summaries from provided text or web content. It allows users to input a URL or text and receive a concise summary.

## Project Structure

```
azure-website-summarizer
├── src
│   ├── app.py                # Entry point of the application
│   ├── summarizer
│   │   └── azure_summarizer.py # Contains AzureSummarizer class for summarization
│   ├── utils
│   │   └── web_loader.py      # Function to load web content from a URL
│   └── types
│       └── index.py           # Defines data types and interfaces
├── requirements.txt           # Lists project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd azure-website-summarizer
   ```

2. **Install dependencies:**
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Set up Azure Text Analytics:**
   - Create an Azure account if you don't have one.
   - Set up a Text Analytics resource in the Azure portal.
   - Obtain your API key and endpoint URL.

4. **Configure environment variables:**
   Set the following environment variables in your system:
   ```
   AZURE_TEXT_ANALYTICS_KEY=<your-api-key>
   AZURE_TEXT_ANALYTICS_ENDPOINT=<your-endpoint-url>
   ```

## Usage

To run the application, execute the following command:
```
python src/app.py
```

You can then access the application in your web browser and input a URL or text to receive a summary.

## Azure Services Used

- **Azure Text Analytics API:** This service provides advanced natural language processing capabilities, including text summarization, sentiment analysis, and entity recognition.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.