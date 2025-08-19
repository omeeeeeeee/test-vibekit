from __future__ import annotations

import os
from typing import Union, Dict, Any, TypedDict
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

OS_URL = "https://fintor-ec2-test.ngrok.app"
DEFAULT_FILE_NAME = "test_document.pdf"

class State(TypedDict):
    user_input: Union[str, Dict[str, Any], None]
    current_node: int
    status: str
    file_name: str
    upload_url: Union[str, None]

def validate_file(state: State, config: RunnableConfig) -> State:
    file_name = state.get("file_name", DEFAULT_FILE_NAME)
    
    if not file_name.endswith(".pdf"):
        state["status"] = "Error: File must be PDF format"
        state["current_node"] = 1
        return state
    
    if not os.path.exists(file_name):
        state["status"] = "Error: File does not exist"
        state["current_node"] = 1
        return state
    
    state["file_name"] = file_name
    state["current_node"] = 1
    state["status"] = "Success"
    return state

def click_action(state: State, config: RunnableConfig, **kwargs) -> State:
    state["status"] = "Success"
    return state

def wait_action(state: State, config: RunnableConfig, **kwargs) -> State:
    state["status"] = "Success"
    return state

def input_action(state: State, config: RunnableConfig, **kwargs) -> State:
    text = kwargs.get("text", "")
    if text == "state.file_name":
        text = state.get("file_name", "")
    state["status"] = "Success"
    return state

def validate_file_node(state: State, config: RunnableConfig) -> State:
    state["current_node"] = 1
    return validate_file(state, config)

def click_documents_node(state: State, config: RunnableConfig) -> State:
    state["current_node"] = 2
    return click_action(state, config, x=120, y=50)

def wait_1s_node(state: State, config: RunnableConfig) -> State:
    state["current_node"] = 3
    return wait_action(state, config, duration=1)

def click_upload_node(state: State, config: RunnableConfig) -> State:
    state["current_node"] = 4
    return click_action(state, config, x=200, y=150)

def input_filename_node(state: State, config: RunnableConfig) -> State:
    state["current_node"] = 5
    return input_action(state, config, text="state.file_name")

def click_submit_node(state: State, config: RunnableConfig) -> State:
    state["current_node"] = 6
    return click_action(state, config, x=180, y=220)

def wait_3s_node(state: State, config: RunnableConfig) -> State:
    state["current_node"] = 7
    return wait_action(state, config, duration=3)

def check_success_node(state: State, config: RunnableConfig) -> State:
    state["current_node"] = 1
    return click_action(state, config, x=150, y=300)

def click_close_node(state: State, config: RunnableConfig) -> State:
    state["current_node"] = 2
    return click_action(state, config, x=350, y=50)

def build_upload_workflow():
    workflow = StateGraph(State)
    
    workflow.add_node("validate_file", validate_file_node)
    workflow.add_node("click_documents", click_documents_node)
    workflow.add_node("wait_1s", wait_1s_node)
    workflow.add_node("click_upload", click_upload_node)
    workflow.add_node("input_filename", input_filename_node)
    workflow.add_node("click_submit", click_submit_node)
    workflow.add_node("wait_3s", wait_3s_node)
    
    workflow.set_entry_point("validate_file")
    workflow.add_edge("validate_file", "click_documents")
    workflow.add_edge("click_documents", "wait_1s")
    workflow.add_edge("wait_1s", "click_upload")
    workflow.add_edge("click_upload", "input_filename")
    workflow.add_edge("input_filename", "click_submit")
    workflow.add_edge("click_submit", "wait_3s")
    workflow.set_finish_point("wait_3s")
    
    return workflow.compile()

def build_confirmation_workflow():
    workflow = StateGraph(State)
    
    workflow.add_node("check_success", check_success_node)
    workflow.add_node("click_close", click_close_node)
    
    workflow.set_entry_point("check_success")
    workflow.add_edge("check_success", "click_close")
    workflow.set_finish_point("click_close")
    
    return workflow.compile()

def finalize_state(state: State, config: RunnableConfig) -> State:
    state["status"] = "Completed"
    return state

upload_workflow_graph = build_upload_workflow()
confirmation_workflow_graph = build_confirmation_workflow()

main_graph = StateGraph(State)

main_graph.add_node("upload_workflow", upload_workflow_graph)
main_graph.add_node("confirmation_workflow", confirmation_workflow_graph)
main_graph.add_node("finalize_state", finalize_state)

main_graph.set_entry_point("upload_workflow")
main_graph.add_edge("upload_workflow", "confirmation_workflow")
main_graph.add_edge("confirmation_workflow", "finalize_state")
main_graph.set_finish_point("finalize_state")

lgDocumentUpload = main_graph.compile()