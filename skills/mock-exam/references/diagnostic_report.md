# 🩺 Mock Exam Diagnostic Post-Mortem Standard

After evaluating a full mock exam, always output a structured diagnostic report and update the ledger's review urgency queue:

```markdown
# 🏁 Mock Exam Diagnostic Post-Mortem & Performance Breakdown

### 📊 Score Overview
* **Total Score:** XX.X / 120.0 Points (YY.Y%)
* **Estimated Grade Tier:** 1.X / Pass / Excellent
* **Time Efficiency:** Target 90 min (Completed in Z min)

---

### 🔍 Detailed Problem-by-Problem Score Breakdown
| Problem # | Module / Topic | Max Pts | Scored | Mastery Status | Primary Error / Deduction Note |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **P1** | [Module 1 Title] | 12.0 | 11.5 | `Exam Ready` | Minor colloquialism on term X (-0.5) |
| **P2** | [Module 2 Title] | 12.0 | 8.0 | `Fragile` | Missed step 2 in calculation (-4.0) |
| ... | ... | ... | ... | ... | ... |

---

### 🚨 Fragile Knowledge Units & Immediate Remediation Plan
1. **[Unit ID — Unit Title]:** Scored X%. *Action:* Scheduled for rapid active calculation drill in next study session.
2. **[Unit ID — Unit Title]:** Misconception logged in `weaknesses_log`. *Review urgency reset to 3.0 (Highest Priority).*

👉 **Next Step:** Run `study-session` to drill these specific remediation targets before the final exam.
```
