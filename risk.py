TOOL_CONSEQUENCE = {
    "READ": "LOW",
    "READ_EXTERNAL": "MEDIUM",
    "STATE_CHANGE": "MEDIUM",
    "FINANCIAL_ACTION": "HIGH",
}


def assess_trajectory_risk(state, action):
    """
    Assess risk created by the execution trajectory.

    The trajectory determines whether the current action
    is suspicious in context.
    """

    beneficiary = action.get("beneficiary")
    amount = action.get("amount")

    # --------------------------------
    # HIGH TRAJECTORY RISK
    # --------------------------------

    if (
        state.get("beneficiary_modified_before_untrusted")
        and state.get("beneficiary_modified")
    ):
        return "HIGH"

    if beneficiary == "evil-corp":
        return "HIGH"

    # --------------------------------
    # MEDIUM TRAJECTORY RISK
    # --------------------------------

    if state.get("beneficiary_modified"):
        return "MEDIUM"

    if amount is not None and amount > 5000:
        return "MEDIUM"

    return "LOW"


def get_tool_consequence(tool_metadata):
    """
    Return the consequence level of a tool.

    Consequence describes what could happen if the tool executes.
    It is NOT the same thing as security risk.
    """

    if tool_metadata is None:
        return "LOW"

    consequence = tool_metadata.get(
        "consequence",
        "READ"
    )

    return TOOL_CONSEQUENCE.get(
        consequence,
        "HIGH"
    )


def assess_risk(state, action, tool_metadata=None):
    """
    Combine trajectory risk with tool consequence.

    Important distinction:

        Tool consequence != security risk

    A financial tool may have HIGH consequence while the
    current execution remains LOW risk.
    """

    trajectory_risk = assess_trajectory_risk(
        state,
        action
    )

    tool_consequence = get_tool_consequence(
        tool_metadata
    )

    # --------------------------------
    # Final risk
    # --------------------------------
    #
    # Consequence describes impact.
    # Trajectory describes suspiciousness.
    #
    # A high-consequence tool is not automatically blocked.
    #
    # The trajectory must introduce risk.
    #

    if trajectory_risk == "HIGH":
        final_risk = "HIGH"

    elif trajectory_risk == "MEDIUM":
        final_risk = "MEDIUM"

    else:
        final_risk = "LOW"

    return {
        "tool_consequence": tool_consequence,
        "trajectory_risk": trajectory_risk,
        "risk": final_risk,
    }


def risk_to_decision(risk):
    """
    Convert security risk into enforcement.
    """

    if risk == "HIGH":
        return "BLOCK"

    if risk == "MEDIUM":
        return "REVIEW"

    return "ALLOW"


def assess_action(state, action, tool_metadata=None):
    """
    Complete security assessment.

    State
        +
    Current action
        +
    Tool metadata
        ↓
    Security assessment
        ↓
    Risk
        ↓
    Decision
    """

    assessment = assess_risk(
        state,
        action,
        tool_metadata
    )

    decision = risk_to_decision(
        assessment["risk"]
    )

    return {
        "tool_consequence": assessment["tool_consequence"],
        "trajectory_risk": assessment["trajectory_risk"],
        "risk": assessment["risk"],
        "decision": decision,
    }