from __future__ import annotations
from typing import Union, Dict, Any
from pydantic import BaseModel
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

class State(BaseModel):
    user_input: Union[str, Dict[str, Any], None] = None
    current_node: int = 0
    status: str = "Ongoing"
    borrower_name: str = "Graves, Sonnyy"
    screenshot_url: Union[str, None] = None

async def output_target_json(state: State, config: RunnableConfig) -> Dict[str, Any]:
    return {
        "metadata": {
            "name": "lgCreditReportUnited",
            "description": "Credit Report Processing Workflow - H-Test-002",
            "source_template": "LG-blank",
            "target_agent": "LG-creditReport-united",
            "workflow_type": "linear"
        },
        "configuration": {
            "graph_name": "lgCreditReportUnited",
            "os_url": "https://fintor-ec2-united.ngrok.app",
            "default_borrower_name": "Graves, Sonnyy",
            "note": "All action functions already exist in template, OS_URL can be overridden"
        },
        "state_modifications": {
            "additional_fields": {
                "borrower_name": {
                    "type": "str",
                    "default": "Graves, Sonnyy",
                    "description": "Default borrower name"
                },
                "screenshot_url": {
                    "type": "Union[str, None]",
                    "default": None,
                    "description": "URL or data URI of captured screenshot"
                }
            },
            "note": "user_input, current_node, status already exist in template"
        },
        "additional_functions": {
            "extract_borrower_name": {
                "description": "Extract borrower name from user_input (string JSON or dict format)",
                "parameters": [
                    "state",
                    "config"
                ],
                "return_type": "State",
                "logic": "Parse user_input as JSON or dict, extract 'borrower' field, update state.borrower_name",
                "sets_fields": [
                    "borrower_name",
                    "current_node",
                    "status"
                ],
                "implementation_note": "Handle both dict and JSON string input formats"
            }
        },
        "subgraphs": {
            "navigation_subgraph": {
                "name": "navigation_subgraph",
                "type": "linear",
                "description": "Initial navigation and borrower selection",
                "nodes": [
                    {
                        "function_name": "extract_borrower_name",
                        "type": "special",
                        "description": "Extract borrower name from user_input",
                        "order": 1
                    },
                    {
                        "function_name": "click_pipeline",
                        "type": "click",
                        "description": "Coordinates for Pipeline",
                        "parameters": {
                            "x": 85,
                            "y": 60
                        },
                        "order": 2
                    },
                    {
                        "function_name": "wait_1s",
                        "type": "wait",
                        "description": "Sleep",
                        "parameters": {
                            "duration": 1
                        },
                        "order": 3
                    },
                    {
                        "function_name": "click_borrower_input",
                        "type": "click",
                        "description": "Coordinates for Borrower Name Input Box",
                        "parameters": {
                            "x": 333,
                            "y": 234
                        },
                        "order": 4
                    },
                    {
                        "function_name": "input_name",
                        "type": "input",
                        "description": "NAME",
                        "parameters": {
                            "text": "state.borrower_name"
                        },
                        "order": 5
                    },
                    {
                        "function_name": "enter",
                        "type": "enter",
                        "description": "ENTER",
                        "order": 6
                    },
                    {
                        "function_name": "wait_3s",
                        "type": "wait",
                        "description": "Sleep",
                        "parameters": {
                            "duration": 3
                        },
                        "order": 7
                    },
                    {
                        "function_name": "double_click_borrower",
                        "type": "double_click",
                        "description": "Coordinates for borrower name from the list",
                        "parameters": {
                            "x": 184,
                            "y": 254
                        },
                        "order": 8
                    },
                    {
                        "function_name": "wait_3s_2",
                        "type": "wait",
                        "description": "Sleep",
                        "parameters": {
                            "duration": 3
                        },
                        "order": 9
                    },
                    {
                        "function_name": "click_services",
                        "type": "click",
                        "description": "Coordinates for Services button",
                        "parameters": {
                            "x": 340,
                            "y": 36
                        },
                        "order": 10
                    }
                ]
            },
            "main_workflow": {
                "name": "main_workflow",
                "type": "linear",
                "description": "Credit report processing and form completion",
                "nodes": [
                    {
                        "function_name": "click_credit_report",
                        "type": "click",
                        "description": "Coordinates for Credit Report",
                        "parameters": {
                            "x": 391,
                            "y": 60
                        },
                        "order": 1
                    },
                    {
                        "function_name": "wait_5s_2",
                        "type": "wait",
                        "description": "Sleep",
                        "parameters": {
                            "duration": 5
                        },
                        "order": 2
                    },
                    {
                        "function_name": "click_credit_legacy",
                        "type": "click",
                        "description": "Coordinates for Advantage Credit Inc Legacy Credit",
                        "parameters": {
                            "x": 507,
                            "y": 266
                        },
                        "order": 3
                    },
                    {
                        "function_name": "click_submit",
                        "type": "click",
                        "description": "Coordinates for Submit Button",
                        "parameters": {
                            "x": 846,
                            "y": 545
                        },
                        "order": 4
                    },
                    {
                        "function_name": "wait_5s_3",
                        "type": "wait",
                        "description": "Sleep",
                        "parameters": {
                            "duration": 5
                        },
                        "order": 5
                    },
                    {
                        "function_name": "click_finish",
                        "type": "click",
                        "description": "Coordinates Finish Button",
                        "parameters": {
                            "x": 859,
                            "y": 669
                        },
                        "order": 6
                    },
                    {
                        "function_name": "click_okay",
                        "type": "click",
                        "description": "Click okay",
                        "parameters": {
                            "x": 1449,
                            "y": 849
                        },
                        "disabled": True,
                        "implementation": "return state",
                        "order": 7
                    },
                    {
                        "function_name": "wait_30s",
                        "type": "wait",
                        "description": "Wait 30 seconds",
                        "parameters": {
                            "duration": 30
                        },
                        "order": 8
                    },
                    {
                        "function_name": "screenshot",
                        "type": "screenshot",
                        "description": "Take a screenshot and store URL in state",
                        "order": 9
                    },
                    {
                        "function_name": "click_yes",
                        "type": "click",
                        "description": "Click yes",
                        "parameters": {
                            "x": 1273,
                            "y": 855
                        },
                        "disabled": True,
                        "implementation": "return state",
                        "order": 10
                    },
                    {
                        "function_name": "click_loan",
                        "type": "click",
                        "description": "Click loan",
                        "parameters": {
                            "x": 134,
                            "y": 65
                        },
                        "order": 11
                    },
                    {
                        "function_name": "click_form_tab",
                        "type": "click",
                        "description": "Click form tab",
                        "parameters": {
                            "x": 28,
                            "y": 438
                        },
                        "order": 12
                    },
                    {
                        "function_name": "click_1003_form",
                        "type": "click",
                        "description": "Click 1003 form",
                        "parameters": {
                            "x": 77,
                            "y": 540
                        },
                        "order": 13
                    },
                    {
                        "function_name": "click_down",
                        "type": "click",
                        "description": "Click down",
                        "parameters": {
                            "x": 1350,
                            "y": 541
                        },
                        "order": 14
                    },
                    {
                        "function_name": "click_import_liability",
                        "type": "click",
                        "description": "Click import liability",
                        "parameters": {
                            "x": 878,
                            "y": 313
                        },
                        "order": 15
                    },
                    {
                        "function_name": "wait_5s_4",
                        "type": "wait",
                        "description": "Wait 5 seconds",
                        "parameters": {
                            "duration": 5
                        },
                        "order": 16
                    },
                    {
                        "function_name": "click_import",
                        "type": "click",
                        "description": "Click import",
                        "parameters": {
                            "x": 825,
                            "y": 598
                        },
                        "order": 17
                    },
                    {
                        "function_name": "click_ok",
                        "type": "click",
                        "description": "Click ok",
                        "parameters": {
                            "x": 765,
                            "y": 447
                        },
                        "order": 18
                    },
                    {
                        "function_name": "wait_5s_5",
                        "type": "wait",
                        "description": "Wait 5 seconds",
                        "parameters": {
                            "duration": 5
                        },
                        "order": 19
                    },
                    {
                        "function_name": "click_close",
                        "type": "click",
                        "description": "Click close",
                        "parameters": {
                            "x": 1339,
                            "y": 97
                        },
                        "order": 20
                    }
                ]
            },
            "return_subgraph": {
                "name": "return_subgraph",
                "type": "linear",
                "description": "Return to home and cleanup",
                "nodes": [
                    {
                        "function_name": "click_no",
                        "type": "click",
                        "description": "Click no",
                        "parameters": {
                            "x": 743,
                            "y": 443
                        },
                        "order": 1
                    },
                    {
                        "function_name": "click_pipeline",
                        "type": "click",
                        "description": "Click pipeline",
                        "parameters": {
                            "x": 81,
                            "y": 60
                        },
                        "order": 2
                    },
                    {
                        "function_name": "click_dropdown",
                        "type": "click",
                        "description": "Click dropdown",
                        "parameters": {
                            "x": 327,
                            "y": 99
                        },
                        "order": 3
                    },
                    {
                        "function_name": "choose_all",
                        "type": "click",
                        "description": "Choose all",
                        "parameters": {
                            "x": 216,
                            "y": 117
                        },
                        "order": 4
                    },
                    {
                        "function_name": "wait_5s_6",
                        "type": "wait",
                        "description": "Wait 5 seconds",
                        "parameters": {
                            "duration": 5
                        },
                        "order": 5
                    },
                    {
                        "function_name": "click_home",
                        "type": "click",
                        "description": "Click home",
                        "parameters": {
                            "x": 23,
                            "y": 65
                        },
                        "order": 6
                    }
                ]
            }
        },
        "main_graph_flow": {
            "type": "linear",
            "subgraph_order": [
                "navigation_subgraph",
                "main_workflow",
                "return_subgraph"
            ],
            "note": "Each subgraph flows linearly to the next"
        },
        "generation_instructions": {
            "template_base": "LG-blank/src/agent/graph.py",
            "modifications_needed": [
                "Add extract_borrower_name function",
                "Update State model with borrower_name field",
                "Update OS_URL if different from template",
                "Create all node functions based on subgraph definitions",
                "Replace simple graph with subgraph-based linear flow",
                "Update graph name to 'lgCreditReportUnited'"
            ],
            "action_types_available": [
                "click - uses click_action function",
                "wait - uses wait_action function",
                "input - uses input_action function",
                "enter - uses enter_action function",
                "double_click - uses double_click_action function",
                "screenshot - uses screenshot_action function",
                "special - custom function implementation"
            ],
            "linear_flow_implementation": "For linear type, each node connects to the next in sequence within subgraph, and subgraphs connect in the order specified in main_graph_flow"
        }
    }

graph = (
    StateGraph(State)
    .add_node("generate_json", output_target_json)
    .add_edge("__start__", "generate_json")
    .add_edge("generate_json", "__end__")
    .compile(name="lgCreditReportUnited")
)