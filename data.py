# Synthetic 10-K excerpt for a fictional wealth management software company.
# Realistic domain, fictional company — safe to use for demos and interviews.

DOCUMENT = """
WEALTHTECH CORP
Form 10-K Annual Report Excerpt — Fiscal Year 2024

─────────────────────────────────────────────
RISK FACTORS
─────────────────────────────────────────────

1. Client Concentration Risk
   Three clients — BlackRock, Fidelity, and Vanguard — collectively account for 42% of annual
   recurring revenue ($187M of $445M total). Loss of any single relationship would be material.
   BlackRock's current contract expires in Q3 2025 and is under active renewal negotiation.

2. Regulatory Exposure
   The SEC's proposed amendments to Rule 22e-4 and FINRA Regulatory Notice 24-07 on algorithmic
   portfolio management are under active rulemaking. Estimated compliance cost: $8–12M over the
   next 18 months. Non-compliance penalties could reach $50M per violation. We have retained
   outside counsel at an additional $2.1M annually.

3. Technology Obsolescence
   Our core rebalancing engine, built in 2018, services 2.1 million accounts. Competitors Orion,
   Envestnet, and Riskalyze all launched AI-native engines in 2024. We have allocated $34M in
   R&D for FY2025 to modernize infrastructure, but execution risk is high given 22% engineering
   attrition in FY2024.

4. Talent Retention
   Engineering attrition reached 22% in FY2024 versus a 14% industry average. A $6.2M annual
   retention program was implemented in Q4 2024. Five senior engineers departed to Orion Advisor
   Solutions, which raised $120M Series D specifically targeting AI rebalancing capabilities.

─────────────────────────────────────────────
FINANCIAL PERFORMANCE
─────────────────────────────────────────────

Revenue:              $445M  (+12% YoY from $397M in FY2023)
Recurring revenue:    $396M  (89% of total; SaaS model)
Adjusted EBITDA:      $134M  (30.1% margin, up from 28.2% in FY2023)
Net Revenue Retention: 118%
Free Cash Flow:       $98M   (+22% YoY)

─────────────────────────────────────────────
MANAGEMENT GUIDANCE — FISCAL YEAR 2025
─────────────────────────────────────────────

Revenue:             $490M–$510M  (10–15% YoY growth)
Adjusted EBITDA margin: 31–33%
R&D investment:      $34M  (≈7% of revenue midpoint)
Headcount growth:    +8% net, primarily engineering and data science

Management notes that the $500M midpoint implies H2 2025 acceleration contingent on closing
two enterprise contracts currently in final negotiation (estimated combined ARR: $18M).
Guidance assumes no material regulatory disruption and continued macro stability.

─────────────────────────────────────────────
COMPETITIVE POSITION
─────────────────────────────────────────────

WealthTech Corp serves approximately 85,000 registered investment advisors and 300+ institutional
asset managers in the United States.

Competitive advantages cited by management:

- Switching costs: Average implementation is 14 months, creating high churn friction.
  12-year average client tenure is 3× the industry average of 4 years.

- Data network effects: $2.1T in processed assets generates proprietary benchmarking data
  unavailable to smaller competitors; used by 23 of the top 50 U.S. asset managers.

- Regulatory expertise: Compliance team includes four former SEC officials. This is cited
  by enterprise clients as a key differentiator in RFP processes.

- Custodian integrations: 147 direct integrations (Schwab, Fidelity, Pershing, etc.),
  versus Orion (89) and Envestnet (102). Each integration takes 6–18 months to build.

Primary competitive threat: Orion's $120M Series D raise in Q3 2024 is directed at
AI-native rebalancing and tax-loss harvesting capabilities that could erode WealthTech's
product differentiation within 18–24 months.
"""

# Questions a wealth manager or analyst would ask about this filing
QUESTIONS = [
    "What are the top 3 risk factors that could materially impact revenue?",
    "What is management's specific revenue guidance for fiscal year 2025?",
    "What competitive advantages does the company cite, and how defensible are they?",
]
