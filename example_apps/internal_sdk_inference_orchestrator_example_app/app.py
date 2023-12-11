"""Starting backend server and exposing the Flask API endpoints.

Authors:
    Moch. Nauval Rizaldi Nasril (moch.n.r.nasril@gdplabs.id)

Reviewers:
    Kevin Yauris (kevin.yauris@gdplabs.id)

References:
    [1] https://github.com/GDP-ADMIN/bca-gen-ai-on-cloud/tree/main/backend
    [2] https://github.com/GDP-ADMIN/gen-ai-veriwise/tree/main
    [3] https://github.com/GDP-ADMIN/gen-ai-botica/tree/f/add-backend
"""

import json
from threading import Thread
from typing import Any, Dict

from constants.constants import (
    COLLECTION_NAMES,
    CONFIG_DESCRIPTION,
    CONFIG_TYPE,
    DEFAULT_CONFIG_PATH,
    DEFAULT_PROMPT_BUILDER_KEY,
    APIMessage,
    ConfigField,
    ExampleInferenceOrchestratorAPIConstant,
    ExampleInferenceOrchestratorEnvironmentVariables,
)
from dotenv import load_dotenv
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
from gdplabs_gen_ai.inference_orchestrator import FlowExecutor
from gdplabs_gen_ai.inference_orchestrator.llm import Generator, OpenAILLM
from gdplabs_gen_ai.inference_orchestrator.prompt import PromptBuilder
from gdplabs_gen_ai.inference_orchestrator.search import ChromaVectorDB
from gdplabs_gen_ai.inference_orchestrator.use_case import QAUseCaseHandler
from gdplabs_gen_ai.inference_orchestrator.utility.utils import load_config, save_config
from langchain.embeddings import OpenAIEmbeddings

app = Flask(__name__)
CORS(app)

# Load `.env`
load_dotenv()

# Intitialize embedding model
embedder = OpenAIEmbeddings(
    model=ExampleInferenceOrchestratorEnvironmentVariables.embedding_name(),
    openai_api_key=ExampleInferenceOrchestratorEnvironmentVariables.openai_api_key(),
)

# Load VectorDB
db_dict = {}
for collection in COLLECTION_NAMES:
    db_dict[collection] = ChromaVectorDB(
        embedder,
        collection,
        persist_directory=ExampleInferenceOrchestratorEnvironmentVariables.persist_directory_path(),
    )

# Intitialize Large Language Model
llm = OpenAILLM(
    model_name=ExampleInferenceOrchestratorEnvironmentVariables.model_name(),
    openai_api_key=ExampleInferenceOrchestratorEnvironmentVariables.openai_api_key(),
    hyperparameter_file_path=DEFAULT_CONFIG_PATH,
)

# Intitialize PromptBuilder from config's file
prompt_builders = PromptBuilder.from_config(config_path=DEFAULT_CONFIG_PATH)

# Intitialize UseCaseHandler
qa_handler = QAUseCaseHandler(
    topic_db_map=db_dict,
    llm=llm,
    prompt_builder=prompt_builders[DEFAULT_PROMPT_BUILDER_KEY],
    config_file_path=DEFAULT_CONFIG_PATH,
)

# Intitialize FlowExecutor
flow_executor = FlowExecutor(qa_handler)


def wrap_message(message: str, success: bool = False) -> Dict[str, str]:
    """Wrap a message with optional success status.

    This function wraps a message with an optional success status and returns it as a dictionary.

    Args:
        message (str): The message to be wrapped.
        success (bool, optional): The success status (default is None).

    Returns:
        Dict[str, str]: A message dictionary.
    """
    response = {APIMessage.API_RESPONSE_FIELD_MESSAGE: message}
    if success:
        response[APIMessage.API_RESPONSE_FIELD_STATUS] = success
    return response


@app.route(
    ExampleInferenceOrchestratorAPIConstant.HEALTH_CHECK,
    methods=ExampleInferenceOrchestratorAPIConstant.METHODS_GET,
)
@cross_origin()
def get_health_check():
    """Expose a Flask API endpoint to verify that the API can be accessed."""
    message = {APIMessage.API_RESPONSE_FIELD_MESSAGE: APIMessage.MESSAGE_HEALTH_CHECK_API_SUCCESS}
    return (
        json.dumps(message),
        200,
    )


