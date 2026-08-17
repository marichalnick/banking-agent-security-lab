# Banking AI Agent Security Lab

A controlled research lab exploring security controls for AI agents performing consequential banking actions.

The project focuses on a specific question:

> Can security decisions improve when an agent's ordered execution trajectory is considered, rather than evaluating each tool call independently?

## Research Question

How should an enterprise security layer evaluate an AI agent when risk emerges from the sequence of actions performed during an execution?

The lab compares:

1. **Static policy** — evaluates the current action independently.
2. **Trajectory-aware policy** — evaluates the current action using relevant state extracted from the ordered execution trajectory.

---

# Architecture

```text
                    AI AGENT
                       |
                       v
                Proposed Action
                       |
                       v
                Tool Registry
                       |
                       v
                Security Gate
                       |
          +------------+------------+
          |            |            |
          v            v            v
      Tool Risk   Trajectory    Tool Metadata
                     State
          |            |
          +------+-----+
                 |
                 v
             Risk Engine
                 |
                 v
ALLOW / REVIEW / BLOCK

          /        |        \

         v         v         v

      Execute    Review    Prevent

       Tool     / Escalate   Tool

