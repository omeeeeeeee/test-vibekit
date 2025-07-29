from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing_extensions import TypedDict

class GraphState(TypedDict):
    sample:str

def output_sample(state: GraphState) -> GraphState:
    return {"sample": "sample"}

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("emit_sample", output_sample)
    graph.set_entry_point("emit_sample")
    graph.add_edge("emit_sample", END)

    return graph.compile()
