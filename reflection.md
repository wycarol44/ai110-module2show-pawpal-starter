# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial design included four main classes: Owner, Pet, Scheduler, and Task. The Owner class represents the user and manages contact information and availability. The Pet class stores the pet’s basic details and is associated with tasks. The Scheduler class handles appointments and scheduling details such as date, time, duration, recurrence, and overlap rules. The Task class represents individual actions that need to be completed, such as feeding, walking, or medication.

In this design, an Owner can have one or more Pets and create multiple Scheduler entries. Each Scheduler entry can contain one or more Tasks, and each Pet can be assigned multiple Tasks.

- What classes did you include, and what responsibilities did you assign to each?
User should be able to perform are:
adding a pet to their profile, 
add tasks for each pets
delete the tasks,
scheduling tasks for pets, 

**b. Design changes**

- Did your design change during implementation?
yes
- If yes, describe at least one change and why you made it.
Add a bidirectional relationship between Owner and Pet so that each Pet stores a reference back to its owner (not just Owner → Pets list).
Replace task-level pet: string fields with a Pet ID or Pet object reference to enforce data consistency and enable validation of ownership and reusable pet metadata.
Strengthen data integrity by adding validation for missing or invalid pet assignments, invalid priority values, and invalid duration inputs at the task creation level.
Upgrade the scheduler logic to handle time conflicts explicitly, rather than only balancing task counts.
Extend the scheduler to support pet-specific constraints and preferences, ensuring tasks respect individual pet rules or restrictions.
Improve scheduling fairness and correctness by incorporating checks for invalid or incomplete task data before scheduling.
Enhance scheduler scalability by preparing for future rule complexity, as the current simple balancing approach may become a bottleneck.
Add an explainability layer to the scheduler so each scheduled task includes metadata on why it was selected and placed (e.g., priority, constraint satisfaction, or rule trigger).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
if start with priprity, iterating through pets with the sate priority, and without overlapping shchedule the time through 8;am 
- How did you decide which constraints mattered most?
from the priority to each pets, then the duration

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
if doesn't contain one time task or recurring task
- Why is that tradeoff reasonable for this scenario?
pets has regular routine, and one time task such as deworm or vacinnation

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
helped with coding the corresponding functions, and logic, and building mocdule and class
- What kinds of prompts or questions were most helpful?
implement a method ...

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
I asked AI to write the description and it's either too short or too many dummy words that, or it looks too AI
- How did you evaluate or verify what the AI suggested?
I think the ChatGPT did a great job with interaction and change, but the build in copilot in github might not be that powerful, and if I didn;t make it too detailed ,it will generate something completely out of my expection, and some thing might be out of control and hard to keep track of if the changes are too many

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Test the user flow, and do with pytest
- Why were these tests important?
To make sure everything go as aligned

**b. Confidence**

- How confident are you that your scheduler works correctly?
I'm not that confident, I felt there's always conner cases will happen
- What edge cases would you test next if you had more time?
with large data, and delete a pet

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
have some features to be implementing

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
UI, make if more hands on, if the interactive is too overwelming may be hard for someone to get used to the UI, and understand the concept

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
Human interaction with AI implementing is necessary, as a guidance with a feasiable feedback