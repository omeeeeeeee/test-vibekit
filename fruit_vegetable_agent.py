from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing_extensions import TypedDict

class GraphState(TypedDict):
    fruit: str
    vegetable: str

def output_fruit_vegetable(state: GraphState) -> GraphState:
    return {"fruit": "apple", "vegetable": "eggplant"}

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("emit_fruit_vegetable", output_fruit_vegetable)
    graph.set_entry_point("emit_fruit_vegetable")
    graph.add_edge("emit_fruit_vegetable", END)

    return graph.compile()