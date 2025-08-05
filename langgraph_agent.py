from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing_extensions import TypedDict
from typing import Any, Dict
import json
import re

class WorkflowState(TypedDict):
    input_data: Any
    validated_data: Dict[str, Any]
    processed_data: Dict[str, Any]
    errors: list
    status: str

def input_validation(state: WorkflowState) -> WorkflowState:
    """Validates input data according to business rules"""
    input_data = state.get("input_data")
    errors = []
    validated_data = {}
    
    if not input_data:
        errors.append("No input data provided")
        return {
            **state,
            "errors": errors,
            "status": "validation_failed"
        }
    
    if isinstance(input_data, str):
        try:
            input_data = json.loads(input_data)
        except json.JSONDecodeError:
            errors.append("Invalid JSON format")
    
    if isinstance(input_data, dict):
        if "name" in input_data:
            name = input_data["name"]
            if isinstance(name, str) and len(name.strip()) > 0:
                validated_data["name"] = name.strip()
            else:
                errors.append("Name must be a non-empty string")
        else:
            errors.append("Missing required field: name")
        
        if "email" in input_data:
            email = input_data["email"]
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if isinstance(email, str) and re.match(email_pattern, email):
                validated_data["email"] = email.lower()
            else:
                errors.append("Invalid email format")
        
        if "age" in input_data:
            age = input_data["age"]
            if isinstance(age, (int, float)) and 0 <= age <= 150:
                validated_data["age"] = int(age)
            else:
                errors.append("Age must be a number between 0 and 150")
    else:
        errors.append("Input data must be a dictionary or valid JSON string")
    
    status = "validation_failed" if errors else "validation_passed"
    
    return {
        **state,
        "validated_data": validated_data,
        "errors": errors,
        "status": status
    }

def data_processing(state: WorkflowState) -> WorkflowState:
    """Processes validated data and performs business logic"""
    if state.get("status") == "validation_failed":
        return {
            **state,
            "processed_data": {},
            "status": "processing_skipped"
        }
    
    validated_data = state.get("validated_data", {})
    processed_data = {}
    
    if "name" in validated_data:
        processed_data["full_name"] = validated_data["name"].title()
        processed_data["name_length"] = len(validated_data["name"])
    
    if "email" in validated_data:
        processed_data["email_domain"] = validated_data["email"].split("@")[1]
        processed_data["email_normalized"] = validated_data["email"]
    
    if "age" in validated_data:
        age = validated_data["age"]
        if age < 18:
            processed_data["age_group"] = "minor"
        elif age < 65:
            processed_data["age_group"] = "adult"
        else:
            processed_data["age_group"] = "senior"
        
        processed_data["age"] = age
    
    processed_data["processing_timestamp"] = "2024-01-01T00:00:00Z"
    processed_data["record_id"] = f"user_{hash(str(validated_data))}"
    
    return {
        **state,
        "processed_data": processed_data,
        "status": "processing_completed"
    }

def build_workflow():
    """Builds and returns the LangGraph workflow"""
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("input_validation", input_validation)
    workflow.add_node("data_processing", data_processing)
    
    workflow.set_entry_point("input_validation")
    workflow.add_edge("input_validation", "data_processing")
    workflow.add_edge("data_processing", END)
    
    return workflow.compile()

def run_workflow(input_data: Any) -> Dict[str, Any]:
    """Convenience function to run the workflow with input data"""
    workflow = build_workflow()
    
    initial_state = {
        "input_data": input_data,
        "validated_data": {},
        "processed_data": {},
        "errors": [],
        "status": "initialized"
    }
    
    result = workflow.invoke(initial_state)
    return result

if __name__ == "__main__":
    test_data = {
        "name": "john doe",
        "email": "JOHN.DOE@EXAMPLE.COM",
        "age": 30
    }
    
    result = run_workflow(test_data)
    print("Workflow Result:")
    print(f"Status: {result['status']}")
    print(f"Errors: {result['errors']}")
    print(f"Validated Data: {result['validated_data']}")
    print(f"Processed Data: {result['processed_data']}")