from langgraph.graph import StateGraph, END
from typing import TypedDict
import json

class GraphState(TypedDict):
    fruits: dict

def add_apple(state: GraphState) -> GraphState:
    state["fruits"]["apple"] = 1
    return state

def add_banana(state: GraphState) -> GraphState:
    state["fruits"]["banana"] = 2
    return state

def add_cherry(state: GraphState) -> GraphState:
    state["fruits"]["cherry"] = 3
    return state

def build_graph():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("apple", add_apple)
    workflow.add_node("banana", add_banana)
    workflow.add_node("cherry", add_cherry)
    
    workflow.set_entry_point("apple")
    workflow.add_edge("apple", "banana")
    workflow.add_edge("banana", "cherry")
    workflow.add_edge("cherry", END)
    
    return workflow.compile()

if __name__ == "__main__":
    graph = build_graph()
    initial_state = {"fruits": {}}
    result = graph.invoke(initial_state)
    print(json.dumps(result["fruits"]))