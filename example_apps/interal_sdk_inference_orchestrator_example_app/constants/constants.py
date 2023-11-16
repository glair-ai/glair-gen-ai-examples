"""Defines a class containing constants used by the main modules.

Authors:
    Moch. Nauval Rizaldi Nasril (moch.n.r.nasril@gdplabs.id)

Reviewers:
    Kevin Yauris (kevin.yauris@gdplabs.id)

References:
    [1] https://github.com/GDP-ADMIN/gsdp
    [2] https://github.com/GDP-ADMIN/gen-ai-botica/tree/f/add-backend
"""
import os

from glair_genai_sdk.inference_orchestrator.constant.constants import (
    ConfigParameters,
    UseCaseHandlerConstants,
)


class EnvironmentVariables:
    """Class used to define constant keys for environment variables.

    Attributes:
        API_HOSTNAME (str): Key to retrieve the API hostname from environment variables for running the app.
        API_PORT (str): Key to retrieve the API port number from environment variables for running the app.
        OPENAI_MODEL_NAME (str): Key to retrieve the OpenAI model name from environment variables.
        OPENAI_EMBEDDING_NAME (str): Key to retrieve the OpenAI embedding name from environment variables.
        OPENAI_API_KEY (str): Key to retrieve the OpenAI API key from environment variables.
        CHROMA_VECTOR_DB_PERSIST_DIRECTORY (str): Key to get the path to the persist directory of the Chroma vector database
                                           from environment variables to load the vector database.
    """

    API_HOSTNAME = "API_HOSTNAME"
    API_PORT = "API_PORT"
    OPENAI_MODEL_NAME = "OPENAI_MODEL_NAME"
    OPENAI_EMBEDDING_NAME = "OPENAI_EMBEDDING_NAME"
    OPENAI_API_KEY = "OPENAI_API_KEY"
    CHROMA_VECTOR_DB_PERSIST_DIRECTORY = "CHROMA_VECTOR_DB_PERSIST_DIRECTORY"


class ExampleInferenceOrchestratorEnvironmentVariables:
    """Class used to get the constant values environment variables.

    This class will locate the `.env` file and load the variables into the environment variables.

    Attributes:
        api_hostname (str): Class method to retrieve the API hostname to run the app.
        api_port (str): Class method to retrieve the API port number to run the app.
        persist_directory_path (str): Class method to retrieve the path to the persist directory of the vector database.
        model_name (str): Class method to retrieve the OpenAI Model.
        embedding_name (str): Class method to retrieve the OpenAI Embedding Model.
        openai_api_key (str): Class method to retrieve the OpenAI API Key.
    """

    @classmethod
    def api_hostname(cls):
        """Class method to retrieve the API hostname to run the app."""
        return os.environ[EnvironmentVariables.API_HOSTNAME]

    @classmethod
    def api_port(cls):
        """Class method to retrieve the API port number to run the app."""
        return os.environ[EnvironmentVariables.API_PORT]

    @classmethod
    def persist_directory_path(cls):
        """Class method to retrieve the path to the persist directory of the vector database."""
        return os.environ[EnvironmentVariables.CHROMA_VECTOR_DB_PERSIST_DIRECTORY]

    @classmethod
    def model_name(cls):
        """Class method to retrieve the OpenAI Model."""
        return os.environ[EnvironmentVariables.OPENAI_MODEL_NAME]

    @classmethod
    def embedding_name(cls):
        """Class method to retrieve the OpenAI Embedding Model."""
        return os.environ[EnvironmentVariables.OPENAI_EMBEDDING_NAME]

    @classmethod
    def openai_api_key(cls):
        """Class method to retrieve the OpenAI API Key."""
        return os.environ[EnvironmentVariables.OPENAI_API_KEY]


