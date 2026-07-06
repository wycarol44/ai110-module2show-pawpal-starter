# AI Interactions Log

> This file documents the stretch-feature work completed with AI assistance during the PawPal+ project.

---

## Agent Workflow (SF7)

**What task did I give the agent?**

I used an AI coding assistant to help implement several project features, including:
- drafting the README content
- creating the core Owner, Pet, Task, and Scheduler classes
- building the Streamlit UI for task entry and schedule generation
- adding task filtering and sorting features
- implementing recurring task behavior for daily and weekly tasks
- creating regression tests for core scheduling logic

**What did the agent do?**

The agent helped generate and refine the initial project structure, including the core models and scheduler logic. It also assisted with UI updates for displaying tasks, generating schedules, and supporting pet-based filtering. In addition, it helped implement recurring-task behavior and provided test scaffolding for the new functionality.

**What did I need to verify or fix manually?**

Several areas required human review and correction:
- import and module naming issues after the file was renamed
- scheduler logic that initially did not clearly explain scheduling decisions
- UI behavior around task deletion and task completion flow
- validation for invalid task data and recurring task creation
- refinement of the README wording to make it more professional and accurate

---

## Prompt Comparison (SF11)

| | Option A | Option B |
|---|----------|----------|
| **Model / tool used** | AI coding assistant | AI coding assistant |
| **Prompt** | Implement the core scheduling model and UI flow | Refine the model, add validation, and improve explanations |
| **Response summary** | Produced a strong initial implementation and useful code structure | Delivered more precise updates for logic refinement and testing |
| **What was useful** | Fast code generation and useful scaffolding | Better handling of edge cases and clearer implementation details |
| **Problems noticed** | Needed manual review for correctness and integration issues | Still required human verification for business logic and UI behavior |
| **Decision** | I used the refined approach for the final implementation because it balanced speed with better reliability. |

**Which approach did I use in the final implementation and why?**

I used the more refined AI-assisted approach because it produced cleaner, more maintainable code and required less manual restructuring. Although the assistant was helpful for implementation, I still verified the behavior manually to ensure the scheduler, UI, and tests matched the project requirements.
