#!/usr/bin/env python3
"""
Langgraph Document Upload Agent
Generates the expected JSON output for the document upload workflow
"""

import json

def generate_document_upload_config():
    """Generate the complete document upload configuration JSON"""
    
    config = {
        'metadata': {
            'name': 'lgDocumentUpload',
            'description': 'Document Upload Workflow - Test Case',
            'source_template': 'LG-blank',
            'target_agent': 'LG-document-upload',
            'workflow_type': 'linear'
        },
        'configuration': {
            'graph_name': 'lgDocumentUpload',
            'os_url': 'https://fintor-ec2-test.ngrok.app',
            'default_file_name': 'test_document.pdf',
            'note': 'Simple workflow for testing graph.py functionality'
        },
        'state_modifications': {
            'additional_fields': {
                'file_name': {
                    'type': 'str',
                    'default': 'test_document.pdf',
                    'description': 'Name of file to upload'
                },
                'upload_url': {
                    'type': 'Union[str, None]',
                    'default': None,
                    'description': 'URL where file was uploaded'
                }
            },
            'note': 'Basic state tracking for document upload'
        },
        'additional_functions': {
            'validate_file': {
                'description': 'Validate file exists and is PDF format',
                'parameters': ['state', 'config'],
                'return_type': 'State',
                'logic': 'Check if file exists and has .pdf extension',
                'sets_fields': ['file_name', 'current_node', 'status'],
                'implementation_note': 'Return error if file invalid'
            }
        },
        'subgraphs': {
            'upload_workflow': {
                'name': 'upload_workflow',
                'type': 'linear',
                'description': 'Basic document upload sequence',
                'nodes': [
                    {
                        'function_name': 'validate_file',
                        'type': 'special',
                        'description': 'Validate input file',
                        'order': 1
                    },
                    {
                        'function_name': 'click_documents',
                        'type': 'click',
                        'description': 'Click Documents tab',
                        'parameters': {'x': 120, 'y': 50},
                        'order': 2
                    },
                    {
                        'function_name': 'wait_1s',
                        'type': 'wait',
                        'description': 'Wait for tab to load',
                        'parameters': {'duration': 1},
                        'order': 3
                    },
                    {
                        'function_name': 'click_upload',
                        'type': 'click',
                        'description': 'Click Upload button',
                        'parameters': {'x': 200, 'y': 150},
                        'order': 4
                    },
                    {
                        'function_name': 'input_filename',
                        'type': 'input',
                        'description': 'Enter filename',
                        'parameters': {'text': 'state.file_name'},
                        'order': 5
                    },
                    {
                        'function_name': 'click_submit',
                        'type': 'click',
                        'description': 'Click Submit button',
                        'parameters': {'x': 180, 'y': 220},
                        'order': 6
                    },
                    {
                        'function_name': 'wait_3s',
                        'type': 'wait',
                        'description': 'Wait for upload',
                        'parameters': {'duration': 3},
                        'order': 7
                    }
                ]
            },
            'confirmation_workflow': {
                'name': 'confirmation_workflow',
                'type': 'linear',
                'description': 'Confirm upload success',
                'nodes': [
                    {
                        'function_name': 'check_success',
                        'type': 'click',
                        'description': 'Check success message',
                        'parameters': {'x': 150, 'y': 300},
                        'order': 1
                    },
                    {
                        'function_name': 'click_close',
                        'type': 'click',
                        'description': 'Close upload dialog',
                        'parameters': {'x': 350, 'y': 50},
                        'order': 2
                    }
                ]
            }
        },
        'main_graph_flow': {
            'type': 'linear',
            'subgraph_order': ['upload_workflow', 'confirmation_workflow'],
            'note': 'Simple linear flow: upload then confirm'
        },
        'generation_instructions': {
            'template_base': 'LG-blank/src/agent/graph.py',
            'modifications_needed': [
                'Add validate_file function',
                'Update State model with file_name field',
                'Update OS_URL if different from template',
                'Create node functions for upload workflow',
                'Create node functions for confirmation workflow',
                "Update graph name to 'lgDocumentUpload'"
            ],
            'action_types_available': [
                'click - uses click_action function',
                'wait - uses wait_action function',
                'input - uses input_action function',
                'special - custom function implementation'
            ],
            'linear_flow_implementation': 'Each node connects to next in sequence within subgraph'
        }
    }
    
    return config

def main():
    """Main function to generate and output the JSON configuration"""
    config = generate_document_upload_config()
    print(json.dumps(config, separators=(',', ': ')))

if __name__ == "__main__":
    main()