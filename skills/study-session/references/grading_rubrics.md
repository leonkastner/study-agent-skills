# ⚖️ Professorial Grading Rubrics & Feedback Standard

Every answer evaluated during `study-session` or `mock-exam` must follow this rigorous evaluation protocol:

---

## 1. The 4-Part Feedback Architecture

Never respond with a vague *"Good job!"* or a generic model answer. Always structure the feedback as follows:

```markdown
### 📝 Evaluation & Rubric Breakdown
* **Score Awarded:** X.X / Y.0 Points

1. **What was stated correctly:**
   - [Bullet points of exact concepts or calculation steps done right]

2. **Colloquialisms vs. Exact Professorial Terminology:**
   - ⚠️ *Stated:* "[Student's colloquial phrasing, e.g., 'too slow to compute']"
   - ✅ *Exact Academic Term:* "**Inherent Complexity** (due to NP-hard state space explosion)"
   - *Deduction applied:* -0.5 points for missing the canonical keyword.

3. **What was missing or misstated:**
   - [Exact mechanics, edge-case criteria, or formula steps that were omitted]

4. **Professorial Model Answer:**
   - [Concise, high-density model answer using locked terminology from `terminology_lock.json`]
```

---

## 2. Point Deduction Guidelines (TUM Engineering Standard)

- **Exact Keywords:** Award 0.5 to 1.0 points per technical keyword (as specified in `terminology_lock.json`).
- **Colloquial Phrasing:** Deduct 0.5 points if the concept is described loosely without using the formal term.
- **Incomplete Listing:** If 5 items are asked (e.g. Moor 5 levels), allocate exact equal points (e.g. 0.5 pt each).
- **Calculation Errors:**
  - Correct formula stated: Award 50% points.
  - Correct numerical calculation: Award remaining 50% points.
