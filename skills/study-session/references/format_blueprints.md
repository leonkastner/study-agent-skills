# 🎯 The 5 Interactive Study Question Format Blueprints

To ensure maximum cognitive depth and eliminate boring repetition, every in-chat study task must match one of these 5 distinct archetypes:

---

## Format 1: Applied Scenario Analysis & System Diagnosis
* **Goal:** Test if the student can apply abstract definitions to realistic, noisy real-world engineering or organizational problems.
* **Blueprint:**
  - Provide a concrete 3–4 sentence real-world case (e.g. an autonomous vehicle encountering an edge case, a hospital cobot making a triage error, or a financial model failing a loan audit).
  - Ask the student to diagnose which exact architectural layer failed, classify the behavior under a formal taxonomy, or evaluate trade-offs.
* **Example:**
  > *"A surgical robot arm follows human teleoperation commands but automatically stops motor actuation if the end-effector force exceeds 10 N to avoid tearing tissue. According to Moor's taxonomy of moral agents, what level of moral agency is this system, and why? Be specific about autonomy vs. ethical sensitivity."*

---

## Format 2: Numerical & Metric Calculations
* **Goal:** Test step-by-step mathematical reasoning and formula verification under exam time pressure.
* **Blueprint:**
  - Provide clean numerical input parameters (e.g. a $2 \times 2$ confusion matrix, probability distributions, or selection rates across demographic groups).
  - Require the student to state the formula, show step-by-step calculations, and compare the result against standard regulatory/ethical thresholds (e.g., $80\%$ Disparate Impact rule, equalized odds condition, expected utility).
* **Example:**
  > *"A hiring algorithm evaluates 100 male applicants (60 hired) and 50 female applicants (20 hired). Calculate the selection rates for both groups and compute the Disparate Impact Ratio (DIR). Does this system violate the EEOC 80% Rule for adverse impact?"*

---

## Format 3: Unguided Forensic Error-Spotting (Strict Zero-Hint Policy)
* **Goal:** Build peak Bloom Level 4 (`Evaluate`) competence by training the student to spot subtle technical errors.
* **MANDATORY RULES:**
  1. Never give hints.
  2. Never point to specific sentences or words.
  3. Never state the error count (e.g. do not say *"Find the 3 errors"*).
* **Blueprint:**
  - Present a mock student exam response that sounds convincing but contains 1–3 subtle factual, conceptual, or methodological errors.
  - Ask the student to evaluate the entire passage cold, identify all flawed claims, explain why they are wrong, and provide the correct professorial formulation.
* **Example:**
  > *"Evaluate the following mock exam student answer. Identify all factual, terminological, or conceptual errors and explain how to fix them:*  
  > *'LIME is an intrinsic, in-model explainability technique that works by training a global linear model on the entire dataset. It completely replaces the black-box neural network with a fully transparent decision tree.'*"

---

## Format 4: Real-Time Priority Triage & Decision Rules
* **Goal:** Test how the student resolves conflicting constraints using hierarchical pre-orders or ethical decision frameworks.
* **Blueprint:**
  - Give a system with multiple competing objectives (e.g. Safety vs. Speed vs. Comfort, or Deontology Rulebook priority hierarchies).
  - Ask the student to rank the rules, explain which constraint overrides which, and justify the outcome using professorial decision criteria.
* **Example:**
  > *"An autonomous vehicle faces a choice: (1) Cross a solid double white line to avoid hitting a debris box, or (2) Stay strictly in lane and collide with the debris. According to Censi et al.'s deontological rule ordering, how should the rulebook be ranked and which rule takes precedence?"*

---

## Format 5: Taxonomy & Matrix Classification
* **Goal:** Master comparative frameworks, 2D/3D grids, and structural category boundaries.
* **Blueprint:**
  - Provide a table, trade-off spectrum, or classification grid with missing items or category labels.
  - Ask the student to place algorithms, sensors, or governance models in the correct positions.
* **Example:**
  > *"Place the following 5 algorithms along an interpretability-complexity spectrum from Most Transparent (1) to Most Opaque (5): Deep Neural Network, Single Decision Tree (depth=3), Linear Regression, Random Forest (500 trees), Rule-Based Expert System."*
