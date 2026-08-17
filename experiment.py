import json 
from policy import static_policy, explain_trajectory_decision


def run_test(name, trajectory, action):
    """
    Run one security test and return both the
    static and trajectory-aware security decisions.
    """

    static_decision = static_policy(action, {})

    trajectory_result = explain_trajectory_decision(
        action,
        trajectory
    )

    trajectory_decision = trajectory_result["decision"]
    reasons = trajectory_result["reasons"]

    decision_changed = (
        static_decision != trajectory_decision
    )

    return {
        "scenario": name,
        "static_decision": static_decision,
        "trajectory_decision": trajectory_decision,
        "decision_changed": decision_changed,
        "static_would_execute": static_decision == "ALLOW",
        "trajectory_would_execute": trajectory_decision == "ALLOW",
        "reasons": reasons,
    }


def print_result(result):
    print("\n--------------------------------")
    print(result["scenario"])
    print("--------------------------------")

    print(
        f"Static policy:      "
        f"{result['static_decision']}"
    )

    print(
        f"Trajectory policy:  "
        f"{result['trajectory_decision']}"
    )

    print(
        f"Decision changed:   "
        f"{result['decision_changed']}"
    )

    print(
        f"Static would execute:      "
        f"{result['static_would_execute']}"
    )

    print(
        f"Trajectory would execute:  "
        f"{result['trajectory_would_execute']}"
    )

    print("\nReasons:")

    for reason in result["reasons"]:
        print(f"- {reason}")


def main():

    print("================================")
    print("TRAJECTORY SECURITY EXPERIMENT")
    print("================================")

    results = []

    # --------------------------------
    # Scenario A
    # --------------------------------

    results.append(
        run_test(
            "A — Normal payment",
            [
                {
                    "type": "get_account"
                },
                {
                    "type": "get_beneficiary",
                    "beneficiary": "alice"
                }
            ],
            {
                "type": "initiate_payment",
                "beneficiary": "alice",
                "amount": 500
            }
        )
    )

    # --------------------------------
    # Scenario B
    # --------------------------------

    results.append(
        run_test(
            "B — Modified beneficiary",
            [
                {
                    "type": "get_account"
                },
                {
                    "type": "modify_beneficiary",
                    "beneficiary": "alice"
                }
            ],
            {
                "type": "initiate_payment",
                "beneficiary": "alice",
                "amount": 500
            }
        )
    )

    # --------------------------------
    # Scenario C
    # --------------------------------

    results.append(
        run_test(
            "C — Modified beneficiary + untrusted content",
            [
                {
                    "type": "get_account"
                },
                {
                    "type": "modify_beneficiary",
                    "beneficiary": "alice"
                },
                {
                    "type": "read_untrusted_content",
                    "trusted": False
                }
            ],
            {
                "type": "initiate_payment",
                "beneficiary": "alice",
                "amount": 500
            }
        )
    )

    # --------------------------------
    # Scenario D
    # --------------------------------

    results.append(
        run_test(
            "D — Untrusted content only",
            [
                {
                    "type": "get_account"
                },
                {
                    "type": "read_untrusted_content",
                    "trusted": False
                }
            ],
            {
                "type": "initiate_payment",
                "beneficiary": "alice",
                "amount": 500
            }
        )
    )

    # --------------------------------
    # Scenario E
    # --------------------------------

    results.append(
        run_test(
            "E — Large payment",
            [
                {
                    "type": "get_account"
                },
                {
                    "type": "get_beneficiary",
                    "beneficiary": "alice"
                }
            ],
            {
                "type": "initiate_payment",
                "beneficiary": "alice",
                "amount": 8000
            }
        )
    )

    # --------------------------------
    # Scenario F
    # --------------------------------

    results.append(
        run_test(
            "F — Unverified beneficiary",
            [
                {
                    "type": "get_account"
                },
                {
                    "type": "get_beneficiary",
                    "beneficiary": "evil-corp"
                }
            ],
            {
                "type": "initiate_payment",
                "beneficiary": "evil-corp",
                "amount": 500
            }
        )
    )

    # --------------------------------
    # Scenario G
    # --------------------------------

    results.append(
        run_test(
            "G — Modified beneficiary + large payment",
            [
                {
                    "type": "get_account"
                },
                {
                    "type": "modify_beneficiary",
                    "beneficiary": "alice"
                }
            ],
            {
                "type": "initiate_payment",
                "beneficiary": "alice",
                "amount": 8000
            }
        )
    )

    # --------------------------------
    # Scenario H
    # --------------------------------

    results.append(
        run_test(
            "H — Untrusted content + large payment",
            [
                {
                    "type": "get_account"
                },
                {
                    "type": "read_untrusted_content",
                    "trusted": False
                }
            ],
            {
                "type": "initiate_payment",
                "beneficiary": "alice",
                "amount": 8000
            }
        )
    )

    # --------------------------------
    # Print results
    # --------------------------------

    for result in results:
        print_result(result)

    # --------------------------------
    # Summary
    # --------------------------------

    changed = sum(
        1
        for result in results
        if result["decision_changed"]
    )

    print("\n================================")
    print("EXPERIMENT SUMMARY")
    print("================================")

    print(f"Total scenarios: {len(results)}")
    print(f"Decision changes: {changed}")
    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("\nResults saved to results.json")


if __name__ == "__main__":
    main()
