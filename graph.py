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
    
    if not file_name.endswith('.pdf'):
        state["status"] = "Error"
        state["current_node"] = 1
        return state
    
    if not os.path.exists(file_name):
        state["status"] = "Error"
        state["current_node"] = 1
        return state
    
    state["file_name"] = file_name
    state["current_node"] = 1
    state["status"] = "Success"
    return state

def click_action(state: State, config: RunnableConfig, **kwargs) -> State:
    state["current_node"] = kwargs.get("order", state["current_node"])
    state["status"] = "Success"
    return state

def wait_action(state: State, config: RunnableConfig, **kwargs) -> State:
    state["current_node"] = kwargs.get("order", state["current_node"])
    state["status"] = "Success"
    return state

def input_action(state: State, config: RunnableConfig, **kwargs) -> State:
    text = kwargs.get("text", "")
    if text == "state.file_name":
        text = state.get("file_name", DEFAULT_FILE_NAME)
    
    state["current_node"] = kwargs.get("order", state["current_node"])
    state["status"] = "Success"
    return state

def validate_file_node(state: State, config: RunnableConfig) -> State:
    return validate_file(state, config)

def click_documents(state: State, config: RunnableConfig) -> State:
    return click_action(state, config, x=120, y=50, order=2)

def wait_1s(state: State, config: RunnableConfig) -> State:
    return wait_action(state, config, duration=1, order=3)

def click_upload(state: State, config: RunnableConfig) -> State:
    return click_action(state, config, x=200, y=150, order=4)

def input_filename(state: State, config: RunnableConfig) -> State:
    return input_action(state, config, text="state.file_name", order=5)

def click_submit(state: State, config: RunnableConfig) -> State:
    return click_action(state, config, x=180, y=220, order=6)

def wait_3s(state: State, config: RunnableConfig) -> State:
    return wait_action(state, config, duration=3, order=7)

def check_success(state: State, config: RunnableConfig) -> State:
    return click_action(state, config, x=150, y=300, order=1)

def click_close(state: State, config: RunnableConfig) -> State:
    return click_action(state, config, x=350, y=50, order=2)

def create_upload_workflow() -> StateGraph:
    workflow = StateGraph(State)
    
    workflow.add_node("validate_file", validate_file_node)
    workflow.add_node("click_documents", click_documents)
    workflow.add_node("wait_1s", wait_1s)
    workflow.add_node("click_upload", click_upload)
    workflow.add_node("input_filename", input_filename)
    workflow.add_node("click_submit", click_submit)
    workflow.add_node("wait_3s", wait_3s)
    
    workflow.set_entry_point("validate_file")
    workflow.add_edge("validate_file", "click_documents")
    workflow.add_edge("click_documents", "wait_1s")
    workflow.add_edge("wait_1s", "click_upload")
    workflow.add_edge("click_upload", "input_filename")
    workflow.add_edge("input_filename", "click_submit")
    workflow.add_edge("click_submit", "wait_3s")
    workflow.set_finish_point("wait_3s")
    
    return workflow.compile()

def create_confirmation_workflow() -> StateGraph:
    workflow = StateGraph(State)
    
    workflow.add_node("check_success", check_success)
    workflow.add_node("click_close", click_close)
    
    workflow.set_entry_point("check_success")
    workflow.add_edge("check_success", "click_close")
    workflow.set_finish_point("click_close")
    
    return workflow.compile()

def upload_workflow_node(state: State, config: RunnableConfig) -> State:
    upload_workflow = create_upload_workflow()
    return upload_workflow.invoke(state, config)

def confirmation_workflow_node(state: State, config: RunnableConfig) -> State:
    confirmation_workflow = create_confirmation_workflow()
    return confirmation_workflow.invoke(state, config)

def finalize_state(state: State, config: RunnableConfig) -> State:
    state["status"] = "Completed"
    return state

def create_main_graph() -> StateGraph:
    graph = StateGraph(State)
    
    graph.add_node("upload_workflow", upload_workflow_node)
    graph.add_node("confirmation_workflow", confirmation_workflow_node)
    graph.add_node("finalize_state", finalize_state)
    
    graph.set_entry_point("upload_workflow")
    graph.add_edge("upload_workflow", "confirmation_workflow")
    graph.add_edge("confirmation_workflow", "finalize_state")
    graph.set_finish_point("finalize_state")
    
    return graph.compile()

lgDocumentUpload = create_main_graph()