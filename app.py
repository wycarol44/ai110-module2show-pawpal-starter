import streamlit as st

from models import Owner, Pet


if "owner" not in st.session_state:
    initial_pet = Pet(name="CoCo", species="cat")
    st.session_state.owner = Owner(name="Carol")
    st.session_state.owner.add_pet(initial_pet)

if "pet" not in st.session_state:
    st.session_state.pet = Pet()

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input(
    "Owner name",
    value=st.session_state.owner.name,
    key="owner_name_input",
)

if st.button("Save owner profile"):
    st.session_state.owner.name = owner_name
    st.success("Owner profile saved!")

pet_name = st.text_input(
    "Pet name",
    value=st.session_state.pet.name,
    key="pet_name_input",
)
species_options = ["dog", "cat", "other"]
species_index = species_options.index(st.session_state.pet.species) if st.session_state.pet.species in species_options else 0
species = st.selectbox(
    "Species",
    species_options,
    index=species_index,
    key="species_input",
)

if st.button("Add pet to owner"):
    if pet_name.strip():
        st.session_state.owner.add_pet(Pet(pet_name, species))
        st.session_state.pet = Pet(name="", species="dog")
        st.success("Pet added to owner!")
    else:
        st.warning("Please enter a pet name.")

st.caption("Current saved profile")
st.write(f"Owner: {st.session_state.owner.name}")
if st.session_state.owner.pets:
    st.write("Pets:")
    for index, pet in enumerate(st.session_state.owner.pets, start=1):
        st.write(f"{index}. {pet.name} ({pet.species})")
else:
    st.write("No pets added yet.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
