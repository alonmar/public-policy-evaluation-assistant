# public-policy-evaluation-assistant

# RAG Flow for Housing Policy Public Consultation Assistant

This project implements a *Retrieval-Augmented Generation* (RAG) flow aimed at developing an expert assistant focused on housing public policy. The assistant is designed to provide verified information about housing policies, highlighting the pros and cons of various proposals to facilitate balanced, well-informed decision-making.

## Project Objective

The main goal is to create a support system for policymakers and public policy professionals, enabling them to obtain accurate, objective summaries on the impact of various housing policies. This assistant leverages relevant data (academic articles, government reports, etc.) and generates structured responses covering the positive and negative aspects of each policy.

## Key Features

- **Verified Information Querying**: The assistant uses a RAG flow to retrieve and synthesize relevant data in response to specific questions about housing policies.
- **Structured Pros and Cons**: Each response includes a summary of the policy's pros and cons, ensuring a balanced and neutral focus.
- **Professional, Objective Tone**: Designed to provide accurate information without additional assumptions or extrapolations beyond the context.

## Project Structure

- **Data Retrieval**: Components to retrieve academic articles, documents, and other relevant data for content generation.
- **Data Chunking**: Long texts are divided into 240-word chunks for efficient search and retrieval. Chunks are configurable for overlap, maintaining context across sections.
- **Response Generation**: A language model receives a query and uses retrieved context to answer with specific pros and cons, maintaining a clear, concise structure.
- **Parameter Configuration**: Customizable chunk size and overlap parameters optimize response accuracy based on context.

## Usage Example

To query a specific housing policy, the user can ask a question such as, “What are the pros and cons of implementing rent control policies in urban areas?”

The assistant will generate a response based solely on verified contextual information, presenting a clear summary of pros and cons to support decision-making.

## Requirements

- **Python 3.10+**
- **Libraries**:
  - `transformers` for the language model
  - `pandas` and `numpy` for data manipulation
  - `scikit-learn` for additional text processing techniques

## Installation Instructions

1. Clone this repository to your local machine.
    ```bash
    git clone https://github.com/alonmar/public-policy-evaluation-assistant.git
    cd public-policy-evaluation-assistant
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up your articles and reports database in the `data/` directory and ensure to update the retrieval index.

## Usage

To launch the assistant, run the following command and follow the instructions:
```bash
python run_assistant.py
```

## Customization

Chunking Parameters: You can adjust chunk size and overlap in the config.py file.
Language Model: Choose between a local model (such as LLaMA) or an API-based model (such as GPT-4).

## Contributions
Contributions are welcome. If you would like to improve the assistant, please open a pull request or discuss your ideas in the issues section.



python .\app\elasticsearch_prep.py
