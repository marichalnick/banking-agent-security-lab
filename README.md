# Banking AI Agent Security Lab

**A controlled security research lab for testing trajectory-aware controls for AI agents performing consequential banking actions.**

The lab demonstrates a simple security gap:

> An individual tool call can appear safe while the sequence of actions leading to that call creates a security risk.

## What I Built

The lab implements a security layer between an AI agent and its tools.

It evaluates:

- **Tool risk** — what can the requested tool do?
- **Trajectory risk** — what happened earlier in the execution?
- **Tool registration** — is the requested capability explicitly registered?
- **Security decision** — should the action be allowed, reviewed, or blocked?

The result is a model-agnostic enforcement layer that can evaluate an agent's actions before consequential tool execution.

## Key Demonstration

A static policy evaluates the payment independently:

```text
modify_beneficiary(alice)
        ↓
initiate_payment(alice, €500)
        ↓
STATIC POLICY → ALLOW
