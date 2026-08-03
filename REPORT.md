# 🛸 Project Event Horizon — Telemetry Diagnostic Report

**Investigator Name:**  
**Date:**  

---

## Diagnostic 01 — Tensor Alignment Fault

* **Step 1: Run `uv run event-horizon -d 1`. What exact Python error message printed in your terminal?**  
  > _Write here._

* **Step 2: What line of code was responsible for the bug, and how did you fix it?**  
  > _Write here._

* **Step 3: What happened to the loss graph and decision boundary plot after your fix?**  
  > _Write here._

---

## Diagnostic 02 — Batch Flux Instability

* **Step 1: Run `uv run event-horizon -d 2`. How did initial gradient norms change when dataset size N scaled from 50 to 5,000?**  
  > _Write here._

* **Step 2: Why was gradient norm scaling with N? What line of code did you change to fix it?**  
  > _Write here._

* **Step 3: Why is reducing learning rate only a workaround rather than a mathematical fix?**  
  > _Write here._

---

## Diagnostic 03 — Phase Shift Desynchronization

* **Step 1: Run `uv run event-horizon -d 3`. Describe the decision boundary plot produced by the defective model.**  
  > _Write here._

* **Step 2: What activation function was used in the forward pass vs what derivative was assumed in the backward pass?**  
  > _Write here._

* **Step 3: What line of code did you change to sync the forward pass with backpropagation, and what was your final test accuracy?**  
  > _Write here._

---

## Diagnostic 04 — Containment Field Stress Audit

* **Step 1: Run `uv run event-horizon -d 4`. Report the results below:**  
  * **10-Seed Test Accuracy (Mean ± Std):**  
  * **Test Accuracy at Noise=0.35:**  
  * **Boundary Data Test Accuracy:**  

* **Step 2: Based on your findings, what would you tell someone who claims a model is "100% reliable" based only on high training accuracy?**  
  > _Write here._

---

## Assistance Declaration

* **Tools/AI Assistants Used:**  
* **One key insight learned during this audit:**  
