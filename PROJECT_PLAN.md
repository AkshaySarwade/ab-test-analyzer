# 🗓️ Weekend Build Plan — A/B Test Analyzer

This is your step-by-step roadmap. Follow it in order. Total time: **~10-12 hours** spread over a weekend.

---

## ✅ BEFORE YOU START

**You have everything you need:**
- `app.py` — the full Streamlit application (working code)
- `requirements.txt` — list of dependencies
- `README.md` — professional README ready to push
- `sample_data.csv` — test data
- This plan

**You only need to:**
1. Get the code running on your machine
2. Find a real Kaggle dataset (~30 min)
3. Push to GitHub (15 min)
4. Deploy to Streamlit Cloud (15 min)
5. Add screenshots and polish

That's it.

---

## 📅 DAY 1 (Saturday) — Build & Run It Locally

### Step 1: Set up the project (15 min)

```bash
# Navigate to your projects folder
cd C:\Users\admin

# Create the project folder
mkdir ab-test-analyzer
cd ab-test-analyzer

# Copy the 4 files I gave you into this folder:
# - app.py
# - requirements.txt
# - README.md
# - sample_data.csv
```

### Step 2: Install dependencies (10 min)

```bash
pip install -r requirements.txt
```

If `pip` complains, try: `pip install streamlit pandas numpy scipy matplotlib seaborn`

### Step 3: Run the app locally (5 min)

```bash
streamlit run app.py
```

Browser opens at `http://localhost:8501`. Click "Use sample data" and you should see the full dashboard working.

**Screenshot this!** You'll need it for your README and LinkedIn post.

### Step 4: Understand the code (1-2 hours)

Open `app.py` in VS Code and read through it section by section. Understand:

- **`calculate_conversion_rates`** — pandas groupby
- **`calculate_lift`** — basic percentage math
- **`two_proportion_z_test`** — the core statistical test
- **`confidence_interval`** — uses the normal distribution
- **`make_recommendation`** — combines significance + business threshold

If anything confuses you, paste it back to me and I'll explain. **Important:** you must understand this code, because in interviews they'll ask "walk me through how your z-test works."

### Step 5: Find a real Kaggle dataset (30 min)

Go to https://www.kaggle.com and search: **"ab test ecommerce"**

Top picks (any of these works):

1. **"A/B Testing Dataset"** by Saraswat — ~294K rows, classic e-commerce conversion test
2. **"E-commerce A/B Testing"** — landing page test data
3. **"Marketing A/B Testing"** — ad campaign test data

Download the CSV, rename the columns if needed to match `group` and `converted`, save it as `data/ecommerce_ab_test.csv` in your project folder.

---

## 📅 DAY 2 (Sunday) — Polish, Push, Deploy

### Step 6: Test with real data (30 min)

```bash
streamlit run app.py
```

Click "Upload CSV" and load your real Kaggle dataset. Take a screenshot of the results.

**You now have a real result to talk about in interviews:**
> "When I ran my analyzer on a 294K-row Kaggle e-commerce A/B test, I found a [X]% lift with p-value [Y], leading to a [SHIP IT / NO-GO] recommendation."

That sentence alone is worth more than 10 generic resume bullets.

### Step 7: Push to GitHub (30 min)

```bash
cd C:\Users\admin\ab-test-analyzer

# Initialize git
git init
git add .
git commit -m "Initial commit: A/B test analyzer with Streamlit UI"

# Create a new repo on github.com (named: ab-test-analyzer)
# Then connect your local repo:
git remote add origin https://github.com/AkshaySarwade/ab-test-analyzer.git
git branch -M main
git push -u origin main
```

### Step 8: Deploy to Streamlit Cloud (20 min)

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Select your `ab-test-analyzer` repo, `main` branch, `app.py` as the main file
5. Click "Deploy"

After ~2 minutes you'll have a public URL like:
`https://akshaysarwade-ab-test-analyzer.streamlit.app`

**Update the README** — replace `[your-streamlit-cloud-link-here]` with your actual deployed URL, commit, and push.

### Step 9: Add screenshots to README (45 min)

