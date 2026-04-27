# 📊 E-commerce A/B Test Analyzer

An interactive web application for analyzing A/B tests on e-commerce conversion data. Upload your test data and instantly see conversion rates, statistical significance, and a clear ship / no-ship recommendation.

🔗 **Live demo:** [your-streamlit-cloud-link-here]

---

## 🎯 What This Project Does

This tool helps product, marketing, and data teams answer the question:

> *"We ran an A/B test. Should we ship the variant or not?"*

It calculates everything needed for that decision:

- Conversion rates for control and variant groups
- Relative lift of the variant over control
- Statistical significance (two-proportion z-test, p-value)
- 95% confidence intervals for each group
- A combined ship / no-ship recommendation that considers both significance and business-meaningful lift

---

## 🛠️ Tech Stack

- **Python** — pandas, numpy, scipy
- **Statistics** — two-proportion z-test, hypothesis testing, confidence intervals
- **Streamlit** — interactive web UI
- **matplotlib** — visualization
- **Deployed on** Streamlit Community Cloud

---

## 🚀 Quick Start

### Run locally

```bash
# Clone the repo
git clone https://github.com/AkshaySarwade/ab-test-analyzer.git
cd ab-test-analyzer

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Or use the live demo

Visit the deployed app, upload your CSV (or use the simulated sample data), and explore the results.

---

## 📂 Input Data Format

Your CSV needs at least two columns:

| Column | Type | Description |
|--------|------|-------------|
| `group` | string | `'control'` or `'variant'` |
| `converted` | int | `1` if user converted, `0` otherwise |

Example:

```csv
user_id,group,converted
1,control,0
2,control,1
3,variant,1
4,variant,0
...
```

---

## 📈 What You'll See

1. **Configuration sidebar** — set your significance level (α) and minimum business lift threshold
2. **Data preview** — check your data loaded correctly
3. **Metrics dashboard** — conversion rates, lift, p-value at a glance
4. **Confidence intervals table** — plausible true conversion rates for each group
5. **Visualization** — bar chart with 95% CI error bars
6. **Recommendation** — clear SHIP IT / DO NOT SHIP / INCONCLUSIVE verdict with reasoning

---

## 🧠 Decision Logic

The recommendation engine uses two thresholds:

- **Statistical significance** (default α = 0.05): the result must be unlikely under the null hypothesis
- **Minimum business lift** (default 2%): the lift must be large enough to be worth shipping

| Significant? | Lift > min? | Recommendation |
|:---:|:---:|---|
| ✅ | ✅ | **SHIP IT** |
| ✅ | ❌ | DO NOT SHIP (significant but lift too small) |
| ❌ | ✅ | INCONCLUSIVE (run longer) |
| ❌ | ❌ | DO NOT SHIP |

This mirrors how real product teams make ship decisions — statistical significance alone is not enough; the lift also has to matter to the business.

---

## 🔬 Statistical Methods

### Two-proportion z-test

Tests whether two conversion rates come from populations with the same true rate. The pooled standard error is calculated under the null hypothesis that the rates are equal.

```
SE = sqrt( p_pool * (1 - p_pool) * (1/n1 + 1/n2) )
z  = (p2 - p1) / SE
p  = 2 * (1 - Φ(|z|))
```

### Confidence interval (Wald)

```
CI = p ± z * sqrt( p * (1 - p) / n )
```

For most A/B tests with reasonable sample sizes, the Wald interval is fine. For very small samples or rates near 0 or 1, more advanced methods (Wilson, Clopper-Pearson) would be more appropriate — a possible future enhancement.

---

## 🔮 Future Enhancements

- [ ] Sample size calculator (how many users do I need to detect X% lift?)
- [ ] Sequential testing support
- [ ] Bayesian A/B testing alongside frequentist
- [ ] Multi-variant (A/B/C/n) tests
- [ ] Segment analysis (lift by user segment)

---

## 📚 Why I Built This

Working in a production ML pipeline at Shelf Watch, I see how much business decisions depend on rigorous experimentation — but it's easy to get statistical significance wrong, and a lot of teams ship features based on lift alone. I wanted to build a tool that combines both, in a way that's accessible to non-statisticians but still statistically sound.

---

## 👤 Author

**Akshay Sarwade**
🔗 [LinkedIn](https://www.linkedin.com/in/akshay0sarwade) • [GitHub](https://github.com/AkshaySarwade) • akshaysarwade00@gmail.com

---

## 📄 License

MIT — feel free to fork, learn from, and build on this.
