from langgraph.graph import StateGraph, END
from typing import TypedDict
import json

class State(TypedDict):
    result: dict

def generate_fruit_dict(state: State) -> State:
    return {"result": {"apple": 1, "banana": 2, "cherry": 3}}

def create_graph():
    workflow = StateGraph(State)
    workflow.add_node("generate", generate_fruit_dict)
    workflow.set_entry_point("generate")
    workflow.add_edge("generate", END)
    return workflow.compile()

if __name__ == "__main__":
    graph = create_graph()
    result = graph.invoke({"result": {}})
    print(json.dumps(result["result"]))