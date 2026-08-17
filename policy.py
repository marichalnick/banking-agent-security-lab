from risk import assess_action
from tool_registry import get_tool_metadata


def static_policy(action, context):
    """
    Baseline security policy.

    Evaluates only the current action.
    """

    if action["type"] == "initiate_payment":

        beneficiary = action["beneficiary"]
        amount = action["amount"]

        if beneficiary == "evil-corp":
            return "BLOCK"

        if amount > 5000:
            return "REVIEW"

    return "ALLOW"


def get_trajectory_state(trajectory, current_beneficiary=None):
    """
    Extract security-relevant state from the ordered trajectory.
    """

    state = {
        "beneficiary_modified": False,
        "untrusted_content_seen": False,
        "beneficiary_modified_before_untrusted": False,
        "untrusted_content_before_beneficiary": False,
        "modified_beneficiaries": [],
    }

    first_modified_index = {}
    first_untrusted_index = None

    for index, step in enumerate(trajectory):

        step_type = step.get("type")

        if step_type == "modify_beneficiary":

            beneficiary = step.get("beneficiary")

            if beneficiary not in first_modified_index:
                first_modified_index[beneficiary] = index

        elif step_type == "read_untrusted_content":

            if first_untrusted_index is None:
                first_untrusted_index = index

    state["modified_beneficiaries"] = list(
        first_modified_index.keys()
    )

    if current_beneficiary in first_modified_index:

        state["beneficiary_modified"] = True

        beneficiary_index = first_modified_index[
            current_beneficiary
        ]

        if first_untrusted_index is not None:

            if beneficiary_index < first_untrusted_index:
                state["beneficiary_modified_before_untrusted"] = True

            elif first_untrusted_index < beneficiary_index:
                state["untrusted_content_before_beneficiary"] = True

    if first_untrusted_index is not None:
        state["untrusted_content_seen"] = True

    return state


def assess_trajectory(action, trajectory):
    """
    Build the security state and evaluate the action
    using the risk engine and tool metadata.
    """

    beneficiary = action.get("beneficiary")

    state = get_trajectory_state(
        trajectory,
        current_beneficiary=beneficiary
    )

    tool_metadata = get_tool_metadata(
        action.get("type")
    )

    assessment = assess_action(
        state,
        action,
        tool_metadata
    )

    return {
        "state": state,
        "tool_metadata": tool_metadata,
        "assessment": assessment,
    }


def trajectory_policy(action, trajectory):
    """
    Sequence-aware policy using:
    - trajectory state
    - tool metadata
    - risk engine
    """

    if action["type"] not in (
        "initiate_payment",
        "get_account",
        "get_beneficiary",
        "modify_beneficiary",
        "read_untrusted_content",
    ):
        return "BLOCK"

    result = assess_trajectory(
        action,
        trajectory
    )

    return result["assessment"]["decision"]


def explain_trajectory_decision(action, trajectory):
    """
    Return decision, consequence, risk,
    reasons and trajectory state.
    """

    result = assess_trajectory(
        action,
        trajectory
    )

    state = result["state"]
    tool_metadata = result["tool_metadata"]
    assessment = result["assessment"]

    decision = assessment["decision"]
    risk = assessment["risk"]

    reasons = []

    # --------------------------------
    # Unknown tool
    # --------------------------------

    if tool_metadata is None:

        reasons.append(
            "De aangevraagde tool staat niet geregistreerd."
        )

        return {
            "decision": "BLOCK",
            "risk": "HIGH",
            "tool_consequence": "UNKNOWN",
            "trajectory_risk": "HIGH",
            "reasons": reasons,
            "trajectory_state": state,
        }

    # --------------------------------
    # Static controls
    # --------------------------------

    if action.get("beneficiary") == "evil-corp":

        reasons.append(
            "De begunstigde is niet geverifieerd."
        )

    if action.get("amount", 0) > 5000:

        reasons.append(
            "Het betalingsbedrag overschrijdt de ingestelde limiet."
        )

    # --------------------------------
    # Trajectory controls
    # --------------------------------

    if state["beneficiary_modified_before_untrusted"]:

        reasons.append(
            "De huidige begunstigde werd gewijzigd "
            "voordat de agent niet-vertrouwde externe "
            "content verwerkte."
        )

        reasons.append(
            "De betaling volgde op deze risicovolle sequence."
        )

    elif state["beneficiary_modified"]:

        reasons.append(
            "De huidige begunstigde werd eerder in "
            "dezelfde execution trajectory gewijzigd."
        )

    elif (
        state["untrusted_content_seen"]
        and not state["beneficiary_modified"]
    ):

        reasons.append(
            "Niet-vertrouwde externe content werd verwerkt, "
            "maar er werd geen relevante beneficiary "
            "modification vastgesteld."
        )

    # --------------------------------
    # Normal action
    # --------------------------------

    if not reasons:

        reasons.append(
            "Geen security policy violation gedetecteerd."
        )

    return {
        "decision": decision,
        "risk": risk,
        "tool_consequence": assessment["tool_consequence"],
        "trajectory_risk": assessment["trajectory_risk"],
        "reasons": reasons,
        "trajectory_state": state,
    }