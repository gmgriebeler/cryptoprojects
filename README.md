(A) - Jupiter DEX Trading Volume Alert Bot

This project automatically tracks the **weekly trading volume on Jupiter**, the leading DEX aggregator on Solana, using the [Dune API](https://dune.com/docs/api/) and sends alerts to a **Discord channel** every week.

The script is scheduled via **GitHub Actions** and can also be triggered manually.

---

(B) - Features

- Fetches real-time analytics from [Dune Analytics](https://dune.com/)
- Detects trading volumes on Jupiter
- Sends formatted alerts to Discord via webhook
- Runs weekly using GitHub Actions (cron)

---

(C) - Project Structure

cryptoprojects/
│
├── .github/workflows/
│ └── dune_alert_bot.yml # GitHub Actions workflow
│
├── jupiter_trading_volume_ath_alert_dune_api_integration_2.py # Main Python script
├── requirements.txt # Python dependencies
└── README.md # This file


---


(D) - Example Alert

" Jupiter Total Volume Weekly Update "
Week of 2025-06-02
Total Volume: $344,621,861.70
Rank: #86 all-time
