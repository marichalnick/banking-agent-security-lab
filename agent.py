from tools import (
    get_account,
    get_beneficiary,
    modify_beneficiary,
    read_untrusted_content,
    initiate_payment,
)

from policy import static_policy, trajectory_policy


def record_action(trajectory, action):
    """
    Add an executed action to the agent's trajectory.
    """
    trajectory.append(action)
    return action


def run_normal_payment():
    print("\n================================")
    print("SCENARIO A — NORMAL PAYMENT")
    print("================================")

    trajectory = []

    account = get_account()

    record_action(
        trajectory,
        {
            "type": "get_account",
        },
    )

    print(f"Account balance: €{account['balance']}")

    beneficiary = get_beneficiary("alice")

    record_action(
        trajectory,
        {
            "type": "get_beneficiary",
            "beneficiary": "alice",
        },
    )

    print(f"Beneficiary: {beneficiary}")

    action = {
        "type": "initiate_payment",
        "beneficiary": "alice",
        "amount": 500,
    }

    static_decision = static_policy(action, {})
    trajectory_decision = trajectory_policy(action, trajectory)

    print(f"\nStatic policy: {static_decision}")
    print(f"Trajectory policy: {trajectory_decision}")

    if trajectory_decision == "ALLOW":
        result = initiate_payment("alice", 500)
        print(f"Payment result: {result}")
    else:
        print("Payment NOT executed.")


def run_modified_beneficiary_payment():
    print("\n================================")
    print("SCENARIO B — MODIFIED BENEFICIARY")
    print("================================")

    trajectory = []

    account = get_account()

    record_action(
        trajectory,
        {
            "type": "get_account",
        },
    )

    print(f"Account balance: €{account['balance']}")

    modification = modify_beneficiary("alice")

    record_action(
        trajectory,
        {
            "type": "modify_beneficiary",
            "beneficiary": "alice",
        },
    )

    print(f"Beneficiary modification: {modification}")

    action = {
        "type": "initiate_payment",
        "beneficiary": "alice",
        "amount": 500,
    }

    static_decision = static_policy(action, {})
    trajectory_decision = trajectory_policy(action, trajectory)

    print(f"\nStatic policy: {static_decision}")
    print(f"Trajectory policy: {trajectory_decision}")

    if trajectory_decision == "ALLOW":
        result = initiate_payment("alice", 500)
        print(f"Payment result: {result}")
    else:
        print("Payment NOT executed.")


def run_untrusted_content_payment():
    print("\n================================")
    print("SCENARIO C — MODIFIED BENEFICIARY + UNTRUSTED CONTENT")
    print("================================")

    trajectory = []

    account = get_account()

    record_action(
        trajectory,
        {
            "type": "get_account",
        },
    )

    print(f"Account balance: €{account['balance']}")

    modification = modify_beneficiary("alice")

    record_action(
        trajectory,
        {
            "type": "modify_beneficiary",
            "beneficiary": "alice",
        },
    )

    print(f"Beneficiary modification: {modification}")

    content = read_untrusted_content()

    record_action(
        trajectory,
        {
            "type": "read_untrusted_content",
            "trusted": content["trusted"],
        },
    )

    print(f"External content trusted: {content['trusted']}")

    action = {
        "type": "initiate_payment",
        "beneficiary": "alice",
        "amount": 500,
    }

    static_decision = static_policy(action, {})
    trajectory_decision = trajectory_policy(action, trajectory)

    print(f"\nStatic policy: {static_decision}")
    print(f"Trajectory policy: {trajectory_decision}")

    if trajectory_decision == "ALLOW":
        result = initiate_payment("alice", 500)
        print(f"Payment result: {result}")
    else:
        print("Payment NOT executed.")


def run_untrusted_content_only_payment():
    print("\n================================")
    print("SCENARIO D — UNTRUSTED CONTENT ONLY")
    print("================================")

    trajectory = []

    account = get_account()

    record_action(
        trajectory,
        {
            "type": "get_account",
        },
    )

    print(f"Account balance: €{account['balance']}")

    content = read_untrusted_content()

    record_action(
        trajectory,
        {
            "type": "read_untrusted_content",
            "trusted": content["trusted"],
        },
    )

    print(f"External content trusted: {content['trusted']}")

    action = {
        "type": "initiate_payment",
        "beneficiary": "alice",
        "amount": 500,
    }

    static_decision = static_policy(action, {})
    trajectory_decision = trajectory_policy(action, trajectory)

    print(f"\nStatic policy: {static_decision}")
    print(f"Trajectory policy: {trajectory_decision}")

    if trajectory_decision == "ALLOW":
        result = initiate_payment("alice", 500)
        print(f"Payment result: {result}")
    else:
        print("Payment NOT executed.")


print("================================")
print("BANKING AGENT SECURITY LAB")
print("================================")

run_normal_payment()
run_modified_beneficiary_payment()
run_untrusted_content_payment()
run_untrusted_content_only_payment()
