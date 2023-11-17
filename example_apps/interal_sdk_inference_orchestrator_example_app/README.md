# Internal SDK Inference Orchestrator example App

## Requirements
- Python 3.10+
- Miniconda

## Setup
Here's a brief explanation of how to run the [Internal SDK Inference Orchestrator](https://github.com/GDP-ADMIN/glair-genai-experiments-and-explorations) example app:

1. **Install requirements**:
   1. Create local enviroment `conda env create -f environment.yml`.
   2.  Install the dependencies via `pip install -r requirements.txt`. Make sure you have access to this [Internal SDK](https://github.com/GDP-ADMIN/glair-genai-experiments-and-explorations) repository.
2. **Set environment variables**:
   1. Create a file named `.env` and place the required information there.
   2. Check `.env-example` for the values.
3. **Set configuration file**:
   1. Please note that there is a configuration file at `configs/default_openai_llm_config.json`. This config is intended for the use of the OpenAI model. You can adjust it according to your needs, including the PromptTemplate, LLM HyperParameter, and UseCaseHandler configs.
4. **Start server**: `python app.py`.

## Backend API Test
1. **Make inference and generate response**: Hit `http://127.0.0.1:5000/generate-response` to make inference based on the uploaded documents as context.
   - Here's an example of the request body:
   ```text
    {
        "message": "How many year economy created over 6.5 Million new jobs? and what country history?"
    }
   ```
   - Here's an example using cURL:
   ```sh
   curl http://127.0.0.1:5000/generate-response -X POST -d \
   '{"message": "How many year economy created over 6.5 Million new jobs? and what country history?"}' \
   -H 'Content-Type: application/json' --no-buffer
   ```
   **Note**: The API endpoints must be hit with the `POST` method.
2. **Get configuration list**: Hit `http://127.0.0.1:5000/get-configs` to get the list of configurations.
   - Here's an example using cURL:
   ```sh
   curl http://127.0.0.1:5000/get-configs -X GET -H 'Content-Type: application/json'
   ```
   **Note**: The API endpoints must be hit with the `GET` method.
3. **Update configuration list**: Hit `http://127.0.0.1:5000/update-configs` to update the configurations.
   - Here's an example of the request body:
   ```text
   {
    "prompt_builder_params": {
        "default_template": {
            "template": "You're a chatbot that...",
            "key_prompt_additional": {}
        }
    },
    "llm_params": {
        "max_tokens": 512,
        "temperature": 0.0,
        "top_p": 0.14,
        "n": 1
    },
    "use_case_handler_params": {
        "model_max_input_token": 200,
        "model_max_context_token": 2500,
        "topic": "state-of-the-union",
        "search_threshold": 0.5,
        "search_top_k": 10
    }
   }
   ```
   - Here's an example using cURL:
   ```sh
   curl http://127.0.0.1:5000/update-configs -X POST -d \
   '{"prompt_builder_params": {}, "llm_params": {"max_tokens": 10, "temperature": 0.5}, "use_case_handler_params": {"search_threshold": 0.5, "search_top_k": 10}}' \
   -H 'Content-Type: application/json'
   ```
   **Note**: The API endpoints must be hit with the `POST` method.

## Project References
1. [GenAI Botica GitHub](https://github.com/GDP-ADMIN/gen-ai-botica/tree/f/add-backend).