@app.route(
    ExampleInferenceOrchestratorAPIConstant.GENERATE_RESPONSE_ROUTE,
    methods=ExampleInferenceOrchestratorAPIConstant.METHODS_POST,
)
@cross_origin()
def generate_response() -> Response:
    """Expose a Flask API endpoint to get response from LLM.

    This function retrieves user's message, preprocess it and generate streamed response to the client.

    Returns:
        Response: The streamed response generated by Finetuned Llama2.
    """
    message = request.get_json()[ExampleInferenceOrchestratorAPIConstant.PARAM_MESSAGE]
    generator = Generator()

    streaming_thread = Thread(target=flow_executor.run_flow, args=(generator, message))

    streaming_thread.start()

    return Response(generator, mimetype=ExampleInferenceOrchestratorAPIConstant.RESPONSE_MIMETYPE)


@app.route(
    ExampleInferenceOrchestratorAPIConstant.GET_PARAM_ROUTE,
    methods=ExampleInferenceOrchestratorAPIConstant.METHODS_GET,
)
@cross_origin()
def get_configs() -> Dict[str, Dict[str, Any]]:
    """Expose a Flask API endpoint to get the current configurations settings.

    This function retrieves and returns the current configurations settings in a dictionary format.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary containing the current configurations settings.
    """
    current_configs = load_config(config_path=DEFAULT_CONFIG_PATH)
    current_configs_detail = {
        key1: {
            key2: {
                ConfigField.CONFIG_FIELD_DEFAULT_VALUE: value2,
                ConfigField.CONFIG_FIELD_TYPE: CONFIG_DESCRIPTION[key1][key2],
                ConfigField.CONFIG_FIELD_DESCRIPTION: CONFIG_TYPE[key1][key2],
            }
            for key2, value2 in value1.items()
        }
        for key1, value1 in current_configs.items()
    }

    return current_configs_detail


@app.route(
    ExampleInferenceOrchestratorAPIConstant.UPDATE_PARAM_ROUTE,
    methods=ExampleInferenceOrchestratorAPIConstant.METHODS_POST,
)
@cross_origin()
def update_config() -> Dict[str, str]:
    """Expose a Flask app API endpoint to update configuration settings.

    This function receives the updated configurations as JSON data, validates them,
    and updates the current configuration settings. It returns a success message if the update is successful.

    Returns:
        Dict[str, str]: A message indicating the status of the configuration update.
    """
    try:
        json_data = request.get_json()
        current_configs = load_config(config_path=DEFAULT_CONFIG_PATH)
        missing_keys = [key for key in json_data if key not in current_configs]
        if missing_keys:
            raise ValueError(f"Keys not found in current configuration: {missing_keys}")

        for key, values in json_data.items():
            if key in current_configs:
                for sub_key, sub_value in values.items():
                    if sub_key in current_configs[key]:
                        current_configs[key][sub_key] = sub_value
                    else:
                        raise ValueError(
                            "Sub-key '{}' not found in '{}' of current configuration.".format(sub_key, key)
                        )

        save_config(DEFAULT_CONFIG_PATH, current_configs)
        llm.update_hyperparameter_from_json(DEFAULT_CONFIG_PATH)
        qa_handler.update_config_from_json(DEFAULT_CONFIG_PATH)
        updated_prompt_builders = PromptBuilder.from_config(config_path=DEFAULT_CONFIG_PATH)
        qa_handler.update_prompt_builder(updated_prompt_builders[DEFAULT_PROMPT_BUILDER_KEY])

        message = APIMessage.MESSAGE_UPDATE_CONFIG_SUCCESS
        success = True
    except Exception as error:
        message = str(error)
        success = False

    return wrap_message(message, success)


def run_server() -> None:
    """Main class to start the Flask app API."""
    hostname = ExampleInferenceOrchestratorEnvironmentVariables.api_hostname()
    port = int(ExampleInferenceOrchestratorEnvironmentVariables.api_port())
    app.run(host=hostname, port=port, debug=True)


if __name__ == "__main__":
    # Running Server
    run_server()