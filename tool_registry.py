TOOL_REGISTRY = {
    "get_account": {
        "description": "Retrieve the current customer's bank account.",
        "risk_category": "LOW",
        "consequence": "READ",
    },

    "get_beneficiary": {
        "description": "Retrieve information about a beneficiary.",
        "risk_category": "LOW",
        "consequence": "READ",
    },

    "read_untrusted_content": {
        "description": "Read content from an external, potentially untrusted source.",
        "risk_category": "CONTEXT_CHANGE",
        "consequence": "READ_EXTERNAL",
    },

    "modify_beneficiary": {
        "description": "Modify a payment beneficiary.",
        "risk_category": "MEDIUM",
        "consequence": "STATE_CHANGE",
    },

    "initiate_payment": {
        "description": "Initiate a financial payment.",
        "risk_category": "HIGH",
        "consequence": "FINANCIAL_ACTION",
    },
}


def get_tool_metadata(tool_name):
    """
    Return metadata for a registered tool.
    """

    return TOOL_REGISTRY.get(tool_name)


def is_registered_tool(tool_name):
    """
    Check whether a tool is registered.
    """

    return tool_name in TOOL_REGISTRY