Take 3 screenshots from your running app:

1. The main dashboard with metrics
2. The visualization (bar chart with confidence intervals)
3. The recommendation card

Create a folder `docs/` in your repo, save screenshots there, and add to your README:

```markdown
## 📸 Screenshots

### Dashboard
![Dashboard](docs/dashboard.png)

### Visualization
![Visualization](docs/visualization.png)

### Recommendation
![Recommendation](docs/recommendation.png)
```

### Step 10: Polish, push, done (30 min)

- Re-read your README — fix any typos
- Make sure live demo link works
- Make sure code runs cleanly when cloned fresh

**Final commit:**
```bash
git add .
git commit -m "Add screenshots and finalize documentation"
git push
```

---

## 🎤 Interview Talking Points

When asked **"Tell me about a project you're proud of"**, you say:

> "I built an A/B test analyzer because I noticed that most teams ship features based on lift alone, without checking statistical significance — or vice versa. My tool combines both. The user uploads their A/B test data, and the app calculates conversion rates, performs a two-proportion z-test, builds 95% confidence intervals, and gives a clear ship recommendation only if the result is both statistically significant AND meets a business-meaningful lift threshold. I deployed it to Streamlit Cloud — anyone can try it. I tested it on a 294K-row e-commerce dataset from Kaggle to validate the results."

When they ask **"Walk me through the z-test"**:

> "I used a two-proportion z-test. I calculate the conversion rate for control and variant, compute the pooled proportion under the null hypothesis, then the standard error, and from there the z-statistic. The two-tailed p-value comes from the normal CDF. If p is below 0.05, we reject the null — meaning the difference is unlikely to be from chance alone."

When they ask **"What would you improve?"**:

> "Three things — first, support for sequential testing so we don't peek at results too early. Second, a Bayesian view alongside the frequentist one, because Bayesian gives a more intuitive 'probability variant is better' answer. Third, segment analysis — sometimes a feature wins overall but loses on specific user segments, and you'd never know without that breakdown."

You **deeply understand** all three of those answers because you wrote the code. That is what separates real candidates from claimers.

---

## 📢 Bonus: LinkedIn Post (Day 3 if you want)

After deploying, write a short post:

> **"I built an A/B test analyzer in Python and Streamlit."**
>
> Most product teams I've talked to ship features based on lift alone, without checking statistical significance. So I built a tool that combines both — runs a two-proportion z-test, calculates 95% confidence intervals, and only recommends shipping if BOTH conditions are met: statistically significant AND meaningful lift.
>
> Tested on a 294K-row e-commerce dataset. Live demo:  [link]  | Code: [github]
>
> Built with: Python, pandas, scipy, Streamlit
>
> #DataAnalytics #ABTesting #Statistics #Python

This brings recruiters to you. Genuinely.

---

## ✋ AFTER THIS IS LIVE

Once your project is on GitHub and deployed, **then** update your resume to add A/B testing — **not before.** Recruiters click GitHub links during screening; they need to see the project actually exists.

Add a new project bullet:

> **A/B Test Analyzer** — Statistical Analysis + Streamlit Deployment
> - Built and deployed an interactive A/B testing tool that calculates conversion lift, runs two-proportion z-tests, computes confidence intervals, and gives ship/no-ship recommendations. Tested on a 294K-row Kaggle e-commerce dataset. *Python, pandas, scipy, Streamlit.*

And in skills, you can now honestly add:
- **A/B Testing:** two-proportion z-tests, confidence intervals, hypothesis testing, ship-decision frameworks

---

## 🚦 Done When

- [ ] App runs locally
- [ ] You understand every function in `app.py`
- [ ] Real Kaggle dataset loaded and tested
- [ ] Code pushed to GitHub
- [ ] Deployed to Streamlit Cloud (live URL)
- [ ] Screenshots in README
- [ ] You can answer the 3 interview questions above without notes

When all 7 are checked, you have a project that genuinely upgrades your candidacy. **Then we update the resume.**

---

Good luck, Akki. This is the real work. Send me the GitHub link when it's live and I'll review.

Jay Bhim.
