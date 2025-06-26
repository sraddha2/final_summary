import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from utils.web_loader import load_web_content
import openai

class AzureSummarizer:
    def __init__(self, key=None, endpoint=None):
        self.key = key or os.environ.get("AZURE_TEXT_ANALYTICS_KEY")
        self.endpoint = endpoint or os.environ.get("AZURE_TEXT_ANALYTICS_ENDPOINT")
        if not self.key or not self.endpoint:
            raise ValueError("Azure Text Analytics key and endpoint must be provided.")
        self.client = TextAnalyticsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )
        # For Azure OpenAI Q&A
        self.openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        self.openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.openai_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

    def summarize_text(self, text, max_sentences=3):
        poller = self.client.begin_extract_summary(
            documents=[text],
            max_sentence_count=max_sentences
        )
        result = poller.result()
        result_list = list(result)
        summary = " ".join([s.text for s in result_list[0].sentences])
        return summary

    def summarize_url(self, url, max_sentences=3):
        content = load_web_content(url)
        return self.summarize_text(content, max_sentences=max_sentences)

    def answer_question(self, context, question):
        if not self.openai_api_key or not self.openai_endpoint or not self.openai_deployment:
            return "Azure OpenAI credentials not set."
        client = openai.AzureOpenAI(
            api_key=self.openai_api_key,
            api_version="2023-05-15",
            azure_endpoint=self.openai_endpoint
        )

        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        try:
            response = client.chat.completions.create(
                model=self.openai_deployment,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=256,
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error from Azure OpenAI: {str(e)}"