class ExampleInferenceOrchestratorAPIConstant:
    """Class used to define the constants to serve the app API.

    Attributes:
        GENERATE_RESPONSE_ROUTE (str): The path of the API endpoint for generating responses from the model.
        GET_PARAM_ROUTE (str): The path of the API endpoint for retrieving model hyperparameters.
        METHODS_GET (List[str]): List of HTTP methods supported for GET requests.
        METHODS_POST (List[str]): List of HTTP methods supported for POST requests.
        PARAM_MESSAGE (str): Key used to retrieve the message from the request.
        RESPONSE_MIMETYPE (str): MIME type for the API response.
        UPDATE_PARAM_ROUTE (str): The path of the API endpoint for updating model hyperparameters.
        HEALTH_CHECK (str): Endpoint for health check.
    """

    GENERATE_RESPONSE_ROUTE = "/generate-response"
    GET_PARAM_ROUTE = "/get-configs"
    METHODS_GET = ["GET"]
    METHODS_POST = ["POST"]
    PARAM_MESSAGE = "message"
    RESPONSE_MIMETYPE = "text/event-stream"
    UPDATE_PARAM_ROUTE = "/update-configs"
    HEALTH_CHECK = "/health-check"


class ExampleInferenceOrchestratorAPIMessage:
    """Class used to define the constants for API message.

    Attributes:
        API_RESPONSE_FIELD_MESSAGE (str): Key used to place the message for the API to send.
        API_RESPONSE_FIELD_STATUS (str): Key used to place the status for the API to send.
        MESSAGE_UPDATE_CONFIG_SUCCESS (str): Message when the configurations are updated successfully.
        MESSAGE_HEALTH_CHECK_API_SUCCESS (str): Message indicating a successful health check for the API.
    """

    API_RESPONSE_FIELD_MESSAGE = "message"
    API_RESPONSE_FIELD_STATUS = "success"
    MESSAGE_UPDATE_CONFIG_SUCCESS = "Successfully updated configurations."
    MESSAGE_HEALTH_CHECK_API_SUCCESS = "Health check success"


CONFIG_DESCRIPTION = {
    ConfigParameters.PROMPT_BUILDER_PARAMS: {
        "default_template": "The default prompt template to be used in Question and Answer."
    },
    ConfigParameters.LLM_PARAMS: {
        "max_tokens": "The maximum number of tokens to generate in the completion.",
        "temperature": "What sampling temperature to use.",
        "top_p": "Total probability mass of tokens to consider at each step.",
        "n": "How many completions to generate for each prompt.",
    },
    ConfigParameters.USE_CASE_HANDLER_PARAMS: {
        UseCaseHandlerConstants.MODEL_MAX_CONTEXT_TOKEN: "The maximum total token for the retrieved documents "
        "that are used as the context.",
        UseCaseHandlerConstants.MODEL_MAX_INPUT_TOKEN: "The maximum token for the user's question.",
        UseCaseHandlerConstants.TOPIC: "The selected topic used by the model to answer the given question.",
        UseCaseHandlerConstants.SEARCH_THRESHOLD: "The minimum similarity probability between 0-1 for a document "
        "used as the context",
        UseCaseHandlerConstants.SEARCH_TOP_K: "The maximum number of retrieved documents when performing similarity search.",
    }
}


CONFIG_TYPE = {
    ConfigParameters.PROMPT_BUILDER_PARAMS: {
        "default_template": "dict",
    },
    ConfigParameters.LLM_PARAMS: {
        "max_tokens": "int",
        "temperature": "float",
        "top_p": "float",
        "n": "int",
    },
    ConfigParameters.USE_CASE_HANDLER_PARAMS: {
        UseCaseHandlerConstants.MODEL_MAX_CONTEXT_TOKEN: "float",
        UseCaseHandlerConstants.MODEL_MAX_INPUT_TOKEN: "int",
        UseCaseHandlerConstants.TOPIC: "text",
        UseCaseHandlerConstants.SEARCH_THRESHOLD: "float",
        UseCaseHandlerConstants.SEARCH_TOP_K: "int",
    }
}


class ConfigField:
    """Class used to define the field name of the Configuration."""

    CONFIG_FIELD_DEFAULT_VALUE = "default_value"
    CONFIG_FIELD_TYPE = "type"
    CONFIG_FIELD_DESCRIPTION = "description"


# Ad more collection names if needed
COLLECTION_NAMES = ["state-of-the-union"]
DEFAULT_CONFIG_PATH = "./configs/default_openai_llm_config.json"
DEFAULT_PROMPT_BUILDER_KEY = "default_template"